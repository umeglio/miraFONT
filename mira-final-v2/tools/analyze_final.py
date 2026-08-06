#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,datetime,hashlib,json,math,statistics
from pathlib import Path
SEEDS=[1972,2718,3141,1618,2026,5772,8119]
TCRIT=2.4469118511449692

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()
def rows(p):
 with Path(p).open(newline='') as f:return list(csv.DictReader(f))
def kv(p):
 d={}
 for line in Path(p).read_text(errors='replace').splitlines():
  if '=' in line:
   a,b=line.split('=',1); d[a.strip()]=b.strip()
 return d

def validate(root):
 out=[]
 for kind in ('f192','gru'):
  for seed in SEEDS:
   d=root/'trained'/kind/str(seed); q=kv(d/'result.txt')
   ok=q.get('early_stopped')=='1' and q.get('profile_pass')=='1' and 8<=float(q.get('epochs','0'))<=30
   if not ok: raise RuntimeError(f'contract fail {kind}/{seed}: {q}')
   out.append({'kind':kind,'seed':seed,'lr':float(q['lr']),'updates':int(q['updates']),
    'epochs':float(q['epochs']),'best_tune_content_nll':float(q['best_tune_content_nll']),
    'best_tune_content_ppl':float(q['best_tune_content_ppl']),'peak_rss':int(q['peak_rss']),
    'best_sha256':sha(d/'best.bin')})
 return out

def analyze(root,split):
 per=[]; seed_delta=[]
 for seed in SEEDS:
  fr=rows(root/f'f192_{seed}.csv'); gr=rows(root/f'gru_{seed}.csv')
  if len(fr)!=128 or len(gr)!=128: raise RuntimeError(f'{split} windows {seed}: {len(fr)}/{len(gr)}')
  f=[float(x['content_nll_mean']) for x in fr]; g=[float(x['content_nll_mean']) for x in gr]
  d=[a-b for a,b in zip(f,g)]; dm=statistics.fmean(d); seed_delta.append(dm)
  fn=statistics.fmean(f); gn=statistics.fmean(g)
  per.append({'seed':seed,'f192_content_nll':fn,'gru_content_nll':gn,
   'f192_content_ppl':math.exp(fn),'gru_content_ppl':math.exp(gn),
   'delta_nll_f_minus_g':dm,'f192_window_wins':sum(x<0 for x in d),
   'gru_window_wins':sum(x>0 for x in d),'ties':sum(x==0 for x in d)})
 mean=statistics.fmean(seed_delta); sd=statistics.stdev(seed_delta); half=TCRIT*sd/math.sqrt(7)
 lo,hi=mean-half,mean+half
 fp=math.exp(statistics.fmean(x['f192_content_nll'] for x in per)); gp=math.exp(statistics.fmean(x['gru_content_nll'] for x in per))
 fw=sum(x['delta_nll_f_minus_g']<0 for x in per); gw=7-fw
 fe=gp/fp-1; ge=fp/gp-1
 if fw>=6 and hi<0 and fe>=.03: verdict='FOURIER192_WINS'
 elif gw>=6 and lo>0 and ge>=.03: verdict='GRU_WINS'
 else: verdict='PAREGGIO'
 return {'split':split,'per_seed':per,'aggregate':{'mean_delta_nll_f_minus_g':mean,
  'sd_seed_delta':sd,'ci95_low':lo,'ci95_high':hi,'f192_seed_wins':fw,'gru_seed_wins':gw,
  'f192_ppl_geomean':fp,'gru_ppl_geomean':gp,'f192_advantage_pct':100*fe,
  'gru_advantage_pct':100*ge,'verdict':verdict}}

def table(a):
 o=['| Seed | PPL F192 | PPL GRU | ΔNLL F−G | Finestre F/GRU |','|---:|---:|---:|---:|---:|']
 for r in a['per_seed']:o.append(f"| {r['seed']} | {r['f192_content_ppl']:.6f} | {r['gru_content_ppl']:.6f} | {r['delta_nll_f_minus_g']:+.9f} | {r['f192_window_wins']}/{r['gru_window_wins']} |")
 x=a['aggregate'];o+=['',f"PPL geometriche F192/GRU: **{x['f192_ppl_geomean']:.6f} / {x['gru_ppl_geomean']:.6f}**. ΔNLL: **{x['mean_delta_nll_f_minus_g']:+.9f}**, CI95 **[{x['ci95_low']:+.9f}, {x['ci95_high']:+.9f}]**. Seed F192/GRU: **{x['f192_seed_wins']}/{x['gru_seed_wins']}**. Gate: **{x['verdict']}**.",'']
 return o

def prof(root):
 out=[]
 for kind in ('f192','gru'):
  for seed in SEEDS:
   rr=rows(root/'trained'/kind/str(seed)/'profiler.csv'); use=rr[5:] or rr
   t=[float(x['tokens_per_second']) for x in use]
   out.append({'kind':kind,'seed':seed,'blocks':len(rr),'median_tps':statistics.median(t),
    'mean_tps':statistics.fmean(t),'bad_blocks':sum(x['speed_ok']!='1' or x['rss_ok']!='1' for x in rr),
    'max_current_rss':max(int(x['current_rss']) for x in rr),'max_peak_rss':max(int(x['peak_rss']) for x in rr)})
 return out

