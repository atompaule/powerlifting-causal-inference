import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import matplotlib
matplotlib.use("Agg")

df = pd.read_csv("data/openpowerlifting-2026-05-16-d230fa1a.csv", low_memory=False)

# ── Style ─────────────────────────────────────────────────────────────────────
sns.set_theme(style="darkgrid", palette="muted")
plt.rcParams.update({"figure.facecolor": "#1c1c1e", "axes.facecolor": "#2c2c2e",
                     "axes.labelcolor": "white", "xtick.color": "white",
                     "ytick.color": "white", "text.color": "white",
                     "axes.titlecolor": "white", "grid.color": "#3c3c3e",
                     "axes.edgecolor": "#3c3c3e", "legend.facecolor": "#2c2c2e",
                     "legend.edgecolor": "#3c3c3e"})
ACCENT = ["#FF6B6B", "#4ECDC4", "#FFE66D", "#A29BFE", "#74B9FF", "#55EFC4", "#FD79A8", "#FDCB6E"]

fig = plt.figure(figsize=(22, 28))
fig.patch.set_facecolor("#1c1c1e")
fig.suptitle("OpenPowerlifting — Supplementary EDA (Previously Uncovered Variables)",
             fontsize=20, fontweight="bold", color="white", y=0.99)
gs = fig.add_gridspec(4, 3, hspace=0.48, wspace=0.35)

# ── 1. Finishing place distribution ──────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, :2])
place_order = [str(i) for i in range(1, 16)] + ["DQ", "NS"]
place_counts = df["Place"].value_counts()
vals = [place_counts.get(p, 0) for p in place_order]
colors_place = [ACCENT[1] if p not in ("DQ", "NS") else ACCENT[0] for p in place_order]
bars = ax1.bar(place_order, vals, color=colors_place, edgecolor="none")
ax1.set_title("Finishing Place Distribution  (DQ = disqualified, NS = no show)", fontsize=13, fontweight="bold")
ax1.set_xlabel("Place"); ax1.set_ylabel("# Entries")
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x/1e6):.1f}M" if x >= 1e6 else f"{int(x/1e3)}K"))
for bar, val in zip(bars, vals):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5000,
             f"{val:,}", ha="center", fontsize=7.5, color="white", rotation=45)
pct_dq = place_counts.get("DQ", 0) / len(df) * 100
ax1.annotate(f"DQ rate: {pct_dq:.1f}%", xy=(14.5, place_counts.get("DQ", 0)),
             xytext=(12, place_counts.get("1", 0) * 0.7),
             arrowprops=dict(arrowstyle="->", color=ACCENT[0]), color=ACCENT[0], fontsize=10)

# ── 2. Parent federation breakdown ───────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 2])
pf = df["ParentFederation"].value_counts().head(10)
wedges, texts, autotexts = ax2.pie(pf, labels=pf.index, autopct="%1.1f%%",
    colors=ACCENT[:len(pf)], startangle=140,
    textprops={"color": "white", "fontsize": 8}, pctdistance=0.75)
for at in autotexts: at.set_fontsize(7.5)
ax2.set_title("Parent Federation Share\n(top 10)", fontsize=13, fontweight="bold")

# ── 3. Top weight classes ─────────────────────────────────────────────────────
ax3 = fig.add_subplot(gs[1, 0])
wc = df["WeightClassKg"].value_counts().head(16)
ax3.barh(wc.index[::-1].astype(str), wc.values[::-1], color=ACCENT[3], edgecolor="none")
ax3.set_title("Most Common Weight Classes (kg)", fontsize=13, fontweight="bold")
ax3.set_xlabel("# Entries")
ax3.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x/1e3)}K"))

# ── 4. Age class distribution ────────────────────────────────────────────────
ax4 = fig.add_subplot(gs[1, 1])
ac = df["AgeClass"].value_counts()
# sort by age band start number
def age_sort_key(s):
    try: return int(str(s).split("-")[0])
    except: return 999
ac_sorted = ac.sort_index(key=lambda idx: [age_sort_key(x) for x in idx])
bars4 = ax4.bar(ac_sorted.index, ac_sorted.values, color=ACCENT[2], edgecolor="none")
ax4.set_title("Age Class Distribution", fontsize=13, fontweight="bold")
ax4.set_ylabel("# Entries")
ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x/1e3)}K"))
plt.setp(ax4.get_xticklabels(), rotation=40, ha="right", fontsize=8)

# ── 5. Top divisions ──────────────────────────────────────────────────────────
ax5 = fig.add_subplot(gs[1, 2])
top_div = df["Division"].value_counts().head(12)
ax5.barh(top_div.index[::-1], top_div.values[::-1], color=ACCENT[4], edgecolor="none")
ax5.set_title("Top 12 Divisions", fontsize=13, fontweight="bold")
ax5.set_xlabel("# Entries")
ax5.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x/1e3)}K"))

# ── 6. Individual lift distributions by sex (Full Power, Raw) ────────────────
ax6 = fig.add_subplot(gs[2, :])
raw_sbd = df[(df["Event"] == "SBD") & (df["Equipment"] == "Raw")]
lifts = {"Best3SquatKg": "Squat", "Best3BenchKg": "Bench", "Best3DeadliftKg": "Deadlift"}
lift_colors_m = ["#74B9FF", "#A29BFE", "#55EFC4"]
lift_colors_f = ["#FF6B6B", "#FD79A8", "#FDCB6E"]
lift_positions = [0, 1, 2]

