import os
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

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

    # === 1. Generate PDF in memory ===
    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 750, "New Enquiry Form Submission")
    pdf.drawString(100, 730, f"Child Name: {child_name}")
    pdf.drawString(100, 710, f"Parent Name: {parent_name}")
    pdf.drawString(100, 690, f"Email: {email}")
    pdf.drawString(100, 670, f"Phone: {phone}")
    pdf.drawString(100, 650, f"Message: {message}")
    pdf.save()
    pdf_buffer.seek(0)

    # === 2. Email the PDF ===
    msg = Message(subject="New Enquiry Form Submission",
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[app.config['MAIL_USERNAME']])
    msg.body = f"New Enquiry received from {parent_name}."
    msg.attach("enquiry_form.pdf", "application/pdf", pdf_buffer.read())
    mail.send(msg)

    # === 3. Show Thank You + Print Option ===
    return render_template("thankyou.html", name=child_name, show_print=True)

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
    admission_to = request.form.getlist('admission_to')  # checkbox list
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

    # === 1. Generate PDF ===
    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
    pdf.setFont("Helvetica", 11)
    y = 770

    def draw_line(label, value):
        nonlocal y
        pdf.drawString(50, y, f"{label}: {value}")
        y -= 20

    draw_line("Form No", form_no)
    draw_line("Standard", standard)
    draw_line("Date", date)
    draw_line("Child's Name", child_name)
    draw_line("Date of Birth", dob)
    draw_line("Aadhar No", aadhar)
    draw_line("Father's Mobile", father_mobile)
    draw_line("Mother's Mobile", mother_mobile)
    draw_line("Admission To", ', '.join(admission_to))
    draw_line("Last School Attended", last_school)
    draw_line("Father's Name", father_name)
    draw_line("Father's Qualification", father_qualification)
    draw_line("Father's Occupation", father_occupation)
    draw_line("Father's Address", father_address)
    draw_line("Mother's Name", mother_name)
    draw_line("Mother's Qualification", mother_qualification)
    draw_line("Mother's Occupation", mother_occupation)
    draw_line("Mother's Address", mother_address)
    draw_line("Siblings", siblings)
    draw_line("Allergy", allergy)

    pdf.save()
    pdf_buffer.seek(0)

    # === 2. Send Email ===
    msg = Message(subject="New Admission Form Submission",
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[app.config['MAIL_USERNAME']])
    msg.body = f"New admission form submitted for {child_name}."
    msg.attach("admission_form.pdf", "application/pdf", pdf_buffer.read())
    mail.send(msg)

    # === 3. Redirect to Thank You with print option ===
    return render_template("thankyou.html", name=child_name, show_print=True)

if __name__ == '__main__':
    app.run(debug=True)
