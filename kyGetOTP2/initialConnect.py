import email # for converting bytes object to python's email.message object
import imaplib # used for connecting to mail server

import datetime # for checking time

user = "keyyayatrading02@gmail.com"
password = "abhuydppyrguvjoz" # a special app password, gmail has policy for using its mail for other application
# to manage your app password, here: https://myaccount.google.com/apppasswords
host = "imap.gmail.com" 
# the imap server for gmail, you need to have SSL certificate if you want to host your own mail handling server, 
# for security reason, gmail disable any usage of its mail that is not connect through SSL

# make a SSL connection with the host
connection = imaplib.IMAP4_SSL(host) # using SSL connection
# login to your mail
connection.login(user, password)

# select a category of your inbox (can be spam, deleted...)
# to check available inbox, use `connection.list()`
connection.select("INBOX")