"""B2 - expected DR4 astrometric retention of the E8 GOLD list, per frozen B2-B4-SPEC.md."""
import csv, json, hashlib, numpy as np
SELF_SHA=hashlib.sha256(open(__file__,'rb').read()).hexdigest()
CAND='/root/ca/e8/e8_candidates.csv'; ABUND='/root/ca/e8/e8_galah_abund.csv'; OUT='/root/ca/fresh/dr4'
# frozen E8 constants (e8_sieve.py)
R0=8.2; VC=233.1; USUN,VSUN,WSUN=11.1,12.24,7.25; LZ_SUN=R0*(VC+VSUN); NU=73.5; KAP=40.2
LZ_WIN,JZ_MAX,JR_MAX=500.0,25.0,20.0; KAPPA_PM=4.740470446e-3
AG=np.array([[-0.0548755604162154,-0.8734370902348850,-0.4838350155487132],
             [ 0.4941094278755837,-0.4448296299600112, 0.7469822444972189],
             [-0.8676661490190047,-0.1980763734312015, 0.4559837761750669]])
def phase_space(ra,dec,plx,pmra,pmdec,rv):
    ra_r,dec_r=np.radians(ra),np.radians(dec); dist=1000.0/plx
    ca,sa,cd,sd=np.cos(ra_r),np.sin(ra_r),np.cos(dec_r),np.sin(dec_r)
    rhat=np.column_stack([cd*ca,cd*sa,sd]); phat=np.column_stack([-sa,ca,np.zeros_like(sa)]); qhat=np.column_stack([-sd*ca,-sd*sa,cd])
    pos=(rhat*dist[:,None])@AG.T
    v=(rv[:,None]*rhat+(1000*KAPPA_PM*pmra/plx)[:,None]*phat+(1000*KAPPA_PM*pmdec/plx)[:,None]*qhat)
    return pos,v@AG.T
def actions(pos,vel):
    x,y,z=pos[:,0],pos[:,1],pos[:,2]
    d=np.column_stack([x-R0*1000,y]); R=np.hypot(d[:,0],d[:,1])/1000.0
    eR=np.column_stack([d[:,0],d[:,1]])/(R[:,None]*1000); ephi=np.column_stack([eR[:,1],-eR[:,0]])
    vtot=vel+np.array([USUN,VSUN+VC,WSUN])
    vR=vtot[:,0]*eR[:,0]+vtot[:,1]*eR[:,1]; vphi=vtot[:,0]*ephi[:,0]+vtot[:,1]*ephi[:,1]
    Lz=R*vphi; Rg=Lz/VC
    return Lz,0.5*(vR**2+KAP**2*(Rg-R)**2)/KAP,0.5*(vtot[:,2]**2+NU**2*(z/1000.0)**2)/NU
def inside(Lz,Jr,Jz): return (np.abs(Lz-LZ_SUN)<=LZ_WIN)&(Jz<=JZ_MAX)&(Jr<=JR_MAX)
# Amendment 1 (2026-09-01): join on the GALAH observation id (survey_id == sobject_id), not gaiadr3_source_id —
# 20 GOLD rows carry an empty gaiadr3_source_id (E8-RESULTS robustness note) and the id-join silently mapped them to one wrong star.
gold=[(r['survey_id'].strip(),r['source_id'].strip()) for r in csv.DictReader(open(CAND)) if r['tier'].strip()=='GOLD']
gold_obs={g[0] for g in gold}; print("GOLD rows:",len(gold),"empty gaiadr3 ids:",sum(1 for g in gold if g[1]==''))
astro={}
for r in csv.DictReader(open(ABUND)):
    ob=r['sobject_id'].strip()
    if ob not in gold_obs or ob in astro: continue
    try: astro[ob]=[float(r[k]) for k in ('ra','dec','parallax','parallax_error','pmra','pmdec','rv_galah','e_rv_galah')]
    except ValueError: continue
ids=[g[0] for g in gold if g[0] in astro]; A=np.array([astro[s] for s in ids]); print("with astrometry:",len(ids))
ra,dec,plx,eplx,pmra,pmdec,rv,erv=A.T
pos,vel=phase_space(ra,dec,plx,pmra,pmdec,rv); Lz0,Jr0,Jz0=actions(pos,vel); in0=inside(Lz0,Jr0,Jz0)
print("inside window at DR3 point values:",int(in0.sum()),"of",len(ids))
rng=np.random.default_rng(20261202); N=4000
SC_PLX,SC_PM=(34/66)**0.5,(34/66)**1.5
def retention(pm_factor,dr4=True):
    epm=eplx*pm_factor
    ret=np.zeros(len(ids))
    for i in range(len(ids)):
        tp=rng.normal(plx[i],eplx[i],N); ta=rng.normal(pmra[i],epm[i],N); td=rng.normal(pmdec[i],epm[i],N); tr=rng.normal(rv[i],erv[i],N)
        if dr4: mp=tp+rng.normal(0,SC_PLX*eplx[i],N); ma=ta+rng.normal(0,SC_PM*epm[i],N); md=td+rng.normal(0,SC_PM*epm[i],N); mr=tr
        else:   mp=tp+rng.normal(0,eplx[i],N); ma=ta+rng.normal(0,epm[i],N); md=td+rng.normal(0,epm[i],N); mr=tr+rng.normal(0,erv[i],N)
        p,v=phase_space(np.full(N,ra[i]),np.full(N,dec[i]),mp,ma,md,mr); L,Jr,Jz=actions(p,v); ret[i]=inside(L,Jr,Jz).mean()
    return ret
def pb_interval(ret,n=20000):
    s=(rng.random((n,len(ret)))<ret).sum(axis=1); return [int(np.percentile(s,2.5)),int(np.percentile(s,97.5))]
res=dict(script_sha256=SELF_SHA,amendment="A1: join on sobject_id",n_gold=len(gold),n_with_astrometry=len(ids),inside_at_DR3_point=int(in0.sum()),
         dr4_scaling=dict(parallax=round(SC_PLX,3),pm=round(SC_PM,3),rv='unchanged (GALAH)'),
         median_errors=dict(parallax_mas=round(float(np.median(eplx)),4),rv_kms=round(float(np.median(erv)),3)))
for label,pmf,dr4 in (('DR4_pm1x',1.0,True),('DR4_pm2x',2.0,True),('DR3_remeasure_pm1x',1.0,False)):
    ret=retention(pmf,dr4)
    res[label]=dict(mean_retention=round(float(ret.mean()),4),expected_survivors=round(float(ret.sum()),2),
                    interval_95=pb_interval(ret),n_below_0p5=int((ret<0.5).sum()),n_below_0p9=int((ret<0.9).sum()),
                    marginal_ids=[ids[i] for i in np.where(ret<0.5)[0]])
    print(label,res[label],flush=True)
json.dump(res,open(f'{OUT}/b2_retention.json','w'),indent=1); print("DONE")
