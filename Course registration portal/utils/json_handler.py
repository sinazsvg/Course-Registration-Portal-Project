import json
class JSONHandler:
    @staticmethod
    def read_json(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:  # اضافه کردن encoding='utf-8'
            return json.load(file)

    @staticmethod
    def write_json(file_path, data):
        with open(file_path, 'w', encoding='utf-8') as file:  # اضافه کردن encoding='utf-8'
            json.dump(data, file, indent=4,
                      ensure_ascii=False)  # غیرفعال کردن ensure_ascii برای پشتیبانی از کاراکترهای غیرلاتین