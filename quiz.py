import csv
import os
from validators import validate_answer

# -------------------------------------------------------
# quiz.py — Quiz engine: reads questions.csv and runs the quiz
# Requirement: CSV file usage, function definitions
# -------------------------------------------------------

QUESTIONS_FILE = "questions.csv"
RESULTS_FILE   = "results.csv"


def start_quiz():
    """
    Reads questions from questions.csv, presents them one by one,
    validates answers using regex, returns (score, total).
    """
    score = 0
    total = 0

    print("\n" + "=" * 40)
    print("            QUIZ STARTED            ")
    print("=" * 40)

    try:
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header

            for row in reader:
                if not row or len(row) < 6:
                    continue

                total += 1
                question_text  = row[0].strip()
                options        = [row[1], row[2], row[3], row[4]]
                correct_answer = row[5].strip()

                clean_question = question_text.lstrip("1234567890. ")
                print(f"\nQ{total}: {clean_question}")

                for i, opt in enumerate(options, 1):
                    print(f"  {i}. {opt.strip()}")

                # Regex validation on answer input
                while True:
                    choice_str = input("Your answer (1-4): ").strip()
                    if validate_answer(choice_str):
                        choice = int(choice_str)
                        break
                    else:
                        print("  [X] Enter 1, 2, 3, or 4 only.")

                selected = options[choice - 1].strip()

                if selected == correct_answer:
                    print("  [✓] Correct!")
                    score += 1
                else:
                    print(f"  [✗] Wrong! Correct answer: {correct_answer}")

        print("\n" + "=" * 40)
        return score, total

    except FileNotFoundError:
        print(f"[ERROR] '{QUESTIONS_FILE}' not found.")
        return 0, 0
    except Exception as e:
        print(f"[ERROR] Quiz failed: {e}")
        return 0, 0


def export_result_to_csv(username, score, total):
    """
    Appends quiz result to results.csv.
    Requirement: CSV file creation / dataset output.
    """
    try:
        file_exists = os.path.isfile(RESULTS_FILE)

        with open(RESULTS_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Username", "Score", "Total"])
            writer.writerow([username, score, total])

        print("[OK] Result exported to results.csv")

    except Exception as e:
        print(f"[ERROR] Could not export result: {e}")