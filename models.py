# oop classes
class User:
    def __init__(self, uid, name, username):
        self.uid = uid
        self.name = name
        self.username = username
        self.__password = None  # private variable (encapsulation)

    def set_password(self, pwd):
        self.__password = pwd

    def get_password(self):
        return self.__password

    def display(self):
        print(f"ID: {self.uid} | Name: {self.name} | Username: {self.username}")


class QuizUser(User):
    # inheritance
    def __init__(self, uid, name, username):
        super().__init__(uid, name, username)
        self.total_quizzes = 0

    # polymorphism (overriding the base method)
    def display(self):
        print(f"Student: {self.name} | Username: {self.username}")

    def load_stats(self, data_dict):
        # uses dictionary as requested
        if "quizzes" in data_dict:
            self.total_quizzes = data_dict["quizzes"]


class Admin(User):
    def __init__(self):
        super().__init__(0, "Admin", "admin")
        self.set_password("admin")

    def display(self):
        print("--- Admin Dashboard ---")