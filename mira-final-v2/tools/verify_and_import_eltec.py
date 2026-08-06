#!/usr/bin/env python3
"""Fail-closed ELTeC-ita v0.3.0 verifier/importer for the F192-vs-GRU final."""
from __future__ import annotations
import argparse, hashlib, json, re, tempfile, unicodedata, zipfile
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET

EXPECTED_MD5 = "9195844caf7e1d61e7b44aaa00743c15"
SPLIT_SEED = "137"
TEI = "{http://www.tei-c.org/ns/1.0}"
XI = "{http://www.w3.org/2001/XInclude}"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:['’][A-Za-zÀ-ÖØ-öø-ÿ]+)?")
HYPHEN_RE = re.compile(r"([A-Za-zÀ-ÖØ-öø-ÿ])-\s*\n\s*([A-Za-zÀ-ÖØ-öø-ÿ])")
MODERN = {
    "perchè":"perché", "poichè":"poiché", "affinchè":"affinché", "benchè":"benché", "nè":"né",
    "avea":"aveva", "aveano":"avevano", "potea":"poteva", "poteano":"potevano",
    "dovea":"doveva", "doveano":"dovevano", "volea":"voleva",
    "dicea":"diceva", "diceano":"dicevano", "facea":"faceva", "faceano":"facevano",
    "vedea":"vedeva", "vedeano":"vedevano", "sapea":"sapeva", "sapeano":"sapevano",
    "parea":"pareva", "pareano":"parevano",
}
APOSTROPHES = {"‘":"'", "’":"'", "ʼ":"'", "`":"'"}

def digest(path: Path, name: str) -> str:
    h = hashlib.new(name)
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""): h.update(block)
    return h.hexdigest()

def case_like(src: str, dst: str) -> str:
    if src.isupper(): return dst.upper()
    if src[:1].isupper(): return dst[:1].upper() + dst[1:]
    return dst

def normalize_text(raw: str, counts: Counter) -> str:
    before = raw
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    counts["line_ending_normalized"] += before.count("\r")
    before = raw
    raw = unicodedata.normalize("NFC", raw)
    counts["unicode_nfc_changed_codepoints"] += sum(a != b for a,b in zip(before, raw)) + abs(len(before)-len(raw))
    for ch, rep in APOSTROPHES.items():
        n = raw.count(ch); counts[f"apostrophe_{ord(ch):04x}_to_ascii"] += n; raw = raw.replace(ch, rep)
    n = raw.count("\u00a0"); counts["nbsp_to_space"] += n; raw = raw.replace("\u00a0", " ")
    while True:
        raw, n = HYPHEN_RE.subn(r"\1\2", raw)
        counts["line_end_hyphen_recomposed"] += n
        if not n: break
    for old, new in MODERN.items():
        pat = re.compile(rf"(?<![A-Za-zÀ-ÖØ-öø-ÿ]){re.escape(old)}(?![A-Za-zÀ-ÖØ-öø-ÿ])", re.I)
        def repl(m): return case_like(m.group(0), new)
        raw, n = pat.subn(repl, raw); counts[f"modernize:{old}->{new}"] += n
    raw, n = re.subn(r"[ \t\f\v]+", " ", raw); counts["horizontal_whitespace_collapsed"] += n
    raw, n = re.subn(r" +([,.;:!?])", r"\1", raw); counts["space_before_punctuation_removed"] += n
    raw, n = re.subn(r"([«“]) +", r"\1", raw); counts["space_after_open_quote_removed"] += n
    raw, n = re.subn(r" +([»”])", r"\1", raw); counts["space_before_close_quote_removed"] += n
    raw, n = re.subn(r"\n{3,}", "\n\n", raw); counts["excess_blank_lines_collapsed"] += n
    return raw.strip()

def element_text(el: ET.Element) -> str:
    return " ".join(x.strip() for x in el.itertext() if x and x.strip())