violin_data_m, violin_data_f = [], []
for col in lifts:
    m = raw_sbd[(raw_sbd["Sex"] == "M") & (raw_sbd[col] > 0)][col].dropna()
    f = raw_sbd[(raw_sbd["Sex"] == "F") & (raw_sbd[col] > 0)][col].dropna()
    violin_data_m.append(m.sample(min(len(m), 50000), random_state=42).values)
    violin_data_f.append(f.sample(min(len(f), 50000), random_state=42).values)

positions_m = [0.8, 2.8, 4.8]
positions_f = [1.4, 3.4, 5.4]
lift_names = list(lifts.values())

for i, (dm, df_f, cm, cf, name) in enumerate(zip(violin_data_m, violin_data_f, lift_colors_m, lift_colors_f, lift_names)):
    vp_m = ax6.violinplot([dm], positions=[positions_m[i]], widths=0.5, showmedians=True)
    for pc in vp_m["bodies"]: pc.set_facecolor(cm); pc.set_alpha(0.8)
    vp_m["cmedians"].set_color("white"); vp_m["cbars"].set_color(cm)
    vp_m["cmins"].set_color(cm); vp_m["cmaxes"].set_color(cm)

    vp_f = ax6.violinplot([df_f], positions=[positions_f[i]], widths=0.5, showmedians=True)
    for pc in vp_f["bodies"]: pc.set_facecolor(cf); pc.set_alpha(0.8)
    vp_f["cmedians"].set_color("white"); vp_f["cbars"].set_color(cf)
    vp_f["cmins"].set_color(cf); vp_f["cmaxes"].set_color(cf)

ax6.set_xticks([1.1, 3.1, 5.1])
ax6.set_xticklabels(["Squat", "Bench", "Deadlift"], fontsize=12)
ax6.set_ylabel("Weight (kg)")
ax6.set_title("Individual Lift Distributions by Sex — Raw Full Power (SBD) lifters, 50K sample each",
              fontsize=13, fontweight="bold")
m_patch = mpatches.Patch(color="#74B9FF", label="Male")
f_patch = mpatches.Patch(color="#FF6B6B", label="Female")
ax6.legend(handles=[m_patch, f_patch], fontsize=10)

# ── 7. Attempt success rates ──────────────────────────────────────────────────
ax7 = fig.add_subplot(gs[3, :2])
attempt_data = {}
for lift in ["Squat", "Bench", "Deadlift"]:
    rates = []
    for attempt in [1, 2, 3]:
        col = f"{lift}{attempt}Kg"
        s = df[col].dropna()
        rates.append((s > 0).mean() * 100)
    attempt_data[lift] = rates

x = np.arange(3)
width = 0.25
lift_cols = [ACCENT[1], ACCENT[0], ACCENT[2]]
for i, (lift, col) in enumerate(zip(["Squat", "Bench", "Deadlift"], lift_cols)):
    bars7 = ax7.bar(x + i * width, attempt_data[lift], width, label=lift, color=col, edgecolor="none")
    for bar, val in zip(bars7, attempt_data[lift]):
        ax7.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f"{val:.1f}%", ha="center", fontsize=9, color="white")

ax7.set_xticks(x + width)
ax7.set_xticklabels(["Attempt 1", "Attempt 2", "Attempt 3"], fontsize=11)
ax7.set_ylabel("Success Rate (%)")
ax7.set_ylim(0, 105)
ax7.set_title("Lift Attempt Success Rates by Attempt Number", fontsize=13, fontweight="bold")
ax7.legend(fontsize=10)

# ── 8. Lift contribution to total (SBD Raw) ───────────────────────────────────
ax8 = fig.add_subplot(gs[3, 2])
comp = raw_sbd[["Best3SquatKg", "Best3BenchKg", "Best3DeadliftKg"]].dropna()
comp = comp[(comp > 0).all(axis=1)]
pct_squat = (comp["Best3SquatKg"] / (comp["Best3SquatKg"] + comp["Best3BenchKg"] + comp["Best3DeadliftKg"])).mean() * 100
pct_bench = (comp["Best3BenchKg"] / (comp["Best3SquatKg"] + comp["Best3BenchKg"] + comp["Best3DeadliftKg"])).mean() * 100
pct_dead  = (comp["Best3DeadliftKg"] / (comp["Best3SquatKg"] + comp["Best3BenchKg"] + comp["Best3DeadliftKg"])).mean() * 100
wedges, texts, autotexts = ax8.pie(
    [pct_squat, pct_bench, pct_dead],
    labels=["Squat", "Bench", "Deadlift"],
    autopct="%1.1f%%", colors=[ACCENT[1], ACCENT[0], ACCENT[2]],
    startangle=90, textprops={"color": "white", "fontsize": 11})
for at in autotexts: at.set_fontsize(10)
ax8.set_title("Avg Lift Contribution to Total\n(Raw SBD lifters)", fontsize=13, fontweight="bold")

plt.savefig("eda_supplementary.png", dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print("Saved eda_supplementary.png")
