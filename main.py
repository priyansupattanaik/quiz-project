from services import register, login, update_password, delete_account, save_result
from quiz import start_quiz, export_csv
from analytics import show_stats, show_line_chart, show_pie_chart
from admin import view_all_students, show_student_chart, add_question
from models import Admin
import db

# main menu loop
while True:
    print("\n===== Online Quiz System =====")
    print("1. Register")
    print("2. Login")
    print("3. Admin Login")
    print("4. Exit")
    print("==============================")
    
    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Please enter a valid number.")
        continue

    if choice == 1:
        register()
        
    elif choice == 2:
        user = login()
        if user:
            while True:
                print("\n--- Student Menu ---")
                user.display()
                print("1. Take Quiz")
                print("2. View Stats")
                print("3. View Line Chart")
                print("4. View Pie Chart")
                print("5. Change Password")
                print("6. Delete Account")
                print("7. Logout")
                
                try:
                    opt = int(input("Enter choice: "))
                except ValueError:
                    print("Invalid input.")
                    continue
                
                if opt == 1:
                    score, total = start_quiz()
                    if total > 0:
                        print(f"\nFinal Score: {score}/{total}")
                        save_result(user.uid, score, total)
                        export_csv(user.username, score, total)
                        user.load_stats({"quizzes": user.total_quizzes + 1})
                elif opt == 2:
                    show_stats(user.uid)
                elif opt == 3:
                    show_line_chart(user.uid)
                elif opt == 4:
                    show_pie_chart(user.uid)
                elif opt == 5:
                    update_password(user)
                elif opt == 6:
                    if delete_account(user):
                        break
                elif opt == 7:
                    print("Logged out.")
                    break
                else:
                    print("Invalid choice.")
                    
    elif choice == 3:
        uname = input("Admin Username: ")
        pwd = input("Admin Password: ")
        admin = Admin()
        
        if uname == admin.username and pwd == admin.get_password():
            print("Admin login successful!")
            while True:
                print("\n--- Admin Menu ---")
                print("1. View All Students")
                print("2. Student Performance Chart")
                print("3. Add Question")
                print("4. Logout")
                
                try:
                    a_opt = int(input("Enter choice: "))
                except ValueError:
                    print("Invalid input.")
                    continue
                    
                if a_opt == 1:
                    view_all_students()
                elif a_opt == 2:
                    show_student_chart()
                elif a_opt == 3:
                    add_question()
                elif a_opt == 4:
                    print("Admin logged out.")
                    break
                else:
                    print("Invalid choice.")
        else:
            print("Invalid admin credentials.")
            
    elif choice == 4:
        print("Exiting. Goodbye!")
        break
    else:
        print("Invalid choice. Try again.")