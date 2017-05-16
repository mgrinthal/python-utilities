#!/usr/bin/python

import sys
import smtplib
import getpass
# import argparse

# parser = argparse.ArgumentParser(description='Send an email.')
# parser.add_argument('subject', metavar='subj', type=str, help='Email subject line')
# parser.add_argument('body', metavar='body', nargs='+', type=str, help='Email body')
# args = parser.parse_args()

# args.body = ' '.join(args.body);

# print args.subject
# print args.body

def send(subject, body):
  if not subject and not body:
    print 'Error: Email message must have a subject line or body'
    sys.exit()

  smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
  connectionRes = smtpObj.ehlo()

  if connectionRes[0] == 250:
    # Successful connection, enable encryption
    smtpObj.starttls()
    password = getpass.getpass(prompt='Email account password: ')
    try:
      loginRes = smtpObj.login('mgrinthal2@gmail.com', password)
    except smtplib.SMTPException as err:
      print 'Error occured: ' + str(err[0]) + ' ' + str(err[1])
      smtpObj.quit()
      sys.exit()
    
    emailRes = smtpObj.sendmail('mgrinthal2@gmail.com', 'mgrinthal2@gmail.com',
                                'Subject: ' + str(subject) + '\n' + str(body))

    if emailRes:
      print 'Mail delivery failed'

    smtpObj.quit()
  else:
    print 'Error connecting to SMTP server'
    print connectionRes
