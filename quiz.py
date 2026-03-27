import csv
import os
from validators import validate_answer

# quiz loop and csv handling
def start_quiz():
    score = 0
    total = 0
    
    try:
        with open("questions.csv", "r") as f:
            reader = csv.reader(f)
            next(reader) # skip header
            
            for row in reader:
                if len(row) < 6:
                    continue
                
                total += 1
                print(f"\nQ{total}: {row[0]}")
                print(f"1. {row[1]}")
                print(f"2. {row[2]}")
                print(f"3. {row[3]}")
                print(f"4. {row[4]}")
                
                while True:
                    ans = input("Your answer (1-4): ")
                    if validate_answer(ans):
                        break
                    print("Please enter 1, 2, 3 or 4.")
                
                selected = row[int(ans)].strip()
                correct = row[5].strip()
                
                if selected == correct:
                    print("Correct!")
                    score += 1
                else:
                    print(f"Wrong. Answer is {correct}")
                    
    except FileNotFoundError:
        print("questions.csv not found!")
        return 0, 0
        
    return score, total


def export_csv(username, score, total):
    file_exists = os.path.exists("results.csv")
    with open("results.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Username", "Score", "Total"])
        writer.writerow([username, score, total])