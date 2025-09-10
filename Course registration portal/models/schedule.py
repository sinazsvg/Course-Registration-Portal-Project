from models.registration import Registration
from models.course import Course


class ScheduleManager:
    @staticmethod
    def has_time_conflict(student_username, new_course_id):
        # دریافت تمام دوره‌های ثبت‌نام شده دانشجو
        student_courses = Registration.get_student_courses(student_username)

        # دریافت زمانبندی دوره جدید
        new_course = Course.get_course_by_id(new_course_id)
        if not new_course:
            return False

        # بررسی تداخل با دوره‌های موجود
        for reg in student_courses:
            course = Course.get_course_by_id(reg['course_id'])
            if course['schedule'] == new_course['schedule']:
                return True
        return False

    @staticmethod
    def generate_schedule(student_username):
        student_courses = Registration.get_student_courses(student_username)
        schedule = {}

        for reg in student_courses:
            course = Course.get_course_by_id(reg['course_id'])
            if course:
                day, time = course['schedule'].split(' ')
                if day not in schedule:
                    schedule[day] = []
                schedule[day].append({
                    'title': course['title'],
                    'time': time
                })

        return schedule