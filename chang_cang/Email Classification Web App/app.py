from flask import Flask,request,render_template,send_file
import pickle
import numpy as np
import pandas as pd
import os

import smtplib
import time
import imaplib
import email
import traceback

from flask import Flask,render_template, request
from flask_mysqldb import MySQL

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
df = pd.read_csv("EmailDataSet.csv")
X_train = vectorizer.fit_transform(df)
email_model=pickle.load(open('EmailModel.pkl','rb'))


def classify_spam(arr):
  output = email_model.predict(vectorizer.transform([arr]))
  str1 =  ""
  
  for index_instance,instance in enumerate(classify_spam(messages)):
    str1 = instance
  return str1

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'hack'
app.config['MYSQL_PASSWORD'] = 'hack@2021'
app.config['MYSQL_DB'] = 'flask'



mysql = MySQL(app)

# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------



ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "changanghack21" + ORG_EMAIL
FROM_PWD = "changang123"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993



def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id,first_email_id, -1):
            data = mail.fetch(str(i), '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1],'utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print('From : ' + email_from + '\n')
                    print('Subject : ' + email_subject + '\n')

    except Exception as e:
        traceback.print_exc()
        print(str(e))

read_email_from_gmail()

str = classify_spam("Akalanaka")
print(str)





app = Flask(__name__)


@app.route('/')
def home():
    return render_template('homepage.html')



if __name__ == "__main__":
    app.run(debug = True)
