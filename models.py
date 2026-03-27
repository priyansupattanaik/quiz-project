# -------------------------------------------------------
# models.py — OOP Class Definitions
# Requirement: OOP — Class, Inheritance, Encapsulation, Polymorphism
# -------------------------------------------------------

class User:
    """
    Base class.
    Covers: Class definition, Encapsulation (private __password),
    and the base form of Polymorphism via display_info().
    """
    def __init__(self, user_id, name, username):
        self.user_id  = user_id
        self.name     = name
        self.username = username

        # Encapsulation: private attribute (name mangling)
        self.__password = None

    # Setter — Encapsulation
    def set_password(self, password):
        try:
            self.__password = password
        except Exception as e:
            print(f"[MODEL ERROR] {e}")

    # Getter — Encapsulation
    def get_password(self):
        try:
            return self.__password
        except Exception as e:
            print(f"[MODEL ERROR] {e}")
            return None

    def display_info(self):
        # Polymorphism: base version
        try:
            print(f"User: {self.name} | Username: {self.username}")
        except Exception as e:
            print(f"[MODEL ERROR] {e}")


class QuizUser(User):
    """
    Child class — inherits from User.
    Demonstrates: Inheritance via super(), Polymorphism by overriding display_info().
    """
    def __init__(self, user_id, name, username):
        try:
            super().__init__(user_id, name, username)
            self.total_quizzes_taken = 0
        except Exception as e:
            print(f"[MODEL ERROR] QuizUser init failed: {e}")

    def display_info(self):
        # Polymorphism: overrides User.display_info()
        try:
            print(f"Welcome, {self.name.upper()} | Username: {self.username} | ID: {self.user_id}")
        except Exception as e:
            print(f"[MODEL ERROR] {e}")

    def load_stats_from_dict(self, stats_dict):
        """
        Updates internal stats from a dictionary.
        Requirement: dictionary data structure usage.
        """
        try:
            if "total_quizzes" in stats_dict:
                self.total_quizzes_taken = stats_dict["total_quizzes"]
        except Exception as e:
            print(f"[MODEL ERROR] {e}")


class Admin(User):
    """
    Admin class — also inherits from User.
    Demonstrates: Inheritance from same base class, Polymorphism via display_info().
    """
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin"

    def __init__(self):
        try:
            super().__init__(user_id=0, name="Administrator", username="admin")
            self.set_password(self.ADMIN_PASSWORD)
        except Exception as e:
            print(f"[MODEL ERROR] Admin init failed: {e}")

    def display_info(self):
        # Polymorphism: Admin's own version
        try:
            print(f"Admin Panel | Logged in as: {self.name.upper()}")
        except Exception as e:
            print(f"[MODEL ERROR] {e}")

    @staticmethod
    def check_credentials(username, password):
        """Static method to verify admin login."""
        return username == Admin.ADMIN_USERNAME and password == Admin.ADMIN_PASSWORD
