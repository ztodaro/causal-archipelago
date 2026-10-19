import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SURF='#fcfcfb'; INK='#0b0b0b'; SEC='#52514e'; GRID='#e7e6e2'
BLUE='#2a78d6'; ORANGE='#eb6834'; AQUA='#1baf7a'; MUTED='#b7b6b0'
r = json.load(open('/root/ca/m3/e1b_results.json'))
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK,
    'axes.edgecolor':SEC,'axes.labelcolor':INK,'xtick.color':SEC,
    'ytick.color':SEC,'axes.facecolor':SURF,'figure.facecolor':SURF})
fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.2))
for ax, name, color in zip(axes, ['GALAH', 'APOGEE'], [BLUE, ORANGE]):
    d = r[name]
    x = [0, 1]
    vals = [d['med_treat'], d['med_control']]
    ax.bar(x, vals, width=0.55, color=[color, MUTED], zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(['co-natal pairs\n(claimed siblings)', 'matched controls\n(look-alike strangers)'], fontsize=9)
    ax.set_ylim(0, 0.24)
    ax.grid(axis='y', color=GRID, zorder=0)
    ax.set_axisbelow(True)
    for s in ['top', 'right']:
        ax.spines[s].set_visible(False)
    ax.set_title(f"{name}", fontsize=12, color=INK, weight='bold')
    ax.text(0, vals[0]+0.006, f"{vals[0]:.3f}", ha='center', fontsize=10, color=INK)
    ax.text(1, vals[1]+0.006, f"{vals[1]:.3f}", ha='center', fontsize=10, color=SEC)
    lo, hi = d['boot_CI']
    ax.text(0.5, 0.215,
            f"Δ = {d['med_diff']:.3f} dex  CI [{lo:.3f}, {hi:.3f}]\n"
            f"{d['treat']:,} pairs · {d['clusters']:,} clusters · CONFIRMED",
            ha='center', fontsize=9, color=AQUA if d['CONFIRMED'] else SEC, weight='bold')
axes[0].set_ylabel('median |Δ[Fe/H]| within pair (dex)', fontsize=10)
fig.suptitle('E1b — chemical genealogy at kiloparsec scale: claimed siblings are twice as chemically alike',
             fontsize=11.5, color=INK, y=0.98)
fig.text(0.5, 0.005, 'Controls matched on Teff, log g, separation, distance; star-clustered bootstrap; spec frozen ec12d01 before data',
         ha='center', fontsize=8, color=SEC)
plt.tight_layout(rect=[0, 0.03, 1, 0.93])
plt.savefig('/root/ca/m3/e1b-results.png', dpi=160, facecolor=SURF)
print('saved')
