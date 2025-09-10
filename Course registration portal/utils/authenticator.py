from models.user import User

class Authenticator:
    @staticmethod
    def authenticate(username, password):
        user_data = User.get_by_username(username)
        if user_data and user_data['password'] == password:
            # ایجاد شیء مناسب بر اساس نقش
            if user_data['role'] == 'student':
                return Student(user_data['username'],
                              user_data['password'],
                              user_data['email'],
                              user_data['student_id'])
            elif user_data['role'] == 'administrator':
                return Administrator(user_data['username'],
                                    user_data['password'],
                                    user_data['email'],
                                    user_data['admin_id'])
        return None