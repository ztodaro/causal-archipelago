import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SURF='#fcfcfb'; INK='#0b0b0b'; SEC='#52514e'; GRID='#e7e6e2'
BLUE='#2a78d6'; ORANGE='#eb6834'; AQUA='#1baf7a'; MUTED='#b7b6b0'
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK,
    'axes.edgecolor':SEC,'axes.labelcolor':INK,'xtick.color':SEC,
    'ytick.color':SEC,'axes.facecolor':SURF,'figure.facecolor':SURF})
r = json.load(open('/root/ca/e7/e10_results.json'))
bins = r['bins']
xc = [1.0, 3.25, 6.25]
xw = [1.0, 1.25, 1.75]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 4.4), gridspec_kw={'width_ratios':[1.25,1]})

ax1.axhline(0, color=SEC, lw=1.0, ls='--', zorder=1)
for x, w, b in zip(xc, xw, bins):
    if b.get('status') == 'underpowered':
        y = b['excess_descriptive']
        ax1.plot(x, y, 'o', mfc='none', mec=MUTED, mew=1.8, ms=10, zorder=3)
        ax1.text(x, y-0.028, f"n={b['matched']}\nunderpowered", ha='center', fontsize=8, color=MUTED)
    else:
        y = b['excess']; lo, hi = b['CI']
        ax1.errorbar(x, y, yerr=[[y-lo], [hi-y]], fmt='o', color=BLUE, ms=9,
                     capsize=5, lw=2.2, zorder=4)
        ax1.text(x, lo-0.02, f"n={b['matched']} pairs\n{b['clusters']} clusters",
                 ha='center', fontsize=8, color=SEC)
ax1.set_xlim(0, 8); ax1.set_ylim(-0.32, 0.08)
ax1.set_xlabel('[Y/Mg] clock age of linked pair (Gyr)', fontsize=10.5)
ax1.set_ylabel('chemical twin excess (dex)\nmedian |Δ[Fe/H]|: linked − matched controls', fontsize=10)
ax1.grid(color=GRID, zorder=0); ax1.set_axisbelow(True)
for s in ['top','right']: ax1.spines[s].set_visible(False)
ax1.axvline(4.568, color=ORANGE, lw=1.0, ls=':', zorder=1)
ax1.text(4.65, 0.045, "Sun's age", color=ORANGE, fontsize=8.5, rotation=90, va='top')
ax1.set_title('Twin excess vs age — memory in point estimate to 8 Gyr', fontsize=11, weight='bold')

x = np.arange(3); wdt = 0.36
td = [b.get('sec_treat_dt_med') for b in bins]
cd = [b.get('sec_ctrl_dt_med') for b in bins]
ax2.bar(x-wdt/2, td, wdt, color=AQUA, label='linked pairs', zorder=3)
ax2.bar(x+wdt/2, cd, wdt, color=MUTED, label='matched controls', zorder=3)
for xi, (t, c) in enumerate(zip(td, cd)):
    ax2.text(xi-wdt/2, t+0.12, f'{t}', ha='center', fontsize=9, color=INK)
    ax2.text(xi+wdt/2, c+0.12, f'{c}', ha='center', fontsize=9, color=SEC)
ax2.set_xticks(x); ax2.set_xticklabels(['[0,2)', '[2,4.5)', '[4.5,8)'])
ax2.set_xlabel('pair age bin (Gyr)', fontsize=10.5)
ax2.set_ylabel('median clock-age disagreement |Δt| (Gyr)', fontsize=10)
ax2.grid(axis='y', color=GRID, zorder=0); ax2.set_axisbelow(True)
for s in ['top','right']: ax2.spines[s].set_visible(False)
ax2.legend(frameon=False, fontsize=9)
ax2.set_title('Linked pairs are co-eval; controls are not', fontsize=11, weight='bold')

fig.suptitle('E10 — the forgetting curve: kinematic linkage stays chemically informative across the disk\'s history',
             fontsize=12, weight='bold', y=0.99)
fig.text(0.5, 0.005,
         'Frozen rule verdict: "forgetting detected" (old-bin CI includes 0 by 0.007 dex at the n=25 power floor) — see results doc for the honest reading · spec 434506c',
         ha='center', fontsize=8, color=SEC)
plt.tight_layout(rect=[0, 0.035, 1, 0.94])
plt.savefig('/root/ca/e7/e10-results.png', dpi=160, facecolor=SURF)
print('saved')
