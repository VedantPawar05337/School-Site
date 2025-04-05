from flask import Flask, render_template, request
import csv
import os
from datetime import datetime 

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/enquiry')
def enquiry():
    return render_template('enquiry.html')

@app.route('/submit_enquiry', methods=['POST'])
def submit_enquiry():
    if request.method == 'POST':
        child_name = request.form['child_name']
        parent_name = request.form['parent_name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        file_exists = os.path.isfile('enquiries.csv')

        # Write to CSV with headers if file doesn't exist
        with open('enquiries.csv', mode='a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Child Name', 'Parent Name', 'Email', 'Phone', 'Message', 'Date & Time'])
            writer.writerow([child_name, parent_name, email, phone, message, timestamp])

        return render_template('thankyou.html', parent_name=parent_name)
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/download_csv')
def download_csv():
    return send_file('enquiries.csv', as_attachment=True)

# @app.route('/submit_enquiry', methods=['POST'])
# def submit_enquiry():
#     if request.method == 'POST':
#         child_name = request.form['child_name']
#         parent_name = request.form['parent_name']
#         email = request.form['email']
#         phone = request.form['phone']
#         message = request.form['message']

#         # Write to CSV
#         with open('enquiries.csv', mode='a', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow([child_name, parent_name, email, phone, message])

#         return render_template('thankyou.html')



if __name__ == '__main__':
    app.run(debug=True)
