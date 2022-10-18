from email.message import EmailMessage
import ssl
import smtplib
import mysql.connector
import pandas as pd
import schedule

#function to pull data from local db and send as a csv via email
def pull_data_send_email():
    #connect to database
    db=mysql.connector.connect(user='root',database='college',password='mysqldillys_3')
    cursor=db.cursor()
    query='select name,email from college.lecturers'
    cursor.execute(query)
    table_data=cursor.fetchall()
    names=[]
    emails=[]

    for name,email in table_data:
        names.append(name)
        emails.append(email)

    #convert data retrieved into a csv file
    table_data={'name':names,'email':emails}
    df=pd.DataFrame(table_data)
    df=df.to_csv('C:/Users/HP/Desktop/Xpress task/result.csv')


    #define email components
    email_Sender='d'
    sender_password='p'
    email_Recipients=['annandillys@gmail.com']
    body='These are the customers holding assets beyond 30 days. Do something about it.Now now'
    subject='Stubborn Customers'
    
    email= EmailMessage()
    email['From']=email_Sender
    email['To']=','.join(email_Recipients)
    email['Subject']=subject
    email.set_content(body)

    #open resulting csv file and add as an attachment
    with open('result.csv','rb') as f:
        filedata=f.read()
        file_name=f.name
        email.add_attachment(filedata,maintype='application',subtype='xlsx',filename=file_name)


    context=ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(email_Sender,sender_password)
        smtp.sendmail(email_Sender,email_Recipients,email.as_string())
        print('done')


#schedule to call function every 12 hours
schedule.every(12).hour.do(pull_data_send_email)

while True:
    schedule.run_pending()
