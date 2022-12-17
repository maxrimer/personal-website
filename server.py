from flask import Flask, render_template, url_for, request, redirect
import csv
import smtplib
from email.message import EmailMessage
from credentials import user, password

app = Flask(__name__)


@app.route('/')
def my_home():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_pages(page_name):
    return render_template(page_name)


# def write_to_database(data):
#     with open('database.txt', mode='a') as database:
#         email = data.get('email')
#         subject = data.get('subject')
#         message = data.get('message')
#         file = database.write(f'\n{email},{subject},{message}')


def write_to_csv_and_email(data):
    with open('database.csv', newline='', mode='a') as database2:
        email_sender = data.get('email')
        subject = data.get('subject')
        message = data.get('message')
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email_sender, subject, message])
    email = EmailMessage()
    email['from'] = 'Maxim Rimer'
    email['to'] = 'maximrimer96@gmail.com'
    email['subject'] = 'You got a message from your website'

    email.set_content(f'You received a message from {email_sender} and the subject is {subject}.\n'
                      f'The message is: {message}. \nPlease check the database for the details.')

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(user=user, password=password)
        smtp.send_message(email)


@app.route('/submit_form', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv_and_email(data)
            return redirect('/gratitude.html')
        except:
            return 'Did not save to database.'
    else:
        return 'Something went wrong. Please try again later.'
