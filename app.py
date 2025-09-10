from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
import logging
from datetime import datetime
from functools import wraps

# تنظیمات اولیه
app = Flask(__name__)
app.secret_key = 'your_very_secret_key_here'
app.config['TEMPLATES_AUTO_RELOAD'] = True

# تنظیمات لاگ‌گیری
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

# مسیر فایل‌های داده
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
COURSES_FILE = os.path.join(DATA_DIR, 'courses.json')
REGISTRATIONS_FILE = os.path.join(DATA_DIR, 'registrations.json')
ADMIN_IDS_FILE = os.path.join(DATA_DIR, 'admin_ids.json')

# ایجاد پوشه داده اگر وجود ندارد
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# مقداردهی اولیه فایل‌های JSON
files_to_init = [
    USERS_FILE, COURSES_FILE, REGISTRATIONS_FILE, ADMIN_IDS_FILE
]

for file_path in files_to_init:
    if not os.path.exists(file_path):
        default_data = []
        if file_path == ADMIN_IDS_FILE:
            default_data = ["ADM-001", "ADM-002", "ADM-003"]
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False)


# --- توابع کمکی ---
def load_json(file_path):
    """بارگیری داده از فایل JSON"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"خطا در خواندن {file_path}: {str(e)}")
        return []


def save_json(file_path, data):
    """ذخیره داده در فایل JSON"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"خطا در نوشتن {file_path}: {str(e)}")
        return False