def manifest(root,out):
 fs=[]
 for p in sorted(root.rglob('*')):
  if p.is_file() and p!=out:fs.append({'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)})
 out.write_text(json.dumps({'created_utc':now(),'files':fs},indent=2,sort_keys=True)+'\n')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['dev','final']);ap.add_argument('--root',type=Path,required=True);a=ap.parse_args();r=a.root
 runs=validate(r)
 if a.mode=='dev':
  d=analyze(r/'eval_dev','DEV');(r/'dev_analysis.json').write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
  md=['# DEV decision frozen','',f'Created UTC: `{now()}`','',f"Gate DEV: **{d['aggregate']['verdict']}**",'']+table(d)+['CONFIRM non è stato valutato al momento di questo lock.','']
  p=r/'DEV_DECISION_FROZEN.md';p.write_text('\n'.join(md))
  q=r/'DEV_LOCK.json';q.write_text(json.dumps({'created_utc':now(),'dev_report_sha256':sha(p),'dev_analysis_sha256':sha(r/'dev_analysis.json'),'run_contracts':len(runs),'confirm_scored':False},indent=2,sort_keys=True)+'\n')
  print(json.dumps({'dev_lock_sha256':sha(q),'dev':d['aggregate']},indent=2));return
 if not (r/'DEV_LOCK.json').exists():raise RuntimeError('DEV lock missing')
 (r/'CONFIRM_OPENED.json').write_text(json.dumps({'opened_utc':now(),'dev_lock_sha256':sha(r/'DEV_LOCK.json'),'one_shot':True},indent=2,sort_keys=True)+'\n')
 dev=json.loads((r/'dev_analysis.json').read_text());con=analyze(r/'eval_confirm','CONFIRM');(r/'confirm_analysis.json').write_text(json.dumps(con,indent=2,sort_keys=True)+'\n')
 x=con['aggregate']
 if x['verdict']=='FOURIER192_WINS':heart='Fourier-192';effect=x['f192_advantage_pct'];fate='GRU resta baseline diagnostica.'
 elif x['verdict']=='GRU_WINS':heart='GRU';effect=x['gru_advantage_pct'];fate='Fourier-192 passa all’archivio di ricerca.'
 else:heart='GRU';effect=abs(100*(x['f192_ppl_geomean']/x['gru_ppl_geomean']-1));fate='PAREGGIO scientifico; GRU è scelta operativa per semplicità ed efficienza, Fourier-192 passa all’archivio di ricerca.'
 ps=prof(r)
 lines=['# FINALE F192 vs GRU — sentenza definitiva','',f'Verdetto scientifico: **{x["verdict"]}**','',
  '## TEST-DEV — decisione congelata','']+table(dev)+['## TEST-CONFIRM — apertura unica','']+table(con)+['## Convergenza','',
  '| Modello | Seed | Epoche | Update | Migliore PPL TUNE | Picco RSS |','|---|---:|---:|---:|---:|---:|']
 for z in runs:lines.append(f"| {z['kind']} | {z['seed']} | {z['epochs']:.1f} | {z['updates']} | {z['best_tune_content_ppl']:.6f} | {z['peak_rss']} |")
 lines+=['','## Costo secondario','', '| Modello | Token/s mediana fra seed | RSS massimo |','|---|---:|---:|']
 for k in ('f192','gru'):
  q=[z for z in ps if z['kind']==k];lines.append(f"| {k} | {statistics.median(z['median_tps'] for z in q):.3f} | {max(z['max_peak_rss'] for z in q)} |")
 if x['verdict']=='PAREGGIO':sentence=f"CUORE LINGUISTICO UFFICIALE: GRU; SU CONFIRM IL VERDETTO SCIENTIFICO È PAREGGIO (SCARTO ASSOLUTO {effect:.3f}%); FOURIER-192 PASSA ALL’ARCHIVIO DI RICERCA PER LA REGOLA PREREGISTRATA DI SEMPLICITÀ ED EFFICIENZA."
 else:sentence=f"CUORE LINGUISTICO UFFICIALE: {heart.upper()}; VANTAGGIO SU CONFIRM {effect:.3f}%; {fate.upper()}"
 lines+=['','## Sentenza','',f'**{sentence}**','']
 rep=r/'FINALE_F192_GRU_REPORT.md';rep.write_text('\n'.join(lines))
 st={'created_utc':now(),'scientific_verdict':x['verdict'],'official_heart':heart,'confirm_effect_pct':effect,'other_fate':fate,'final_sentence':sentence,'report_sha256':sha(rep)}
 (r/'FINAL_STATUS.json').write_text(json.dumps(st,indent=2,sort_keys=True)+'\n');manifest(r,r/'FINAL_SHA256_MANIFEST.json');(r/'PIPELINE_DONE').write_text(sentence+'\n')
 print(json.dumps(st,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
