from utils.json_handler import JSONHandler

class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.role = "user"

    def save(self):
        users = JSONHandler.read_json('data/users.json')
        users.append(self.__dict__)
        JSONHandler.write_json('data/users.json', users)

    @staticmethod
    def get_by_username(username):
        users = JSONHandler.read_json('data/users.json')
        for user in users:
            if user['username'] == username:
                return user
        return None

class Student(User):
    def __init__(self, username, password, email, student_id):
        super().__init__(username, password, email)
        self.role = "student"
        self.student_id = student_id
        self.enrolled_courses = []

class Administrator(User):
    def __init__(self, username, password, email, admin_id):
        super().__init__(username, password, email)
        self.role = "administrator"
        self.admin_id = admin_id