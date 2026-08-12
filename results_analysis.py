import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------
# LOAD RESULTS
# --------------------------------

df = pd.read_csv("ecg_results.csv")

print("--- ECG RESULTS ---")
print(df.to_string(index=False))


# =================================
# GRAPH 1: RAW VS FILTERED HEART RATE
# =================================

plt.figure(figsize=(10, 5))

x = range(len(df))

plt.bar(
    [i - 0.2 for i in x],
    df["Raw HR (BPM)"],
    width=0.4,
    label="Raw HR"
)

plt.bar(
    [i + 0.2 for i in x],
    df["Filtered HR (BPM)"],
    width=0.4,
    label="Filtered HR"
)

plt.xticks(
    x,
    df["Record"].astype(str)
)

plt.title("Raw vs Filtered Heart Rate")
plt.xlabel("MIT-BIH Record")
plt.ylabel("Average Heart Rate (BPM)")

plt.grid(axis="y")
plt.legend()

# SAVE BEFORE SHOW
plt.savefig(
    "plots/heart_rate_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# =================================
# GRAPH 2: FILTERING DIFFERENCE
# =================================

plt.figure(figsize=(10, 5))

bars = plt.bar(
    df["Record"].astype(str),
    df["HR Difference (%)"]
)

plt.title(
    "Percentage Difference Between Raw and Filtered Heart Rate"
)

plt.xlabel("MIT-BIH Record")
plt.ylabel("Heart Rate Difference (%)")

plt.grid(axis="y")

# Show the value above each bar
for bar, value in zip(bars, df["HR Difference (%)"]):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value,
        f"{value:.3f}%",
        ha="center",
        va="bottom"
    )

plt.savefig(
    "plots/filtering_difference.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()