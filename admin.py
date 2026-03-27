import csv
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from db import get_connection

# -------------------------------------------------------
# admin.py — Admin panel functions
# Admin can: view all student performance, add questions
# -------------------------------------------------------

QUESTIONS_FILE = "questions.csv"


def get_all_students_data():
    """Fetches every student's quiz results from DB as a list of dicts."""
    try:
        con = get_connection()
        if con is None:
            return None

        cursor = con.cursor()
        query = """
            SELECT u.id, u.name, u.username, r.score, r.total
            FROM results r
            JOIN users u ON r.user_id = u.id
            ORDER BY u.name, r.id
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    except Exception as e:
        print(f"[ERROR] Could not load student data: {e}")
        return None
    finally:
        try:
            cursor.close()
            con.close()
        except:
            pass


def view_all_performance():
    """Shows a table summary of all students and their quiz stats."""
    try:
        rows = get_all_students_data()

        if not rows:
            print("\n  [INFO] No quiz data found yet. Students haven't taken any quiz.")
            return

        # Build a pandas DataFrame from the raw rows
        df = pd.DataFrame(rows, columns=["ID", "Name", "Username", "Score", "Total"])

        # Group by student and calculate their stats using numpy
        print("\n" + "=" * 55)
        print("          ALL STUDENTS PERFORMANCE REPORT")
        print("=" * 55)
        print(f"  {'Name':<15} {'Username':<12} {'Attempts':>8} {'Avg Score':>10} {'Accuracy':>10}")
        print("-" * 55)

        grouped = df.groupby(["ID", "Name", "Username"])

        for (uid, name, username), group in grouped:
            attempts  = len(group)
            avg_score = round(np.mean(group["Score"].values), 2)
            total_correct = group["Score"].sum()
            total_possible = group["Total"].sum()
            accuracy = round((total_correct / total_possible) * 100, 1) if total_possible > 0 else 0.0
            print(f"  {name:<15} {username:<12} {attempts:>8} {avg_score:>10} {accuracy:>9}%")

        print("=" * 55)
        print(f"  Total Records: {len(df)} attempt(s) from {df['Username'].nunique()} student(s)")

    except Exception as e:
        print(f"[ERROR] Performance view failed: {e}")


def view_all_performance_chart():
    """Draws a bar chart comparing average scores of all students."""
    try:
        rows = get_all_students_data()
        if not rows:
            print("\n  [INFO] No data to plot.")
            return

        df = pd.DataFrame(rows, columns=["ID", "Name", "Username", "Score", "Total"])
        grouped = df.groupby("Name")["Score"].mean().reset_index()
        grouped.columns = ["Name", "AvgScore"]

        names = grouped["Name"].values
        scores = grouped["AvgScore"].values
        x_pos = np.arange(len(names))

        plt.figure(figsize=(9, 5))
        bars = plt.bar(x_pos, scores, color="#5b8dee", edgecolor="black", width=0.5)
        plt.xticks(x_pos, names)
        plt.title("Average Score per Student", fontsize=14)
        plt.xlabel("Student Name")
        plt.ylabel("Average Score")
        plt.ylim(0, 10)
        plt.grid(True, axis="y", linestyle="--", alpha=0.6)

        # Label each bar with the value
        for bar, val in zip(bars, scores):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                     f"{round(val, 1)}", ha="center", fontsize=9)

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"[ERROR] Chart generation failed: {e}")


def add_question():
    """Lets the admin add a new question to questions.csv."""
    try:
        print("\n--- Add New Question ---")
        print("  (Press Enter without typing to cancel at any time)\n")

        question = input("  Enter the question text  : ").strip()
        if not question:
            print("  [--] Cancelled.")
            return

        opt1 = input("  Option 1                 : ").strip()
        opt2 = input("  Option 2                 : ").strip()
        opt3 = input("  Option 3                 : ").strip()
        opt4 = input("  Option 4                 : ").strip()

        if not all([opt1, opt2, opt3, opt4]):
            print("  [X] All four options are required.")
            return

        print(f"\n  1. {opt1}")
        print(f"  2. {opt2}")
        print(f"  3. {opt3}")
        print(f"  4. {opt4}")
        correct_num = input("\n  Which option is correct? (1/2/3/4): ").strip()

        if correct_num not in ["1", "2", "3", "4"]:
            print("  [X] Invalid choice. Enter 1, 2, 3, or 4.")
            return

        options_map = {"1": opt1, "2": opt2, "3": opt3, "4": opt4}
        correct_answer = options_map[correct_num]

        # Write to CSV
        file_exists = os.path.isfile(QUESTIONS_FILE)
        with open(QUESTIONS_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["question", "opt1", "opt2", "opt3", "opt4", "answer"])
            writer.writerow([question, opt1, opt2, opt3, opt4, correct_answer])

        print(f"\n  [OK] Question added successfully! Correct answer: {correct_answer}")

    except Exception as e:
        print(f"[ERROR] Failed to add question: {e}")


def view_all_questions():
    """Lists all questions currently in questions.csv."""
    try:
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            print("\n" + "=" * 55)
            print("           CURRENT QUESTION BANK")
            print("=" * 55)
            for i, row in enumerate(reader, 1):
                if row and len(row) >= 6:
                    q_text = row[0].strip().replace("\n", " ")
                    # Trim for display if too long
                    if len(q_text) > 60:
                        q_text = q_text[:57] + "..."
                    print(f"  Q{i}: {q_text}")
            print("=" * 55)
    except FileNotFoundError:
        print(f"  [X] File '{QUESTIONS_FILE}' not found.")
    except Exception as e:
        print(f"[ERROR] Could not list questions: {e}")
