import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SURF='#fcfcfb'; INK='#0b0b0b'; SEC='#52514e'; GRID='#e7e6e2'
BLUE='#2a78d6'; ORANGE='#eb6834'; AQUA='#1baf7a'; MUTED='#b7b6b0'
r = json.load(open('/root/ca/e2b/e2b_UNSEALED.json'))
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK,
    'axes.edgecolor':SEC,'axes.labelcolor':INK,'xtick.color':SEC,
    'ytick.color':SEC,'axes.facecolor':SURF,'figure.facecolor':SURF})
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.4),
                               gridspec_kw={'width_ratios': [1.15, 1]})

# ---- left: decision statistics vs anchors ----
rows = [('PRIMARY\n(n=1,377)', r['PRIMARY'], r['anchors']['primary']),
        ('R<0.1 variant\n(n=1,395)', r['variant_R01'], r['anchors']['primary']),
        ('precision-trimmed\n(n=506)', r['variant_trim'], r['anchors']['trim'])]
y = np.arange(len(rows))[::-1]
for yy, (lab, d, anch) in zip(y, rows):
    nlo, nhi = anch['newton'][1], anch['newton'][2]
    mlo, mhi = anch['mond'][1], anch['mond'][2]
    ax1.barh(yy, nhi-nlo, left=nlo, height=0.62, color=BLUE, alpha=0.16, zorder=1)
    ax1.barh(yy, mhi-mlo, left=mlo, height=0.62, color=ORANGE, alpha=0.16, zorder=1)
    ax1.plot([anch['newton'][0]]*2, [yy-0.31, yy+0.31], color=BLUE, lw=1.2, zorder=2)
    ax1.plot([anch['mond'][0]]*2, [yy-0.31, yy+0.31], color=ORANGE, lw=1.2, zorder=2)
    lo95, hi95 = d['CI95']
    ax1.plot([lo95, hi95], [yy, yy], color=INK, lw=2.4, zorder=4,
             solid_capstyle='butt')
    ax1.plot(d['RATIO'], yy, 'o', color=INK, ms=7, zorder=5)
ax1.set_yticks(y)
ax1.set_yticklabels([t[0] for t in rows], fontsize=9.5)
ax1.set_xlim(0.90, 1.42)
ax1.set_xlabel('median ṽ ratio  [0.1–1]a₀ / [10–100]a₀', fontsize=10)
ax1.grid(axis='x', color=GRID, zorder=0); ax1.set_axisbelow(True)
for s in ['top', 'right']: ax1.spines[s].set_visible(False)
ax1.set_ylim(-0.55, 3.25)
ax1.text(1.115, 2.52, 'Newton\n(noise-adj.)', color=BLUE,
         ha='center', va='bottom', fontsize=8.5, weight='bold')
ax1.text(1.299, 2.52, 'MOND\n(noise-adj.)', color=ORANGE,
         ha='center', va='bottom', fontsize=8.5, weight='bold')
ax1.set_title('Sealed measurements vs preregistered anchors', fontsize=11, weight='bold')

# ---- right: acceleration profile ----
prof = r['profile']
xc = [np.sqrt(p['bin_lo_a0']*p['bin_hi_a0']) for p in prof]
med = [p['med'] for p in prof]
ns = [p['n'] for p in prof]
ax2.axvspan(0.09, 10, color=ORANGE, alpha=0.06, zorder=0)
ax2.plot(xc, med, 'o-', color=INK, lw=1.4, ms=6, zorder=4)
ax2.axhline(0.582, color=BLUE, lw=1.1, ls='--', zorder=2)
ax2.text(0.12, 0.560, 'high-acceleration baseline 0.582', color=BLUE, fontsize=8.5)
for x_, m_, n_ in zip(xc, med, ns):
    ax2.text(x_, m_+0.022, f'{n_:,}', ha='center', fontsize=7.5, color=SEC)
ax2.set_xscale('log')
ax2.set_xlim(0.09, 120); ax2.set_ylim(0.45, 0.85)
ax2.set_xlabel('Newtonian internal acceleration g_N (a₀)', fontsize=10)
ax2.set_ylabel('median ṽ_perp', fontsize=10)
ax2.grid(color=GRID, zorder=0); ax2.set_axisbelow(True)
for s in ['top', 'right']: ax2.spines[s].set_visible(False)
ax2.text(1.0, 0.815, 'sealed region\n(opened once)', color=SEC, fontsize=8.5, ha='center')
ax2.set_title('ṽ profile across the MOND regime', fontsize=11, weight='bold')

fig.suptitle('E2b unsealed — Newtonian; MOND-scale boost excluded in all four preregistered statistics',
             fontsize=12, color=INK, weight='bold', y=0.99)
fig.text(0.5, 0.005,
         'PRIMARY 1.104 [1.063, 1.164] vs Newton 1.115 / MOND 1.299 · flicker bin 0.699 [0.640, 0.733] vs 0.682 / 0.788 · anchored: tag pre-unseal-e2b, GitHub 10:10:44Z, OTS',
         ha='center', fontsize=8, color=SEC)
plt.tight_layout(rect=[0, 0.03, 1, 0.93])
plt.savefig('/root/ca/e2b/e2b-unsealed.png', dpi=160, facecolor=SURF)
print('saved')
