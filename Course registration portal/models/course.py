from utils.json_handler import JSONHandler


class Course:
    def __init__(self, course_id, title, schedule, capacity, prerequisites=None):
        self.course_id = course_id
        self.title = title
        self.schedule = schedule
        self.capacity = capacity
        self.prerequisites = prerequisites or []

    def save(self):
        courses = JSONHandler.read_json('data/courses.json')
        courses.append(self.__dict__)
        JSONHandler.write_json('data/courses.json', courses)

    @staticmethod
    def get_all_courses():
        return JSONHandler.read_json('data/courses.json')

    @staticmethod
    def get_course_by_id(course_id):
        courses = Course.get_all_courses()
        for course in courses:
            if course['course_id'] == course_id:
                return course
        return None