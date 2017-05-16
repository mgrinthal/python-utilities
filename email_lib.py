#!/usr/bin/python

import sys, smtplib, getpass, configparser

configParser = configparser.RawConfigParser()
configPath = './email-config.txt'
configParser.read(configPath)

emailAddress = configParser.get('email-config', 'address')

def send(subject, body):
  if not subject and not body:
    print('Error: Email message must have a subject line or body')
    sys.exit()

  smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
  connectionRes = smtpObj.ehlo()

  if connectionRes[0] == 250:
    # Successful connection, enable encryption
    smtpObj.starttls()
    password = getpass.getpass(prompt='Email account password: ')
    try:
      loginRes = smtpObj.login(emailAddress, password)
    except smtplib.SMTPException as err:
      print('Error occured: ' + str(err[0]) + ' ' + str(err[1]))
      smtpObj.quit()
      sys.exit()
    
    emailRes = smtpObj.sendmail(emailAddress, emailAddress,
                                'Subject: ' + str(subject) + '\n' + str(body))

    if emailRes:
      print('Mail delivery failed')

    smtpObj.quit()
  else:
    print('Error connecting to SMTP server')
    print(connectionRes)
