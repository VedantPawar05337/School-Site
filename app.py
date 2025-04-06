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
    child_name = request.form['child_name']
    parent_name = request.form['parent_name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']

    # Send Email
    msg = Message(subject="New Enquiry Form Submission",
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[app.config['MAIL_USERNAME']])
    msg.body = f"""
    Enquiry Form Details:

    Child's Name: {child_name}
    Parent's Name: {parent_name}
    Email: {email}
    Phone: {phone}
    Message: {message}
    """
    mail.send(msg)

    return redirect(url_for('thankyou', name=child_name))

@app.route('/admission')
def admission_form():
    return render_template('admission.html')

@app.route('/submit_admission', methods=['POST'])
def submit_admission():
    form_no = request.form['form_no']
    standard = request.form['standard']
    date = request.form['date']
    child_name = request.form['child_name']
    dob = request.form['dob']
    aadhar = request.form['aadhar']
    father_mobile = request.form['father_mobile']
    mother_mobile = request.form['mother_mobile']
    admission_to = request.form.getlist('admission_to')  # checkboxes return a list
    last_school = request.form['last_school']
    father_name = request.form['father_name']
    father_qualification = request.form['father_qualification']
    father_occupation = request.form['father_occupation']
    father_address = request.form['father_address']
    mother_name = request.form['mother_name']
    mother_qualification = request.form['mother_qualification']
    mother_occupation = request.form['mother_occupation']
    mother_address = request.form['mother_address']
    siblings = request.form['siblings']
    allergy = request.form['allergy']

    # Prepare the message
    msg = Message(subject="New Admission Form Submission",
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[app.config['MAIL_USERNAME']])
    msg.body = f"""
    Admission Form Submission:

    Form No: {form_no}
    Standard: {standard}
    Date: {date}
    Child Name: {child_name}
    Date of Birth: {dob}
    Aadhar No: {aadhar}
    Father's Mobile: {father_mobile}
    Mother's Mobile: {mother_mobile}
    Admission Sought To: {', '.join(admission_to)}
    Last School Attended: {last_school}

    Father's Name: {father_name}
    Father's Qualification: {father_qualification}
    Father's Occupation: {father_occupation}
    Father's Occupation Address: {father_address}

    Mother's Name: {mother_name}
    Mother's Qualification: {mother_qualification}
    Mother's Occupation: {mother_occupation}
    Mother's Occupation Address: {mother_address}

    Siblings Studying In: {siblings}
    Allergies/Sickness: {allergy}
    """

    mail.send(msg)

    return redirect(url_for('thankyou', name=child_name))


if __name__ == '__main__':
    app.run(debug=True)
