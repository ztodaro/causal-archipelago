"""E10b figure: conatal fraction vs age (decision bins + descriptive bins + parametric curve)."""
import json, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
BG,FG,MUTED,GRID,BLUE,ORANGE,GREEN,GREY='#fcfcfb','#0b0b0b','#52514e','#e7e6e2','#2a78d6','#eb6834','#1baf7a','#b7b6b0'
R=json.load(open('/root/ca/fresh/e10b/e10b_results.json'))
fig,ax=plt.subplots(figsize=(8.2,4.6),facecolor=BG); ax.set_facecolor(BG)
# descriptive four bins
b4=R['descriptive_bins']; f4=R['f_4bin']; c4=R['f_4bin_CI']
for (lo,hi),f,(cl,ch) in zip(b4,f4,c4):
    ax.fill_between([lo,hi],[cl,cl],[ch,ch],color=GRID,alpha=0.8,lw=0)
    ax.plot([lo,hi],[f,f],color=GREY,lw=1.5)
# decision two bins
b2=[tuple(x) for x in R['decision_bins']]; b4=[tuple(x) for x in b4]
for (lo,hi),f,(cl,ch),col in zip(b2,[R['f_young'],R['f_old']],[R['f_young_CI'],R['f_old_CI']],[BLUE,ORANGE]):
    ax.errorbar([(lo+hi)/2],[f],yerr=[[f-cl],[ch-f]],fmt='o',color=col,capsize=4,ms=8,lw=2,zorder=5)
    ax.annotate(f"f = {f:.2f} [{cl:.2f}, {ch:.2f}]\nn(mass>0.5) = {R['pairs_mass_gt_half_decision'][b2.index((lo,hi))]}",((lo+hi)/2,f),textcoords='offset points',xytext=(10,12),fontsize=8,color=col)
t=np.linspace(0,14,200); ax.plot(t,R['param_f0']*np.exp(-t/R['param_tau_gyr']),color=GREEN,lw=1.5,ls='--',label=f"f0·exp(−t/τ), τ = {R['param_tau_gyr']:.1f} Gyr [{R['param_tau_CI'][0]:.1f}, {R['param_tau_CI'][1]:.1f}]")
ax.axhline(R['oracle1']['f_const'],color=GREY,lw=1,ls=':',label=f"constant-f fit = {R['oracle1']['f_const']:.2f}")
ax.set_xlim(0,14); ax.set_ylim(0,1); ax.set_xlabel('pair age from the [Y/Mg] clock (Gyr); median error %.1f Gyr'%R['median_age_err'],fontsize=9,color=FG)
ax.set_ylabel('conatal fraction f (lower bound; orbit-matched template)',fontsize=9,color=FG)
ax.set_title(f"E10b — conatal fraction of comoving pairs vs age: verdict {R['verdict']} (R = f_old/f_young = {R['ratio_old_young']:.2f}, bootstrap interval degenerate)",fontsize=9.5,color=FG,loc='left')
for s in ax.spines.values(): s.set_color(GRID)
ax.tick_params(colors=MUTED,labelsize=8); ax.grid(color=GRID,lw=0.6); ax.legend(fontsize=8,frameon=False,loc='upper right')
fig.text(0.01,0.005,'Grey: four descriptive bins with 95%% CIs. Points: two decision bins. Mixture of half-normal (conatal) and orbit-matched empirical chance template; age error marginalised per pair. GALAH, %d pairs.'%R['n_pairs_with_clocks'],fontsize=7.5,color=MUTED)
plt.tight_layout(rect=[0,0.03,1,1]); plt.savefig('/root/ca/fresh/e10b/e10b-results.png',dpi=160,facecolor=BG); print('figure written')