def login_required(role=None):
    """دکوراتور برای نیاز به احراز هویت"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                flash('لطفاً ابتدا وارد سیستم شوید', 'warning')
                return redirect(url_for('login'))

            if role and session['user'].get('role') != role:
                flash('شما مجوز دسترسی به این صفحه را ندارید', 'danger')
                return redirect(url_for('dashboard'))

            return f(*args, **kwargs)

        return decorated_function

    return decorator


# --- مسیرهای اصلی برنامه ---
@app.route('/')
def home():
    """صفحه اصلی"""
    courses = load_json(COURSES_FILE)
    return render_template('index.html', courses=courses)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """صفحه ثبت‌نام کاربر"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']

        # بررسی وجود کاربر
        users = load_json(USERS_FILE)
        if any(user['username'] == username for user in users):
            flash('نام کاربری قبلاً استفاده شده است', 'danger')
            return render_template('register.html')

        # ایجاد کاربر جدید
        new_user = {
            'username': username,
            'password': password,
            'email': email,
            'role': role,
            'created_at': datetime.now().isoformat()
        }

        # افزودن فیلدهای اختصاصی دانشجو
        if role == 'student':
            student_id = request.form.get('student_id', '').strip()
            if not student_id:
                flash('شماره دانشجویی الزامی است', 'danger')
                return render_template('register.html')
            new_user['student_id'] = student_id

        # ذخیره کاربر
        users.append(new_user)
        save_json(USERS_FILE, users)

        logger.info(f"کاربر جدید ثبت نام کرد: {username} ({role})")
        flash('ثبت‌نام با موفقیت انجام شد. لطفاً وارد شوید', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """صفحه ورود به سیستم"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin_id = request.form.get('admin_id', '').strip()  # دریافت شناسه مدیر

        users = load_json(USERS_FILE)
        user = next((u for u in users if u['username'] == username and u['password'] == password), None)

        if user:
            # اگر کاربر مدیر باشد، بررسی شناسه مدیر
            if user['role'] == 'administrator':
                admin_ids = load_json(ADMIN_IDS_FILE)

                if not admin_id:
                    flash('برای ورود به عنوان مدیر، شناسه مدیر الزامی است', 'danger')
                    return render_template('login.html')

                if admin_id not in admin_ids:
                    flash('شناسه مدیر نامعتبر است', 'danger')
                    return render_template('login.html')

                # ذخیره شناسه مدیر در سشن
                user['admin_id'] = admin_id

            # ورود کاربر
            session['user'] = user
            logger.info(f"کاربر وارد شد: {username}")
            return redirect(url_for('dashboard'))
        else:
            flash('نام کاربری یا رمز عبور اشتباه است', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    """خروج از سیستم"""
    if 'user' in session:
        user = session['user']
        role_info = f"{user['role']}"
        if user['role'] == 'administrator' and 'admin_id' in user:
            role_info += f" (شناسه: {user['admin_id']})"

        logger.info(f"کاربر خارج شد: {user['username']} - {role_info}")
        session.pop('user', None)
        flash('با موفقیت از سیستم خارج شدید', 'success')
    return redirect(url_for('home'))


@app.route('/dashboard')
@login_required()
def dashboard():
    """داشبورد کاربری"""
    user = session['user']
    courses = load_json(COURSES_FILE)
    registrations = load_json(REGISTRATIONS_FILE)

    # دریافت دوره‌های ثبت‌نام شده کاربر
    user_registrations = [r for r in registrations if r['username'] == user['username']]
    user_courses = [
        course for course in courses
        if any(r['course_id'] == course['course_id'] for r in user_registrations)
    ]

    return render_template('dashboard.html',
                           user=user,
                           courses=courses,
                           user_courses=user_courses)


@app.route('/profile')
@login_required()
def profile():
    """صفحه پروفایل کاربر"""
    user = session['user']

    # دریافت اطلاعات تکمیلی کاربر
    users = load_json(USERS_FILE)
    user_details = next((u for u in users if u['username'] == user['username']), None)

    if not user_details:
        flash('اطلاعات کاربر یافت نشد', 'danger')
        return redirect(url_for('dashboard'))

    # دریافت دوره‌های ثبت‌نام شده کاربر (فقط برای دانشجویان)
    user_courses = []
    if user['role'] == 'student':
        registrations = load_json(REGISTRATIONS_FILE)
        courses = load_json(COURSES_FILE)

        if registrations:
            user_registrations = [r for r in registrations if r['username'] == user['username']]
            user_courses = [
                course for course in courses
                if any(r['course_id'] == course['course_id'] for r in user_registrations)
            ]

    return render_template('profile.html',
                           user=user_details,
                           courses=user_courses)


@app.route('/enroll', methods=['POST'])
@login_required(role='student')
def enroll():
    """ثبت‌نام در دوره"""
    user = session['user']
    course_id = request.form['course_id']
    username = user['username']

    courses = load_json(COURSES_FILE)
    course = next((c for c in courses if c['course_id'] == course_id), None)

    if not course:
        flash('دوره مورد نظر یافت نشد', 'danger')
        return redirect(url_for('dashboard'))

    # بررسی تداخل زمانی
    registrations = load_json(REGISTRATIONS_FILE)
    user_registrations = [r for r in registrations if r['username'] == username]
    user_courses = [c for c in courses if any(r['course_id'] == c['course_id'] for r in user_registrations)]

    # بررسی تداخل زمانی
    for user_course in user_courses:
        if user_course['schedule'] == course['schedule']:
            flash(f'تداخل زمانی با دوره: {user_course["title"]}', 'danger')
            return redirect(url_for('dashboard'))

    # ثبت‌نام جدید
    new_registration = {
        'username': username,
        'course_id': course_id,
        'registered_at': datetime.now().isoformat()
    }

    registrations.append(new_registration)
    save_json(REGISTRATIONS_FILE, registrations)

    logger.info(f"کاربر {username} در دوره {course_id} ثبت نام کرد")
    flash('ثبت‌نام در دوره با موفقیت انجام شد', 'success')
    return redirect(url_for('dashboard'))


@app.route('/payment/<course_id>', methods=['GET', 'POST'])
@login_required(role='student')
def payment(course_id):
    """صفحه پرداخت برای دوره"""
    user = session['user']
    courses = load_json(COURSES_FILE)
    course = next((c for c in courses if c['course_id'] == course_id), None)

    if not course:
        flash('دوره مورد نظر یافت نشد', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        if course['price'] == 0:
            # ثبت‌نام مستقیم برای دوره‌های رایگان
            success, message = enroll_user(user['username'], course_id)
            if success:
                flash('پرداخت با موفقیت انجام شد و دوره به پروفایل شما اضافه شد', 'success')
            else:
                flash(message, 'danger')
            return redirect(url_for('profile'))
        else:
            # برای دوره‌های پولی
            card_number = request.form['card_number']
            cvv2 = request.form['cvv2']
            expiry_date = request.form['expiry_date']

            # اینجا می‌توانید پرداخت را واقعی کنید، اما طبق خواسته شما:
            flash('خوشبختانه خرید موفقیت آمیز نبود و ما کلاهبرداری کردیم 3>', 'danger')
            return redirect(url_for('home'))

    return render_template('payment.html', course=course)


def enroll_user(username, course_id):
    """ثبت‌نام کاربر در دوره (تابع کمکی)"""
    courses = load_json(COURSES_FILE)
    course = next((c for c in courses if c['course_id'] == course_id), None)

    if not course:
        return False, "دوره یافت نشد"

    # بررسی تداخل زمانی
    registrations = load_json(REGISTRATIONS_FILE)
    user_registrations = [r for r in registrations if r['username'] == username]
    user_courses = [c for c in courses if any(r['course_id'] == c['course_id'] for r in user_registrations)]

    for user_course in user_courses:
        if user_course['schedule'] == course['schedule']:
            return False, f'تداخل زمانی با دوره: {user_course["title"]}'

    # ثبت‌نام جدید
    new_registration = {
        'username': username,
        'course_id': course_id,
        'registered_at': datetime.now().isoformat()
    }

    registrations.append(new_registration)
    save_json(REGISTRATIONS_FILE, registrations)

    logger.info(f"کاربر {username} در دوره {course_id} ثبت نام کرد")
    return True, "ثبت‌نام با موفقیت انجام شد"


# --- مدیریت دوره‌ها (فقط برای مدیران) ---
@app.route('/admin/courses')
@login_required(role='administrator')
def manage_courses():
    """مدیریت دوره‌ها (فقط مدیران)"""
    user = session['user']
    logger.info(f"مدیر وارد بخش مدیریت دوره‌ها شد: {user['username']} (شناسه: {user.get('admin_id', 'N/A')})")

    courses = load_json(COURSES_FILE)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')

    return render_template(
        'admin_courses.html',
        courses=courses,
        current_time=current_time  # پاس دادن زمان به صورت رشته
    )


@app.route('/admin/create_course', methods=['GET', 'POST'])
@login_required(role='administrator')
def create_course():
    """ایجاد دوره جدید توسط مدیر"""
    user = session['user']

    if request.method == 'POST':
        course_id = request.form['course_id']
        title = request.form['title']
        schedule = request.form['schedule']
        capacity = int(request.form['capacity'])
        prerequisites = request.form.get('prerequisites', '')
        description = request.form.get('description', '')
        price = float(request.form.get('price', 0))  # دریافت قیمت

        # تبدیل پیش‌نیازها به لیست
        if prerequisites:
            prerequisites = [p.strip() for p in prerequisites.split(',')]
        else:
            prerequisites = []

        courses = load_json(COURSES_FILE)

        # بررسی وجود دوره
        if any(c['course_id'] == course_id for c in courses):
            flash('کد دوره تکراری است', 'danger')
            return render_template('create_course.html')

        # ایجاد دوره جدید
        new_course = {
            'course_id': course_id,
            'title': title,
            'schedule': schedule,
            'capacity': capacity,
            'prerequisites': prerequisites,
            'description': description,
            'price': price,
            'created_by': user['username'],
            'created_by_admin_id': user.get('admin_id', 'N/A'),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }

        courses.append(new_course)
        save_json(COURSES_FILE, courses)

        logger.info(
            f"مدیر {user['username']} (شناسه: {user.get('admin_id', 'N/A')}) دوره جدید ایجاد کرد: {title} ({course_id})")
        flash('دوره جدید با موفقیت ایجاد شد', 'success')
        return redirect(url_for('manage_courses'))

    return render_template('create_course.html')


@app.route('/admin/edit_course/<course_id>', methods=['GET', 'POST'])
@login_required(role='administrator')
def edit_course(course_id):
    """ویرایش دوره توسط مدیر"""
    user = session['user']
    courses = load_json(COURSES_FILE)
    course_to_edit = next((c for c in courses if c['course_id'] == course_id), None)

    if not course_to_edit:
        flash('دوره مورد نظر یافت نشد', 'danger')
        return redirect(url_for('manage_courses'))

    if request.method == 'POST':
        # دریافت داده‌های ویرایش شده
        title = request.form['title']
        schedule = request.form['schedule']
        capacity = int(request.form['capacity'])
        prerequisites = request.form.get('prerequisites', '')
        description = request.form.get('description', '')
        price = float(request.form.get('price', 0))  # دریافت قیمت

        # تبدیل پیش‌نیازها به لیست
        if prerequisites:
            prerequisites = [p.strip() for p in prerequisites.split(',')]
        else:
            prerequisites = []

        # به‌روزرسانی دوره
        course_to_edit['title'] = title
        course_to_edit['schedule'] = schedule
        course_to_edit['capacity'] = capacity
        course_to_edit['prerequisites'] = prerequisites
        course_to_edit['description'] = description
        course_to_edit['price'] = price
        course_to_edit['updated_at'] = datetime.now().isoformat()

        save_json(COURSES_FILE, courses)

        logger.info(
            f"مدیر {user['username']} (شناسه: {user.get('admin_id', 'N/A')}) دوره را ویرایش کرد: {title} ({course_id})")
        flash('دوره با موفقیت به‌روزرسانی شد', 'success')
        return redirect(url_for('manage_courses'))

    return render_template('edit_course.html', course=course_to_edit)


@app.route('/admin/delete_course/<course_id>', methods=['POST'])
@login_required(role='administrator')
def delete_course(course_id):
    """حذف دوره توسط مدیر"""
    user = session['user']
    courses = load_json(COURSES_FILE)
    registrations = load_json(REGISTRATIONS_FILE)

    # پیدا کردن دوره برای نمایش عنوان
    course = next((c for c in courses if c['course_id'] == course_id), None)

    if not course:
        flash('دوره مورد نظر یافت نشد', 'warning')
        return redirect(url_for('manage_courses'))

    # حذف دوره
    new_courses = [c for c in courses if c['course_id'] != course_id]
    save_json(COURSES_FILE, new_courses)

    # حذف ثبت‌نام‌های مرتبط
    new_registrations = [r for r in registrations if r.get('course_id') != course_id]
    save_json(REGISTRATIONS_FILE, new_registrations)

    logger.info(
        f"مدیر {user['username']} (شناسه: {user.get('admin_id', 'N/A')}) دوره را حذف کرد: {course['title']} ({course_id})")
    flash(f'دوره "{course["title"]}" با موفقیت حذف شد', 'success')
    return redirect(url_for('manage_courses'))


@app.route('/admin/enrollments_report')
@login_required(role='administrator')
def enrollments_report():
    """گزارش ثبت‌نام‌های کاربران"""
    user = session['user']
    logger.info(f"مدیر وارد بخش گزارش ثبت‌نام‌ها شد: {user['username']} (شناسه: {user.get('admin_id', 'N/A')})")

    # دریافت تمام داده‌ها
    registrations = load_json(REGISTRATIONS_FILE)
    users = load_json(USERS_FILE)
    courses = load_json(COURSES_FILE)

    # ایجاد لیست گزارش با اطلاعات کامل
    enrollment_list = []
    for reg in registrations:
        user_info = next((u for u in users if u['username'] == reg['username']), None)
        course_info = next((c for c in courses if c['course_id'] == reg['course_id']), None)

        if user_info and course_info:
            enrollment_list.append({
                'username': reg['username'],
                'student_id': user_info.get('student_id', 'نامشخص'),
                'course_id': reg['course_id'],
                'course_title': course_info['title'],
                'registration_date': reg.get('registered_at', 'نامشخص')
            })

    # اضافه کردن زمان فعلی برای نمایش در قالب
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')

    return render_template('enrollments_report.html',
                           enrollments=enrollment_list,
                           current_time=current_time)  # پاس دادن زمان به قالب


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=True)