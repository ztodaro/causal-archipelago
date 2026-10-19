"""E2 UNSEAL - the sealed bin, computed once, under the frozen protocol
(E2-SPEC.md a82ea9c + pre-unseal amendments 7e75a61, publicly anchored:
GitHub push 2026-08-30T09:05:35Z, tag pre-unseal-v1, OTS proof committed).

Frozen analysis: selection identical to the corrected calibration build;
primary sample = El-Badry-intersected pairs; decision statistic = median
vtilde_perp in [0.1 a0, a0] / median in [10 a0, 100 a0]; pair-clustered
bootstrap CI (10,000); full own-selection set as labeled variant;
symmetric reporting; small-N contraction clause if sealed pairs < 50.
Newtonian expectation ~ 1.0; MOND-type ~ 1.2."""
import csv, json, sys, numpy as np
sys.path.insert(0,'/root/ca/m3')
from contact_field import load_phase_space
from scipy.spatial import cKDTree
KMS=1.02269
G_SI=6.674e-11; MSUN=1.989e30; AU=1.495978707e11; PC_AU=206264.8; A0=1.2e-10
CSV='/mnt/user-data/uploads/projects/causal-archipelago/m3-pathfinder/data/gaia_100pc_rv.csv'
E2='/mnt/user-data/uploads/projects/causal-archipelago/e2-wide-binaries/data'
sid,pos,vel = load_phase_space(CSV)
g=np.genfromtxt(CSV,delimiter=',',names=True)
MG=g['phot_g_mean_mag']+5*np.log10(g['parallax'])-10
MGs=[];Ms=[]
for line in open(f'{E2}/mamajek_dwarf_table.txt'):
    if line.startswith('#') or not line.strip(): continue
    p=line.split()
    if len(p)<31: continue
    try: mg=float(p[13]); m=float(p[30])
    except ValueError: continue
    MGs.append(mg); Ms.append(m)
MGs=np.array(MGs);Ms=np.array(Ms);o=np.argsort(MGs);MGs,Ms=MGs[o],Ms[o]
u,ui=np.unique(MGs,return_index=True);MGs,Ms=u,Ms[ui]
mass=np.interp(np.clip(MG,MGs.min(),MGs.max()),MGs,Ms)
rverr_ok=g['radial_velocity_error']<1.5
tree=cKDTree(pos)
pairs=tree.query_pairs(0.6,output_type='ndarray')
uv=pos/np.linalg.norm(pos,axis=1)[:,None]
dmean=0.5*(np.linalg.norm(pos[pairs[:,0]],axis=1)+np.linalg.norm(pos[pairs[:,1]],axis=1))
theta=np.arccos(np.clip(np.sum(uv[pairs[:,0]]*uv[pairs[:,1]],axis=1),-1,1))
dx=theta*dmean*PC_AU
keep=(dx>500)&(dx<30000); pairs,dx,dmean=pairs[keep],dx[keep],dmean[keep]
d1=np.linalg.norm(pos[pairs[:,0]],axis=1);d2=np.linalg.norm(pos[pairs[:,1]],axis=1)
keep=np.abs(d1-d2)<0.5; pairs,dx,dmean=pairs[keep],dx[keep],dmean[keep]
Mtot=mass[pairs[:,0]]+mass[pairs[:,1]]
vcirc=np.sqrt(G_SI*Mtot*MSUN/(dx*AU))/1000.0
dv3d=np.linalg.norm(vel[pairs[:,0]]-vel[pairs[:,1]],axis=1)/KMS
keep=(dv3d<2*vcirc)&rverr_ok[pairs[:,0]]&rverr_ok[pairs[:,1]]
pairs,dx,dmean,Mtot,vcirc=pairs[keep],dx[keep],dmean[keep],Mtot[keep],vcirc[keep]
r10k=10000/PC_AU
neigh=tree.query_ball_point(pos,r10k)
third=np.zeros(len(pairs),bool)
for k,(a,b) in enumerate(pairs):
    if (set(neigh[a])-{a,b}) or (set(neigh[b])-{a,b}): third[k]=True
pairs,dx,dmean,Mtot,vcirc=pairs[~third],dx[~third],dmean[~third],Mtot[~third],vcirc[~third]
gN=G_SI*Mtot*MSUN/(dx*AU)**2
dmu=np.hypot(g['pmra'][pairs[:,0]]-g['pmra'][pairs[:,1]],g['pmdec'][pairs[:,0]]-g['pmdec'][pairs[:,1]])
vtp=(4.740470446e-3*dmu*dmean)/vcirc
eb=set()
for r in csv.DictReader(open(f'{E2}/elbadry_nearby.csv')):
    eb.add(frozenset((r['source_id1'].strip(),r['source_id2'].strip())))
in_eb=np.array([frozenset((str(int(sid[a])),str(int(sid[b])))) in eb for a,b in pairs])
sealed = gN < 10*A0
print(f"total pairs {len(pairs)}; SEALED region pairs: {int(sealed.sum())} "
      f"(El-Badry-intersected: {int((sealed&in_eb).sum())})", flush=True)
def analyze(mask,label):
    hi=(gN>10*A0)&(gN<100*A0)&mask
    lo=(gN>0.1*A0)&(gN<A0)&mask
    n_hi,n_lo=int(hi.sum()),int(lo.sum())
    out=dict(label=label,n_high=n_hi,n_low=n_lo)
    if n_lo<5 or n_hi<5:
        out['status']='insufficient-bins'; return out
    ratio=float(np.median(vtp[lo])/np.median(vtp[hi]))
    rng=np.random.default_rng(99); rs=[]
    ilo,ihi=np.where(lo)[0],np.where(hi)[0]
    for _ in range(10000):
        a=vtp[rng.choice(ilo,n_lo)]; b=vtp[rng.choice(ihi,n_hi)]
        rs.append(np.median(a)/np.median(b))
    lo95,hi95=np.percentile(rs,[2.5,97.5])
    out.update(median_high=round(float(np.median(vtp[hi])),3),
        median_low=round(float(np.median(vtp[lo])),3),
        RATIO=round(ratio,3), CI95=[round(float(lo95),3),round(float(hi95),3)])
    return out
res=dict(sealed_total=int(sealed.sum()),
    sealed_elbadry=int((sealed&in_eb).sum()),
    contraction_clause_triggered=bool(sealed.sum()<50),
    primary=analyze(in_eb,'El-Badry-intersected (PRIMARY)'),
    variant=analyze(np.ones(len(pairs),bool),'full own-selection (variant)'))
# profile for the figure
bins=np.array([0.1,0.3,1,3,10,30,100])*A0
prof=[]
for i in range(len(bins)-1):
    m=(gN>=bins[i])&(gN<bins[i+1])
    for lab,mm in (('primary',m&in_eb),('variant',m)):
        if mm.sum()>=3:
            prof.append(dict(bin_lo_a0=round(bins[i]/A0,2),bin_hi_a0=round(bins[i+1]/A0,2),
                subset=lab,n=int(mm.sum()),med=round(float(np.median(vtp[mm])),3)))
res['profile']=prof
json.dump(res,open('/root/ca/m3/e2_UNSEALED.json','w'),indent=1)
np.savez_compressed('/root/ca/m3/e2_unsealed_pairs.npz',pairs=pairs,gN=gN,vtp=vtp,in_eb=in_eb,dx=dx)
print(json.dumps({k:v for k,v in res.items() if k!='profile'},indent=1))
print("UNSEALED")
