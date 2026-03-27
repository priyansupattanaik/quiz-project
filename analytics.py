import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from db import get_connection

# pandas and numpy analytics
def get_user_data(uid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT score, total FROM results WHERE user_id=%s", (uid,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def show_stats(uid):
    rows = get_user_data(uid)
    if not rows:
        print("No quiz data yet.")
        return

    df = pd.DataFrame(rows, columns=["score", "total"])
    
    total_quizzes = len(df)
    total_correct = df["score"].sum()
    total_wrong = (df["total"] - df["score"]).sum()
    avg = np.mean(df["score"])

    print("\n--- Your Stats ---")
    print(f"Quizzes taken: {total_quizzes}")
    print(f"Correct answers: {total_correct}")
    print(f"Wrong answers: {total_wrong}")
    print(f"Average score: {round(avg, 2)}")

def show_line_chart(uid):
    rows = get_user_data(uid)
    if not rows: 
        print("Take a quiz first to see the chart.")
        return
        
    df = pd.DataFrame(rows, columns=["score", "total"])
    x = np.arange(1, len(df) + 1)
    y = df["score"]

    plt.plot(x, y, marker="o")
    plt.title("Scores Over Time")
    plt.xlabel("Attempt")
    plt.ylabel("Score")
    plt.show()

def show_pie_chart(uid):
    rows = get_user_data(uid)
    if not rows: 
        print("Take a quiz first to see the chart.")
        return
        
    df = pd.DataFrame(rows, columns=["score", "total"])
    correct = int(df["score"].sum())
    wrong = int((df["total"] - df["score"]).sum())
    
    plt.pie([correct, wrong], labels=["Correct", "Wrong"], autopct="%1.1f%%")
    plt.title("Overall Accuracy")
    plt.show()