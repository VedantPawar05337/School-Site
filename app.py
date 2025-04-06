import os
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env (for local testing)

app = Flask(__name__)

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

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

@app.route('/thankyou')
def thankyou():
    name = request.args.get('name', 'User')
    return render_template('thankyou.html', name=name)

@app.route('/enquiry')
def enquiry_form():
    return render_template('enquiry.html')

@app.route('/submit_enquiry', methods=['POST'])
def submit_enquiry():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']

    # Send Email
    msg = Message(subject="New Enquiry Form Submission",
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[app.config['MAIL_USERNAME']])
    msg.body = f"""
    Enquiry Form Details:

    Name: {name}
    Email: {email}
    Phone: {phone}
    Message: {message}
    """
    mail.send(msg)

    return redirect(url_for('thankyou', name=name))

@app.route('/admission')
def admission_form():
    return render_template('admission.html')


@app.route('/submit_admission', methods=['POST'])
def submit_admission():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    dob = request.form['dob']
    address = request.form['address']
    father_name = request.form['father_name']
    mother_name = request.form['mother_name']

    msg = Message(subject="New Admission Form Submission",
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[app.config['MAIL_USERNAME']])
    msg.body = f"""
    Admission Form Details:

    Name: {name}
    Email: {email}
    Phone: {phone}
    DOB: {dob}
    Address: {address}
    Father's Name: {father_name}
    Mother's Name: {mother_name}
    """
    mail.send(msg)

    return redirect(url_for('thankyou', name=name))

if __name__ == '__main__':
    app.run(debug=True)
