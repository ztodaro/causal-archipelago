"""Predict line-of-sight velocities using external anchors only."""
from pathlib import Path
import numpy as np,pandas as pd,json,hashlib
from astropy.coordinates import SkyCoord
import astropy.units as u
P=Path(__file__).resolve().parent;R=P.parents[1]
d=pd.read_csv(P/'r3-starting-evidence.csv',dtype={'source_id':str})
g=pd.read_csv(R/'m3-pathfinder/vetting/data/gaia_dr3_candidate_vetting.csv',dtype={'source_id':str}).set_index('source_id')
f=pd.read_csv(R/'m3-pathfinder/data/gaia_100pc_rv.csv',dtype={'source_id':str}).set_index('source_id')
m=pd.read_csv(R/'m3-pathfinder/vetting/data/catalog-updates/raw/moranta_table1.csv',dtype={'Gaia':str})
a=m.loc[m.Crius==227,'Gaia'];a=a[a.isin(f.index)&~a.isin(d.source_id)];af=f.loc[a]
def coord(df,rv=True):
    return SkyCoord(ra=df.ra.to_numpy()*u.deg,dec=df.dec.to_numpy()*u.deg,distance=1000/df.parallax.to_numpy()*u.pc,pm_ra_cosdec=df.pmra.to_numpy()*u.mas/u.yr,pm_dec=df.pmdec.to_numpy()*u.mas/u.yr,radial_velocity=(df.radial_velocity.to_numpy() if rv else np.zeros(len(df)))*u.km/u.s).galactic
v=coord(af).velocity.d_xyz.to_value(u.km/u.s).T;centroid=v.mean(axis=0);cov=np.cov(v.T,ddof=1)
df=g.loc[d.source_id];c=coord(df,False);n=c.cartesian.xyz.to_value(u.pc).T;n=n/np.linalg.norm(n,axis=1)[:,None]
pred=n@centroid;disp=np.sqrt(np.einsum('ij,jk,ik->i',n,cov,n));tan=c.velocity.d_xyz.to_value(u.km/u.s).T
out=d[['source_id','group','cls','dv_external_kms']].copy();out['predicted_rv']=pred;out['anchor_los_scatter']=disp;out['centroid_rv_standard_error']=disp/np.sqrt(len(a));out['rv_free_tangential_residual_kms']=np.linalg.norm(tan-(centroid-pred[:,None]*n),axis=1)
for col in ['ra','dec','parallax','bp_rp','ruwe','radial_velocity','radial_velocity_error']:out[col]=df[col].to_numpy()
i=pd.read_csv(P/'simbad/identity.csv');i['source_id']=i.id.str.replace('Gaia DR3 ','',regex=False);out=out.merge(i[['source_id','main_id']],on='source_id',how='left')
archive=pd.read_csv(R/'notes/next-cycle/candidate-spectra.csv',dtype={'source_id':str});archive=archive[(archive.group=='R3')&archive.rv_valid].copy();archive['origin']='primary_archival_field'
fallback=pd.read_csv(R/'notes/next-cycle/candidate-archive-field-audit.csv',dtype={'source_id':str});fallback=fallback[fallback.source_id.isin(d.source_id)&fallback.fallback_column.notna()]
for _,row in fallback.iterrows():
    if not np.isfinite(row.adopted_rv):continue
    archive=pd.concat([archive,pd.DataFrame([{'source_id':row.source_id,'survey':'LAMOST MRS','rv':row.adopted_rv,'adopted_rv_error':max(2,row.adopted_error),'origin':'fallback_'+row.fallback_column}])],ignore_index=True)
z=archive.merge(out[['source_id','main_id','predicted_rv','anchor_los_scatter','centroid_rv_standard_error']],on='source_id')
z['residual_to_external']=z.rv-z.predicted_rv
# This is a diagnostic standardized residual, not a membership likelihood.
z['diagnostic_z']=z.residual_to_external/np.sqrt(z.adopted_rv_error**2+z.anchor_los_scatter**2+z.centroid_rv_standard_error**2)
out.to_csv(P/'r3-predictions.csv',index=False);z.to_csv(P/'r3-independent-rv.csv',index=False)
(P/'r3-prediction-provenance.json').write_text(json.dumps({'anchor_ids':a.tolist(),'n_anchors':len(a),'mean_uvw_kms':centroid.tolist(),'covariance_uvw':cov.tolist(),'no_candidate_rv_in_prediction':True,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'caveat':'External group is not an independently age-confirmed training set; no calibrated membership probability.'},indent=2),encoding='utf-8')
print(out.to_string(index=False,columns=['source_id','main_id','dv_external_kms','rv_free_tangential_residual_kms','predicted_rv']))
print(z.to_string(index=False,columns=['source_id','survey','rv','predicted_rv','residual_to_external','diagnostic_z']))
