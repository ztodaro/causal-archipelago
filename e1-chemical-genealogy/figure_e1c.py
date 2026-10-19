"""E1c figure: twin excess vs control tier, both surveys. House palette."""
import json, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
BG,FG,MUTED,GRID,BLUE,ORANGE,GREEN,GREY='#fcfcfb','#0b0b0b','#52514e','#e7e6e2','#2a78d6','#eb6834','#1baf7a','#b7b6b0'
R=json.load(open('/root/ca/fresh/e1c/e1c_results.json'))
tiers=['C0','C1','C2','C3','C4']
labels=['E1b control\n(near, dv>6)','far,\norbit-free','+ Lz','+ Jz','+ Jr\n(full orbit)']
fig,axes=plt.subplots(1,2,figsize=(10.5,4.4),facecolor=BG)
for ax,(name,col) in zip(axes,[('GALAH',BLUE),('APOGEE',ORANGE)]):
    ax.set_facecolor(BG)
    sv=R['surveys'].get(name,{})
    xs=[];ys=[];lo=[];hi=[]
    for i,t in enumerate(tiers):
        r=sv.get(t)
        if not r or 'med_diff' not in r: continue
        xs.append(i); ys.append(r['med_diff']); lo.append(r['boot_CI'][0]); hi.append(r['boot_CI'][1])
    xs=np.array(xs);ys=np.array(ys);lo=np.array(lo);hi=np.array(hi)
    ax.axhline(0,color=GREY,lw=1)
    ref=sv.get('C0',{}).get('med_diff')
    if ref is not None: ax.axhspan(*[v for v in json.load(open('/root/ca/m3/e1b_results.json'))[name]['boot_CI']],color=GRID,alpha=0.9,lw=0,label='E1b 95% CI')
    ax.errorbar(xs,ys,yerr=[ys-lo,hi-ys],fmt='o',color=col,ecolor=col,capsize=3,lw=1.5,ms=6)
    for x,y,r in zip(xs,ys,[sv[t] for t in tiers if t in sv and 'med_diff' in sv[t]]):
        ax.annotate(f"{y:+.3f}\nn={r['treat']}",(x,y),textcoords='offset points',xytext=(8,-4),fontsize=7.5,color=MUTED)
    ax.set_xticks(range(len(tiers))); ax.set_xticklabels(labels,fontsize=8,color=FG)
    ax.set_ylim(-0.14,0.02); ax.set_ylabel('median |Δ[Fe/H]|, treatment − control (dex)',fontsize=8.5,color=FG)
    v=sv.get('verdict','?'); ax.set_title(f"{name} — C4 verdict: {v}",fontsize=10,color=FG,loc='left')
    for s in ax.spines.values(): s.set_color(GRID)
    ax.tick_params(colors=MUTED,labelsize=8); ax.grid(axis='y',color=GRID,lw=0.6)
    ax.legend(fontsize=7.5,frameon=False,loc='lower left')
fig.suptitle('E1c: how much of the comoving-pair twin excess survives orbit-matched controls (S_min = 300 pc)',fontsize=10.5,color=FG,x=0.01,ha='left')
fig.text(0.01,0.005,'Same treatment pairs as E1b; controls matched on Teff/log g/distance at every tier; orbit tolerances = 90th pct of treatment pairs’ own |ΔJ|. Bars: star-clustered bootstrap 95% CI.',fontsize=7.5,color=MUTED)
plt.tight_layout(rect=[0,0.03,1,0.95]); plt.savefig('/root/ca/fresh/e1c/e1c-results.png',dpi=160,facecolor=BG)
print('figure written')