def parse_work(path: Path) -> dict:
    root = ET.parse(path).getroot()
    sid = root.attrib.get(XML_ID, path.stem)
    title_el = root.find(f".//{TEI}titleStmt/{TEI}title")
    author_el = root.find(f".//{TEI}titleStmt/{TEI}author")
    title = element_text(title_el) if title_el is not None else path.stem
    author = element_text(author_el) if author_el is not None else "sconosciuto"
    body = root.find(f".//{TEI}body")
    if body is None: raise ValueError(f"body TEI assente: {path}")
    counts = Counter(); paragraphs=[]
    for el in body.iter():
        tag = el.tag.rsplit("}",1)[-1]
        if tag in {"head","p","l","sp","stage","quote"}:
            text = normalize_text(element_text(el), counts)
            if len(WORD_RE.findall(text)) >= 3: paragraphs.append(text)
    seen=set(); unique=[]
    for p in paragraphs:
        key=hashlib.sha256(p.casefold().encode()).digest()
        if key in seen: counts["duplicate_paragraph_removed"] += 1
        else: seen.add(key); unique.append(p)
    text="\n".join(unique).strip()
    if len(WORD_RE.findall(text)) < 500: raise ValueError(f"opera troppo corta: {path}")
    return {"source_id":sid,"title":title,"author":author,"text":text,
            "word_count":len(WORD_RE.findall(text)),"source_sha256":digest(path,"sha256"),
            "normalized_sha256":hashlib.sha256(text.encode()).hexdigest(),"normalization_counts":dict(sorted(counts.items()))}

def rank(sid: str) -> bytes: return hashlib.sha256((SPLIT_SEED+"\0"+sid).encode()).digest()
def corpus_stats(text: str) -> dict:
    words=[w.casefold().replace("’", "'") for w in WORD_RE.findall(text)]
    return {"bytes":len(text.encode()),"words":len(words),"types":len(set(words)),
            "ttr":len(set(words))/len(words) if words else 0.0,"sha256":hashlib.sha256(text.encode()).hexdigest()}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("archive"); ap.add_argument("--out",default="data/eltec_finale")
    ns=ap.parse_args(); archive=Path(ns.archive); out=Path(ns.out)
    if not archive.is_file(): raise SystemExit("INPUT_MISSING: archivio ELTeC non trovato")
    md5=digest(archive,"md5")
    if md5 != EXPECTED_MD5: raise SystemExit(f"ARCHIVE_MD5_MISMATCH expected={EXPECTED_MD5} found={md5}")
    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(archive) as z: z.extractall(td)
        drivers=list(Path(td).rglob("driver.tei"))
        if len(drivers)!=1: raise SystemExit(f"DRIVER_COUNT_FAIL found={len(drivers)}")
        driver=ET.parse(drivers[0]).getroot(); refs=[]
        for el in driver.iter(f"{XI}include"):
            href=el.attrib.get("href","")
            if href.startswith("level1/") and href.endswith(".xml"): refs.append(href)
        if len(refs)!=34 or len(set(refs))!=34: raise SystemExit(f"LEVEL1_DRIVER_FAIL expected=34 found={len(refs)} unique={len(set(refs))}")
        base=drivers[0].parent
        works=[]
        for href in refs:
            p=base/href
            if not p.is_file(): raise SystemExit(f"REFERENCED_FILE_MISSING {href}")
            works.append(parse_work(p))
    works.sort(key=lambda w: rank(w["source_id"]))
    groups={"tune":works[0:4],"test_dev":works[4:8],"test_confirm":works[8:12],"train":works[12:34]}
    out.mkdir(parents=True,exist_ok=True)
    audit={"schema":"mira-finale-eltec-v1","archive":{"md5":md5,"sha256":digest(archive,"sha256"),"bytes":archive.stat().st_size},
           "source_disjoint":True,"split_seed":137,"work_count":34,"normalization_rules":list(MODERN.items()),"splits":{},"works":{}}
    works_dir = out / "works"
    works_dir.mkdir(parents=True, exist_ok=True)
    for split, group in groups.items():
        chunks=[]
        for w in group:
            work_rel = f"works/{w['source_id']}.txt"
            (out / work_rel).write_text(w["text"], encoding="utf-8")
            chunks.append("[DOC]\n"+w["text"]+"\n\n")
            audit["works"][w["source_id"]]={k:v for k,v in w.items() if k!="text"}|{"split":split,"normalized_path":work_rel}
        text="".join(chunks); (out/f"{split}.txt").write_text(text,encoding="utf-8")
        audit["splits"][split]=corpus_stats(text)|{"works":len(group),"source_ids":[w["source_id"] for w in group]}
    (out/"audit.json").write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding="utf-8")
    with (out / "works.tsv").open("w", encoding="utf-8", newline="\n") as f:
        f.write("split\tsource_id\tnormalized_path\ttitle\tauthor\n")
        for split in ("train", "tune", "test_dev", "test_confirm"):
            for sid in audit["splits"][split]["source_ids"]:
                w = audit["works"][sid]
                safe_title = w["title"].replace("\t", " ").replace("\n", " ")
                safe_author = w["author"].replace("\t", " ").replace("\n", " ")
                f.write(f"{split}\t{sid}\t{w['normalized_path']}\t{safe_title}\t{safe_author}\n")
    print(json.dumps(audit,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
