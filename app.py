from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  # Your Gmail
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')  # Gmail App Password

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/admission')
def admission():
    return render_template('admission.html')

# --- Enquiry Form Submission ---
@app.route('/submit_enquiry', methods=['POST'])
def submit_enquiry():
    name = request.form['name']
    dob = request.form['dob']
    mobile_father = request.form['mobile_father']
    mobile_mother = request.form['mobile_mother']

    msg = Message(subject='📩 New Enquiry Submission',
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[app.config['MAIL_USERNAME']],
                  body=f'''New enquiry received:

👶 Name: {name}
🎂 Date of Birth: {dob}
📱 Father’s Mobile: {mobile_father}
📱 Mother’s Mobile: {mobile_mother}
''')
    mail.send(msg)
    return render_template('thankyou.html', name=name)

# --- Admission Form Submission ---
@app.route('/submit_admission', methods=['POST'])
def submit_admission():
    student_name = request.form['student_name']
    dob = request.form['dob']
    address = request.form['address']
    email = request.form['email']
    phone = request.form['phone']
    parent_name = request.form['parent_name']

    msg = Message(subject='📝 New Admission Form Submission',
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[app.config['MAIL_USERNAME']],
                  body=f'''New admission form submitted:

👦 Student Name: {student_name}
🎂 DOB: {dob}
🏠 Address: {address}
📧 Email: {email}
📞 Phone: {phone}
👨‍👩‍👧 Parent/Guardian: {parent_name}
''')
    mail.send(msg)
    return render_template('thankyou.html', name=student_name)
