import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from db import get_connection

# admin specific functions
def view_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.name, r.score, r.total 
        FROM results r JOIN users u ON r.user_id = u.id
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        print("No records found.")
        return

    df = pd.DataFrame(rows, columns=["Name", "Score", "Total"])
    print("\n--- All Student Records ---")
    print(df.to_string(index=False))


def show_student_chart():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.name, r.score, r.total 
        FROM results r JOIN users u ON r.user_id = u.id
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        print("No data to plot.")
        return

    df = pd.DataFrame(rows, columns=["Name", "Score", "Total"])

    # group by student name and get average score using numpy
    names = df["Name"].unique()
    avg_scores = np.array([df[df["Name"] == n]["Score"].mean() for n in names])

    x = np.arange(len(names))

    plt.figure(figsize=(8, 5))
    bars = plt.bar(x, avg_scores, color="steelblue", edgecolor="black", width=0.5)
    plt.xticks(x, names)
    plt.title("Average Score per Student")
    plt.xlabel("Student")
    plt.ylabel("Average Score")
    plt.ylim(0, 10)

    # label each bar
    for bar, val in zip(bars, avg_scores):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                 str(round(val, 1)), ha="center")

    plt.tight_layout()
    plt.show()


def add_question():

    q = input("Enter question: ")
    o1 = input("Option 1: ")
    o2 = input("Option 2: ")
    o3 = input("Option 3: ")
    o4 = input("Option 4: ")
    ans = input("Correct Answer (1-4): ")

    options = {"1": o1, "2": o2, "3": o3, "4": o4}
    correct = options.get(ans)

    if not correct:
        print("Invalid answer choice.")
        return

    with open("questions.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([q, o1, o2, o3, o4, correct])
    print("Question added to bank!")