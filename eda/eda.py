import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ── Load ────────────────────────────────────────────────────────────────────
df = pd.read_csv("data/openpowerlifting-2026-05-16-d230fa1a.csv", low_memory=False)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Year"] = df["Date"].dt.year

print(f"Total samples: {len(df):,}")

# ── Style ────────────────────────────────────────────────────────────────────
sns.set_theme(style="darkgrid", palette="muted")
plt.rcParams.update({"figure.facecolor": "#1c1c1e", "axes.facecolor": "#2c2c2e",
                     "axes.labelcolor": "white", "xtick.color": "white",
                     "ytick.color": "white", "text.color": "white",
                     "axes.titlecolor": "white", "grid.color": "#3c3c3e",
                     "axes.edgecolor": "#3c3c3e"})
ACCENT = ["#FF6B6B", "#4ECDC4", "#FFE66D", "#A29BFE", "#74B9FF", "#55EFC4"]

fig = plt.figure(figsize=(22, 26))
fig.patch.set_facecolor("#1c1c1e")
fig.suptitle("OpenPowerlifting — Exploratory Data Analysis\n3,925,887 competition entries",
             fontsize=20, fontweight="bold", color="white", y=0.98)

gs = fig.add_gridspec(4, 3, hspace=0.45, wspace=0.35)

# ── 1. Entries per year ───────────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, :2])
yearly = df.groupby("Year").size().reset_index(name="count")
yearly = yearly[(yearly["Year"] >= 1960) & (yearly["Year"] <= 2026)]
ax1.fill_between(yearly["Year"], yearly["count"], alpha=0.3, color=ACCENT[1])
ax1.plot(yearly["Year"], yearly["count"], color=ACCENT[1], linewidth=2)
ax1.set_title("Competition Entries per Year", fontsize=13, fontweight="bold")
ax1.set_xlabel("Year"); ax1.set_ylabel("# Entries")
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

# ── 2. Sex distribution ───────────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 2])
sex_counts = df["Sex"].value_counts()
wedges, texts, autotexts = ax2.pie(
    sex_counts, labels=sex_counts.index, autopct="%1.1f%%",
    colors=ACCENT[:len(sex_counts)], startangle=140,
    textprops={"color": "white", "fontsize": 11})
for at in autotexts:
    at.set_fontsize(10)
ax2.set_title("Sex Distribution", fontsize=13, fontweight="bold")

# ── 3. Event type breakdown ───────────────────────────────────────────────────
ax3 = fig.add_subplot(gs[1, 0])
event_map = {"SBD": "Full Power\n(SBD)", "B": "Bench Only", "D": "Deadlift Only",
             "S": "Squat Only", "BD": "Bench+Deadlift", "SB": "Squat+Bench"}
event_counts = df["Event"].value_counts().head(6)
event_labels = [event_map.get(e, e) for e in event_counts.index]
bars = ax3.barh(event_labels[::-1], event_counts.values[::-1], color=ACCENT[0], edgecolor="none")
ax3.set_title("Event Type", fontsize=13, fontweight="bold")
ax3.set_xlabel("# Entries")
ax3.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x/1e6):.1f}M" if x >= 1e6 else f"{int(x/1e3)}K"))
for bar, val in zip(bars, event_counts.values[::-1]):
    ax3.text(bar.get_width() + 5000, bar.get_y() + bar.get_height()/2,
             f"{val:,}", va="center", fontsize=8, color="white")

# ── 4. Equipment breakdown ────────────────────────────────────────────────────
ax4 = fig.add_subplot(gs[1, 1])
eq_counts = df["Equipment"].value_counts()
bars4 = ax4.bar(eq_counts.index, eq_counts.values, color=ACCENT[3], edgecolor="none")
ax4.set_title("Equipment Type", fontsize=13, fontweight="bold")
ax4.set_ylabel("# Entries")
ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x/1e6):.1f}M" if x >= 1e6 else f"{int(x/1e3)}K"))
plt.setp(ax4.get_xticklabels(), rotation=15, ha="right", fontsize=9)
for bar in bars4:
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5000,
             f"{int(bar.get_height()):,}", ha="center", fontsize=7.5, color="white")

# ── 5. Top 15 federations ─────────────────────────────────────────────────────
ax5 = fig.add_subplot(gs[1, 2])
top_feds = df["Federation"].value_counts().head(15)
ax5.barh(top_feds.index[::-1], top_feds.values[::-1], color=ACCENT[4], edgecolor="none")
ax5.set_title("Top 15 Federations", fontsize=13, fontweight="bold")
ax5.set_xlabel("# Entries")
ax5.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x/1e3)}K"))

