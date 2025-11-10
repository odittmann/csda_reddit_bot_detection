import os
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

# Files and params
BIG_DATA_FILE = "conservative_sept_nov_2024_clean.csv"
SUSPICIOUS_FILE = "suspicious_accounts_posting_patterns.csv"
SAVE_PLOTS = True
FIG_FOLDER = f"suspicious_analysis_{datetime.now().strftime('%m-%d-%H_%M')}"
os.makedirs(FIG_FOLDER, exist_ok=True)



def load_data(big_file, suspicious_file):
    # load main and suspicious user data into dfs
    with open(suspicious_file, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    suspicious_users = [u.strip() for u in lines if u.strip().lower() != "username"]

    df = pd.read_csv(big_file)
    df["created_datetime"] = pd.to_datetime(df["created_utc"], unit="s", errors="coerce")
    df = df.dropna(subset=["author", "link_id", "created_datetime"])

    filtered = df[df["author"].isin(suspicious_users)]

    print(f"Filtered: {len(filtered)} comments from {filtered['author'].nunique()} users")
    return filtered, df



def plot_posting_activity(df, output_path):
    # plot posts over time with significant events marked
    start_date = pd.Timestamp("2024-09-01")
    end_date = pd.Timestamp("2024-11-30")

    plt.figure(figsize=(14, 6))
    sns.histplot(
        data=df,
        x="created_datetime",
        hue="author",
        multiple="stack",
        bins=100,
        palette="husl",
        edgecolor=None,
        legend=False
    )

    ax = plt.gca()
    ax.set_xlim(start_date, end_date)
    ax.set_title("Posting Activity Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Comments")

    ax.xaxis.set_major_locator(mdates.MonthLocator())        
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=mdates.SU))
    plt.xticks(rotation=30, ha="right")
    ax.grid(True, which="major", linestyle="--", alpha=0.5)
    ax.grid(True, which="minor", linestyle=":", alpha=0.3)

    events = {
        "Second Presidential Debate": "2024-09-10",
        "9/11 Anniversary": "2024-09-11",
        "VP Debate": "2024-10-01",
        "Trump Rally at MSG": "2024-10-27",
        "Election Day": "2024-11-05"
    }

    for label, date in events.items():
        ax.axvline(pd.to_datetime(date), color="black", linestyle="--", alpha=0.7)
        ax.text(
            pd.to_datetime(date) + pd.Timedelta(days=0.5),
            ax.get_ylim()[1] * 0.9,
            label,
            rotation=90,
            va="top",
            ha="left",
            fontsize=9,
            color="black",
            backgroundcolor="white"
        )

    plt.tight_layout()
    file_path = os.path.join(output_path, "posting_activity.png")
    plt.savefig(file_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Saved: {file_path}")
  


def plot_posting_heatmaps(df, top_users, output_path, users_per_fig=25):
    # day/hour heatmaps split into multiple figures
    df["created_datetime"] = pd.to_datetime(df["created_utc"], unit="s", errors="coerce")
    df["hour"] = df["created_datetime"].dt.hour
    df["day"] = df["created_datetime"].dt.day_name()
    df["day"] = pd.Categorical(df["day"], categories=[
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ], ordered=True)

    # split users into chunks
    for start in range(0, len(top_users), users_per_fig):
        users_chunk = top_users[start:start + users_per_fig]
        n_users = len(users_chunk)
        n_cols = 5
        n_rows = int(np.ceil(n_users / n_cols))
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(3.5 * n_cols, 3 * n_rows))
        axes = axes.flatten()

        for i, user in enumerate(users_chunk):
            user_data = df[df["author"] == user]
            heat = user_data.groupby(["day", "hour"]).size().unstack(fill_value=0)
            sns.heatmap(heat, ax=axes[i], cmap="Blues", cbar=False)
            axes[i].set_title(user, fontsize=9)
            axes[i].set_xlabel("Hour")
            axes[i].set_ylabel("Day")

        # hide extra axes
        for j in range(i + 1, len(axes)):
            axes[j].axis("off")

        fig.suptitle(f"Posting Activity Heatmaps (Users {start+1}-{start+n_users})", fontsize=14)
        plt.tight_layout(rect=[0, 0, 1, 0.95])

        file_path = os.path.join(output_path, f"posting_heatmaps_{start+1}-{start+n_users}.png")
        plt.savefig(file_path, bbox_inches="tight")
        plt.close()
        print(f"Saved: {file_path}")




if __name__ == "__main__":
    df, df_unfiltered = load_data(BIG_DATA_FILE, SUSPICIOUS_FILE)

    # Plot and save figs
    plot_posting_activity(df, FIG_FOLDER)

    # function call with 300
    # plot_posting_heatmaps(df_unfiltered, df_unfiltered["author"].value_counts().head(300).index.tolist(), FIG_FOLDER)
    # plot_posting_heatmaps(df_unfiltered, df_unfiltered["author"].value_counts().head(25).index.tolist(), FIG_FOLDER)

    print("Done.")
