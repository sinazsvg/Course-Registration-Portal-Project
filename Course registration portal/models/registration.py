from utils.json_handler import JSONHandler
from models.course import Course
from models.user import User


class Registration:
    @staticmethod
    def enroll(student_username, course_id):
        # بررسی ظرفیت دوره
        course = Course.get_course_by_id(course_id)
        if not course:
            return False, "دوره یافت نشد"

        # بررسی پیش‌نیازها
        student = User.get_by_username(student_username)
        if not all(prereq in student.get('completed_courses', []) for prereq in course['prerequisites']):
            return False, "پیش‌نیازهای دوره تکمیل نشده"

        # ثبت‌نام
        registrations = JSONHandler.read_json('data/registrations.json')
        registrations.append({
            "student": student_username,
            "course_id": course_id
        })
        JSONHandler.write_json('data/registrations.json', registrations)
        return True, "ثبت‌نام با موفقیت انجام شد"

    @staticmethod
    def get_student_courses(username):
        registrations = JSONHandler.read_json('data/registrations.json')
        return [reg for reg in registrations if reg['student'] == username]