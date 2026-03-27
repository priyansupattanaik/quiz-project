from services import register, login, save_result, update_password, delete_account
from quiz import start_quiz, export_result_to_csv
from analytics import display_line_chart, display_bar_chart, display_pie_chart, display_histogram, display_text_summary
from models import Admin
from admin import view_all_performance, view_all_performance_chart, add_question, view_all_questions
import db  # Auto-creates DB and tables on import

# -------------------------------------------------------
# main.py — Application entry point
# Requirement: functions, exception handling, menu flow
# -------------------------------------------------------

def admin_menu():
    """Admin panel menu — only reached after credential check."""
    admin = Admin()

    while True:
        try:
            print("\n" + "=" * 40)
            # Polymorphism: Admin.display_info() is called (different from QuizUser's)
            admin.display_info()
            print("=" * 40)
            print("  1. View All Students Performance")
            print("  2. Student Performance Chart")
            print("  3. View Question Bank")
            print("  4. Add a New Question")
            print("  5. Logout")
            print("=" * 40)

            opt = input("Enter choice (1-5): ").strip()

            if   opt == "1":
                view_all_performance()
            elif opt == "2":
                view_all_performance_chart()
            elif opt == "3":
                view_all_questions()
            elif opt == "4":
                add_question()
            elif opt == "5":
                print("\n  Admin logged out.")
                break
            else:
                print("  [X] Invalid choice. Enter 1 to 5.")

        except Exception as e:
            print(f"  [ERROR] {e}")


def main():
    """Main function — shows the root menu and routes all user actions."""
    while True:
        try:
            print("\n" + "=" * 40)
            print("     ONLINE QUIZ SYSTEM")
            print("=" * 40)
            print("  1. Register")
            print("  2. Login")
            print("  3. Admin Login")
            print("  4. Exit")
            print("=" * 40)

            choice = input("Enter choice (1-4): ").strip()

            if choice == "1":
                register()

            elif choice == "2":
                quiz_user = login()  # Returns QuizUser object (OOP)

                if quiz_user:
                    while True:
                        print("\n" + "=" * 40)
                        quiz_user.display_info()  # Polymorphism

                        # Dictionary usage requirement
                        stats_dict = {"total_quizzes": quiz_user.total_quizzes_taken}
                        quiz_user.load_stats_from_dict(stats_dict)

                        print("=" * 40)
                        print("  1. Take a Quiz")
                        print("  2. View Performance Analytics")
                        print("  3. Change Password")
                        print("  4. Delete Account")
                        print("  5. Logout")
                        print("=" * 40)

                        opt = input("Enter choice (1-5): ").strip()

                        if opt == "1":
                            score, total = start_quiz()

                            if total > 0:
                                print(f"\n{'='*40}")
                                print(f"  QUIZ RESULT")
                                print(f"{'='*40}")
                                print(f"  Correct : {score}")
                                print(f"  Wrong   : {total - score}")
                                print(f"  Total   : {total}")
                                print(f"  Score   : {score}/{total}")
                                print(f"{'='*40}")

                                save_result(quiz_user.user_id, score, total)   # CRUD Create
                                export_result_to_csv(quiz_user.username, score, total)  # CSV
                                quiz_user.total_quizzes_taken += 1

                        elif opt == "2":
                            while True:
                                print("\n" + "=" * 40)
                                print("    PERFORMANCE ANALYTICS")
                                print("=" * 40)
                                display_text_summary(quiz_user.user_id)
                                print("\n  1. Performance Over Time")
                                print("  2. Correct vs Wrong per Attempt")
                                print("  3. Overall Accuracy Ratio (Pie)")
                                print("  4. Score Distribution (Histogram)")
                                print("  5. Go Back")
                                print("=" * 40)

                                an_opt = input("Enter choice (1-5): ").strip()

                                if   an_opt == "1": display_line_chart(quiz_user.user_id)
                                elif an_opt == "2": display_bar_chart(quiz_user.user_id)
                                elif an_opt == "3": display_pie_chart(quiz_user.user_id)
                                elif an_opt == "4": display_histogram(quiz_user.user_id)
                                elif an_opt == "5": break
                                else: print("  [X] Invalid choice.")

                        elif opt == "3":
                            update_password(quiz_user)   # CRUD Update

                        elif opt == "4":
                            if delete_account(quiz_user.user_id):   # CRUD Delete
                                print(f"  Goodbye, {quiz_user.name}!")
                                break

                        elif opt == "5":
                            print(f"\n  Logged out. Goodbye, {quiz_user.name}!")
                            break

                        else:
                            print("  [X] Invalid choice. Enter 1 to 5.")

            elif choice == "3":
                print("\n--- Admin Login ---")
                uname = input("Username: ").strip()
                pwd   = input("Password: ").strip()

                if Admin.check_credentials(uname, pwd):  # Static method (OOP)
                    print("\n[OK] Admin Login Successful!")
                    admin_menu()
                else:
                    print("\n[X] Invalid admin credentials.")

            elif choice == "4":
                print("\n  Thank you for using the Quiz System. Goodbye!")
                break

            else:
                print("  [X] Invalid choice. Enter 1, 2, 3, or 4.")

        except KeyboardInterrupt:
            print("\n\n  Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"  [CRITICAL ERROR] {e}")


if __name__ == "__main__":
    main()