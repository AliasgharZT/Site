

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_mail import Mail, Message
import os
import datetime
import random
import re
import dns.resolver

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

# تنظیمات ایمیل
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'aliasgharzahdyanwork@gmail.com'  # ایمیل فرستنده
app.config['MAIL_PASSWORD'] = 'aiyv pyrj twny jnwv'  # رمز عبور یا App Password
mail = Mail(app)

# تابع برای اتصال به دیتابیس
def get_db_connection():
    db_path = os.path.join(BASE_DIR, 'static', 'data.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# تابع تولید کد پروژه
def generate_project_code():
    today = datetime.date.today()
    date_str = today.strftime("%Y/%m/%d")
    random_code = random.randint(1000, 9999)
    return f"{date_str}={random_code}"

@app.route('/switch_language/<language>')
def switch_language(language):
    if language == 'fa':
        return redirect(url_for('home', lang='fa'))
    elif language == 'en':
        return redirect(url_for('home', lang='en'))
    return redirect(url_for('home'))

@app.route('/')
def home():
    lang = request.args.get('lang', 'en')  # زبان پیش فرض 
    conn = get_db_connection()
    
    # دریافت پروژه‌های ثبت‌نام شده
    registered_projects = conn.execute('''
        SELECT * FROM registration 
        WHERE code NOT IN (SELECT code FROM done) 
        AND confirmation = 'F'
    ''').fetchall()

    # معکوس کردن پروژه‌های ثبت‌نام شده
    registered_projects.reverse()

    # تفکیک پروژه‌ها بر اساس زبان
    english_registered_projects = [project for project in registered_projects if project['language'] == 'en']
    farsi_registered_projects = [project for project in registered_projects if project['language'] == 'fa']
    
    # دریافت پروژه‌های در حال انجام
    registration_projects = conn.execute('''
        SELECT * FROM registration 
        WHERE code NOT IN (SELECT code FROM done) 
        AND confirmation = 'T'
    ''').fetchall()

    # معکوس کردن پروژه‌های در حال انجام
    registration_projects.reverse()

    # تفکیک پروژه‌ها بر اساس زبان
    farsi_projects = [project for project in registration_projects if project['language'] == 'fa']
    english_projects = [project for project in registration_projects if project['language'] == 'en']

    # دریافت پروژه‌های انجام‌شده (بدون نام کاربر)
    done_projects = conn.execute('''
        SELECT registration.info_project, registration.language 
        FROM registration 
        INNER JOIN done 
        ON registration.code = done.code
    ''').fetchall()

    # معکوس کردن پروژه‌های انجام‌شده
    done_projects.reverse()

    # تفکیک پروژه‌های انجام شده بر اساس زبان
    farsi_done_projects = [project for project in done_projects if project['language'] == 'fa']
    english_done_projects = [project for project in done_projects if project['language'] == 'en']

    # دریافت نظرات
    comments = conn.execute('SELECT * FROM comments').fetchall()

    # معکوس کردن نظرات
    comments.reverse()

    # تفکیک نظرات بر اساس زبان
    farsi_comments = [comment for comment in comments if comment['language'] == 'fa']
    english_comments = [comment for comment in comments if comment['language'] == 'en']

    conn.close()

    if lang == 'fa':
        return render_template(
            'index_fa.html', 
            farsi_projects=farsi_projects,
            farsi_done_projects=farsi_done_projects,
            farsi_comments=farsi_comments,
            farsi_registered_projects=farsi_registered_projects
        )
    else:
        return render_template(
            'index_en.html', 
            english_projects=english_projects,
            english_done_projects=english_done_projects,
            english_comments=english_comments,
            english_registered_projects=english_registered_projects,
        )


# تابع اعتبارسنجی ساختار ایمیل
def is_valid_email_format(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

# تابع اعتبارسنجی دامنه ایمیل (MX Record)
def is_valid_email_domain(email):
    try:
        domain = email.split('@')[1]  # استخراج دامنه از ایمیل
        mx_records = dns.resolver.resolve(domain, 'MX')  # جستجوی رکورد MX
        return len(mx_records) > 0
    except Exception:
        return False

# تابع ترکیبی برای اعتبارسنجی ایمیل
def is_valid_email(email):
    # بررسی ساختار ایمیل
    if not is_valid_email_format(email):
        return False
    
    # بررسی دامنه و رکوردهای MX
    if not is_valid_email_domain(email):
        return False
    
    return True
    
# ثبت پروژه
@app.route('/submit_project', methods=['POST'])
def submit_project():
    project_name = request.form.get('project_name')
    email = request.form.get('email')
    description = request.form.get('description')

    # اطمینان از پر بودن فیلدها
    if not project_name or not email or not description:
        return redirect(request.referrer)

    # اعتبارسنجی ایمیل
    if not is_valid_email(email):
        return redirect(request.referrer)

    # تشخیص زبان به صورت دستی از فیلد مخفی فرم
    language = request.form.get('language', 'en')

    # تولید کد پروژه
    project_code = generate_project_code()

    try:
        # ارسال ایمیل
        msg = Message(
            'New Project Submitted',
            sender=app.config['MAIL_USERNAME'],
            recipients=['aliasgharzahdyanwork@gmail.com']
        )
        msg.body = (
            f'New project submitted PERSONIQ:\n\n'
            f'Customer Name: {project_name}\n'
            f'Email: {email}\n'
            f'Project Description: {description}\n'
            f'Project Code: {project_code}'
        )
        mail.send(msg)

        # ذخیره داده‌ها در دیتابیس
        conn = get_db_connection()
        conn.execute('INSERT INTO registration (name, email, info_project, code, language, confirmation) VALUES (?, ?, ?, ?, ?, ?)',
                     (project_name, email, description, project_code, language, 'F'))
        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Error occurred: {e}")
        return redirect(request.referrer)

    return redirect(request.referrer)

# ثبت نظر
@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    name = request.form['name']
    comment = request.form['comment']

    # اطمینان از پر بودن فیلدها
    if not name or not comment:
        return redirect(request.referrer)

    # تشخیص زبان به صورت دستی از فیلد مخفی فرم
    language = request.form.get('language', 'en')

    try:
        # ذخیره داده‌ها در دیتابیس
        conn = get_db_connection()
        conn.execute('INSERT INTO comments (name, comment, language) VALUES (?, ?, ?)', (name, comment, language))
        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Error occurred: {e}")
        return redirect(request.referrer)

    return redirect(request.referrer)


if __name__ == '__main__':
    app.run(debug=True)


