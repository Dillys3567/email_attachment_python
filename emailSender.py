from email.message import EmailMessage
import ssl
import smtplib
import mysql.connector
import pandas as pd
import schedule

#function to pull data from local db and send as a csv via email
def pull_data_send_email():
    #connect to database
    db=mysql.connector.connect(user='root',database='databaseName',password='databasePassword')
    cursor=db.cursor()
    query='select value1,value2 from databaseName.tableName'
    cursor.execute(query)
    table_data=cursor.fetchall()
    value1List=[]
    value2List=[]

    for value1,value2 in table_data:
        value1List.append(value1)
        value2List.append(value2)

    #convert data retrieved into a csv file
    table_data={'value1':value1List,'value2':value2List}
    df=pd.DataFrame(table_data)
    df=df.to_csv('path for resulting csv file. could be in the same directory as the python file')


    #define email components
    email_Sender='senderEmail'
    sender_password='senderPassword(you can generate an app password for this in your google account)'
    #list of recipient emails 
    email_Recipients=['user1@gmail.com','user1@gmail.com']
    body='the email body message goes here'
    subject='the subject of the email'
    
    email= EmailMessage()
    email['From']=email_Sender
    email['To']=','.join(email_Recipients)
    email['Subject']=subject
    email.set_content(body)

    #open resulting csv file and add as an attachment
    with open('path for csv file you wish to attach','rb') as f:
        filedata=f.read()
        file_name=f.name
        email.add_attachment(filedata,maintype='application',subtype='xlsx',filename=file_name)


    context=ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(email_Sender,sender_password)
        smtp.sendmail(email_Sender,email_Recipients,email.as_string())



#schedule to call function every 12 hours
schedule.every(12).hour.do(pull_data_send_email)

while True:
    schedule.run_pending()
