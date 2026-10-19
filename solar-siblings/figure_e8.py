import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SURF='#fcfcfb'; INK='#0b0b0b'; SEC='#52514e'; GRID='#e7e6e2'
BLUE='#2a78d6'; ORANGE='#eb6834'; AQUA='#1baf7a'; MUTED='#b7b6b0'
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK,
    'axes.edgecolor':SEC,'axes.labelcolor':INK,'xtick.color':SEC,
    'ytick.color':SEC,'axes.facecolor':SURF,'figure.facecolor':SURF})
c = pd.read_csv('/root/ca/e8/e8_candidates.csv', dtype={'source_id':str})
g = c[(c.lane=='GALAH') & c.wmad.notna() & (c.wmad!='')].copy()
g['wmad']=g['wmad'].astype(float)
t1 = g[g.tier=='CANDIDATE']; t2 = g[g.tier=='KINEMATIC-CONSISTENT']; g3 = g[g.tier=='GOLD']
top = g3.nsmallest(10,'wmad')
fig, ax = plt.subplots(figsize=(8.6, 5.0))
ax.scatter(t1.age_gyr, t1.wmad, s=10, c=MUTED, alpha=0.5, label=f'CANDIDATE ({len(t1)})', zorder=2)
ax.scatter(t2.age_gyr, t2.wmad, s=12, c=BLUE, alpha=0.55, label=f'KINEMATIC-CONSISTENT ({len(t2)})', zorder=3)
ax.scatter(g3.age_gyr, g3.wmad, s=26, c=AQUA, label=f'GOLD ({len(g3)})', zorder=4)
ax.scatter(top.age_gyr, top.wmad, s=90, facecolors='none', edgecolors=INK,
           linewidths=1.4, label='top 10 (follow-up shortlist)', zorder=5)
ax.axvline(4.568, color=ORANGE, lw=1.1, ls='--', zorder=1)
ax.text(4.63, 0.157, "Sun's age", color=ORANGE, fontsize=9, rotation=90, va='top')
ax.axhline(0.040, color=SEC, lw=0.9, ls=':', zorder=1)
ax.text(3.12, 0.043, 'GOLD threshold (WMAD = 0.040)', color=SEC, fontsize=8.5)
ax.set_xlabel('[Y/Mg] clock age (Gyr)', fontsize=10.5)
ax.set_ylabel('13-element solar distance WMAD (dex)', fontsize=10.5)
ax.set_xlim(2.9, 6.3); ax.set_ylim(0.01, 0.16)
ax.grid(color=GRID, zorder=0); ax.set_axisbelow(True)
for s in ['top','right']: ax.spines[s].set_visible(False)
ax.legend(frameon=False, fontsize=9, loc='upper right')
ax.set_title('E8 — 221 GOLD solar-sibling candidates from 349,899 GALAH stars',
             fontsize=12, weight='bold')
fig.text(0.5, 0.005,
         'Frozen sieve 28d308e · completeness 5.9% (injection) · expected true siblings in list: 0.02–0.2 · candidates, not detections',
         ha='center', fontsize=8, color=SEC)
plt.tight_layout(rect=[0,0.03,1,1])
plt.savefig('/root/ca/e8/e8-results.png', dpi=160, facecolor=SURF)
print('saved')