# ── 6. Age distribution ───────────────────────────────────────────────────────
ax6 = fig.add_subplot(gs[2, 0])
ages = df["Age"].dropna()
ages = ages[(ages >= 10) & (ages <= 90)]
ax6.hist(ages, bins=80, color=ACCENT[2], edgecolor="none", alpha=0.85)
ax6.axvline(ages.median(), color="white", linestyle="--", linewidth=1.5, label=f"Median: {ages.median():.0f}")
ax6.set_title("Age Distribution", fontsize=13, fontweight="bold")
ax6.set_xlabel("Age"); ax6.set_ylabel("# Lifters")
ax6.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x/1e3)}K"))
ax6.legend(fontsize=9)

# ── 7. Bodyweight distribution by sex ────────────────────────────────────────
ax7 = fig.add_subplot(gs[2, 1])
for sex, color in zip(["M", "F"], [ACCENT[4], ACCENT[0]]):
    bw = df[df["Sex"] == sex]["BodyweightKg"].dropna()
    bw = bw[(bw > 30) & (bw < 250)]
    ax7.hist(bw, bins=80, alpha=0.6, color=color, label=sex, edgecolor="none")
ax7.set_title("Bodyweight Distribution by Sex", fontsize=13, fontweight="bold")
ax7.set_xlabel("Bodyweight (kg)"); ax7.set_ylabel("# Entries")
ax7.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x/1e3)}K"))
ax7.legend(fontsize=10)

# ── 8. Total lifted distribution by sex ──────────────────────────────────────
ax8 = fig.add_subplot(gs[2, 2])
for sex, color in zip(["M", "F"], [ACCENT[4], ACCENT[0]]):
    tots = df[(df["Sex"] == sex) & (df["TotalKg"] > 0)]["TotalKg"].dropna()
    tots = tots[tots < 1500]
    ax8.hist(tots, bins=80, alpha=0.6, color=color, label=sex, edgecolor="none")
ax8.set_title("Total Lifted (kg) by Sex", fontsize=13, fontweight="bold")
ax8.set_xlabel("Total (kg)"); ax8.set_ylabel("# Entries")
ax8.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x/1e3)}K"))
ax8.legend(fontsize=10)

# ── 9. Dots score distribution by equipment (Full Power only) ────────────────
ax9 = fig.add_subplot(gs[3, 0])
sbd = df[(df["Event"] == "SBD") & (df["Dots"] > 0) & (df["Dots"] < 1000)]
for eq, color in zip(["Raw", "Wraps", "Single-ply", "Multi-ply"],
                     [ACCENT[1], ACCENT[2], ACCENT[0], ACCENT[3]]):
    sub = sbd[sbd["Equipment"] == eq]["Dots"]
    if len(sub) > 0:
        ax9.hist(sub, bins=60, alpha=0.55, label=eq, color=color, edgecolor="none")
ax9.set_title("Dots Score by Equipment (Full Power)", fontsize=13, fontweight="bold")
ax9.set_xlabel("Dots Score"); ax9.set_ylabel("# Entries")
ax9.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x/1e3)}K"))
ax9.legend(fontsize=9)

# ── 10. Top 15 meet countries ─────────────────────────────────────────────────
ax10 = fig.add_subplot(gs[3, 1])
top_countries = df["MeetCountry"].value_counts().head(15)
ax10.barh(top_countries.index[::-1], top_countries.values[::-1], color=ACCENT[5], edgecolor="none")
ax10.set_title("Top 15 Meet Countries", fontsize=13, fontweight="bold")
ax10.set_xlabel("# Entries")
ax10.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x/1e6):.1f}M" if x >= 1e6 else f"{int(x/1e3)}K"))

# ── 11. Drug-tested vs untested ───────────────────────────────────────────────
ax11 = fig.add_subplot(gs[3, 2])
tested = df["Tested"].fillna("Unknown").map({"Yes": "Tested", "No": "Untested"}).fillna("Unknown")
t_counts = tested.value_counts()
ax11.pie(t_counts, labels=t_counts.index, autopct="%1.1f%%",
         colors=[ACCENT[1], ACCENT[0], "#888"], startangle=140,
         textprops={"color": "white", "fontsize": 11})
ax11.set_title("Drug Tested?", fontsize=13, fontweight="bold")

# ── Save & show ───────────────────────────────────────────────────────────────
out = "eda_overview.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print(f"Saved → {out}")
plt.show()
