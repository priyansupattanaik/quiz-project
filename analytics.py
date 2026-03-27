import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from services import get_user_data

# -------------------------------------------------------
# analytics.py — Performance analytics using Pandas, NumPy, Matplotlib
# Requirement: numpy, pandas, matplotlib
# -------------------------------------------------------

def get_dataframe(user_id):
    """
    Fetches quiz results from DB and converts to a Pandas DataFrame.
    Returns None if no data found.
    """
    try:
        raw_data = get_user_data(user_id)
        if not raw_data:
            print("\n[INFO] No quiz attempts found. Take a quiz first!")
            return None

        # Requirement: pandas DataFrame from database records
        df = pd.DataFrame(raw_data, columns=["Name", "Score", "Total"])

        if df.empty:
            print("\n[INFO] No data available.")
            return None

        return df

    except Exception as e:
        print(f"[ERROR] Could not load data: {e}")
        return None


def display_text_summary(user_id):
    """
    Shows a text-based analytics summary using NumPy calculations.
    Requirement: numpy for statistical calculations.
    """
    try:
        df = get_dataframe(user_id)
        if df is None:
            return

        total_quizzes  = len(df)
        total_correct  = int(df["Score"].sum())
        total_wrong    = int((df["Total"] - df["Score"]).sum())

        # Requirement: numpy for mean/round calculations
        avg_score      = np.mean(df["Score"].values)
        accuracy       = (total_correct / (total_correct + total_wrong)) * 100 if (total_correct + total_wrong) > 0 else 0

        print(f"\n{'─'*32}")
        print(f"  Total Quizzes Attempted : {total_quizzes}")
        print(f"  Total Correct Answers   : {total_correct}")
        print(f"  Total Wrong Answers     : {total_wrong}")
        print(f"  Average Score           : {round(avg_score, 2)}")
        print(f"  Overall Accuracy        : {round(accuracy, 2)}%")
        print(f"{'─'*32}")

    except Exception as e:
        print(f"[ERROR] Could not show text summary: {e}")


def display_line_chart(user_id):
    """Performance over time — Line Chart."""
    try:
        df = get_dataframe(user_id)
        if df is None:
            return

        attempts = np.arange(1, len(df) + 1)   # NumPy array for x-axis
        scores   = df["Score"].values

        plt.figure(figsize=(8, 5))
        plt.plot(attempts, scores, marker="o", linestyle="-", color="royalblue", linewidth=2, markersize=7)
        plt.title("Performance Over Time", fontsize=14)
        plt.xlabel("Attempt Number")
        plt.ylabel("Score")
        plt.xticks(attempts)
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"[ERROR] Line chart failed: {e}")


def display_bar_chart(user_id):
    """Correct vs Wrong per attempt — Stacked Bar Chart."""
    try:
        df = get_dataframe(user_id)
        if df is None:
            return

        attempts = np.arange(1, len(df) + 1)
        corrects = df["Score"].values
        wrongs   = (df["Total"] - df["Score"]).values

        plt.figure(figsize=(8, 5))
        plt.bar(attempts, corrects, color="#66b3ff", label="Correct")
        plt.bar(attempts, wrongs,   bottom=corrects, color="#ff9999", label="Wrong")
        plt.title("Correct vs Wrong per Attempt", fontsize=14)
        plt.xlabel("Attempt Number")
        plt.ylabel("Number of Questions")
        plt.xticks(attempts)
        plt.legend()
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"[ERROR] Bar chart failed: {e}")


def display_pie_chart(user_id):
    """Overall correct vs wrong ratio — Pie Chart."""
    try:
        df = get_dataframe(user_id)
        if df is None:
            return

        total_correct = int(df["Score"].sum())
        total_wrong   = int((df["Total"] - df["Score"]).sum())

        if total_correct == 0 and total_wrong == 0:
            print("[INFO] Not enough data to draw pie chart.")
            return

        labels = ["Correct", "Wrong"]
        sizes  = [total_correct, total_wrong]
        colors = ["#66b3ff", "#ff9999"]

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90)
        plt.title("Overall Correct vs Wrong Ratio", fontsize=14)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"[ERROR] Pie chart failed: {e}")


def display_histogram(user_id):
    """Score distribution across all attempts — Histogram."""
    try:
        df = get_dataframe(user_id)
        if df is None:
            return

        scores = df["Score"].values  # NumPy array

        plt.figure(figsize=(8, 5))
        plt.hist(scores, bins=5, color="orange", edgecolor="black")
        plt.title("Score Distribution", fontsize=14)
        plt.xlabel("Score")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"[ERROR] Histogram failed: {e}")