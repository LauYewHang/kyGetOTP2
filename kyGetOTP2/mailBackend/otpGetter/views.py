import sys # for setting directory
sys.path.append("../../kyGetOTP2/") 
# add a new path which is two directory above 
# (going back to directory will makes it fall under the same directory with 'initialConnect.py')
from initialConnect import * # since we added a new path, we can directly do `from initialConnect import *`

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect # used for sending http response
from django.urls import reverse

# Create your views here.

# default page
def index(request):
    return render(request, "otpGetter/index.html", {})

# get otp
def getOTP(request):
    emailAddress = str(request.POST["emailDayo"])

    connection = imaplib.IMAP4_SSL(host)
    connection.login(user, password)
    connection.select("INBOX") 
    # need to select the "INBOX" every time a new request is made to `refresh` the mailbox
    # (getting the mails from mailbox again, to get the newly added mails)

    searchStatus, mailList = connection.search(None, '(FROM "info@account.netflix.com")', '(TO "%s")' %(emailAddress))
    # search() rertun two value:
    # 1) the status of the search `OK`, `NO`, or `BAD`
    # 2) the id of mails in byte format, in a list
    # here we search with the criteria of "FROM info@account.netflix.com" and "TO emailAddress"
    # we use conversion specifier to replace `%s` to the emailAddress from the user request arguemnt
    # reference (search criteria): https://gist.github.com/martinrusev/6121028
    # if you have multiple criteria, just add on at the back, e.g. search(None, '(FROM "user@mail.com")', 'SEEN', ...)

    if (len(mailList[0].split()) == 0): 
        # if the len of the mailList after splitting is 0, that means the mail doesn't exist
        # (it doesn't satisfy the search criteria)
        return HttpResponse("The email doesn't exist, please try again")
    else:
        fetchStatus, fetchData = connection.fetch(mailList[0].split()[-1], '(RFC822.TEXT)')
        # fetch the latest email, '(RFC822)' means get all the content, `(RFC822.TEXT)` means only get the text body
        # reference: https://www.rfc-editor.org/rfc/rfc1730#section-6.4.5
        # fetch() returns two value:
        # 1) the fetch status
        # 2) a list of bytes related to the email message (such as the sender, mail received date, etc...)
        # example of value 2 (format):
        # fetchData = [(b'1604, b'MIME-Version: 1.0\r\nDate: Wed, 14 Aug 2024...), b')']
        # here you can see fetchData is a list of len() 2, the first element, fetchData[0] is a tuple with len() 2, 
        # inside contain data in byte data type such as the mail id "1604", the MIME-Version "1.0", the Date "Wed..."

        message = email.message_from_bytes(fetchData[0][1])
        # convert the byte data to an email.message object
        # remember fetchData[0] is a tuple, the first element of the tuple is the mail id
        # the second element is all the data in the email message, thus we need to convert fetchData[0][1]

        payload = message.get_payload()
        # get the payload, which is the main message thingy
        # this return a string

        numList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        # since python doesn't support ASCII comparison like in C++, we need to create a list and iterate through it
        for i in payload.split():
            if (len(i) == 4): # netflix otp is 4 character long
                isOTP = True
                for j in str(i): # iterate and check if every character is within numList
                    if j not in numList:
                        isOTP = False
                        break
                if (isOTP and i != str(datetime.datetime.now()).split()[0].split('-')[0]):
                    return HttpResponse(str(i))
        
        return HttpResponse("Something went wrong... Please try again later")