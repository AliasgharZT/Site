
from flask import Flask
from flask_mail import Mail, Message
import time 

app = Flask(__name__)

# تنظیمات SMTP
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'aliasgharzahdyanwork@gmail.com'  # ایمیل فرستنده
app.config['MAIL_PASSWORD'] = 'aiyv pyrj twny jnwv'  # رمز عبور یا App Password

mail = Mail(app)

# ارسال ایمیل
with app.app_context():
    try:
        msg = Message(
            subject="Testing email from Flask",  # موضوع ایمیل
            sender=app.config['MAIL_USERNAME'],  # فرستنده
            recipients=['aliasgharzahdyanwork@gmail.com'],  # گیرنده
            body="Hello, this is a test email!"  # متن ایمیل
        )
        mail.send(msg)
        print("Email sent successfully!")
        time.sleep(7)
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(7)
        

