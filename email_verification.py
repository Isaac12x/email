import re
import dns.resolver
import socket
import smtplib

"""Do this too much and you will get put on a naughty list (e.g. Spamhaus),
especially if you are using a dynamic IP address from your ISP.
B2C addresses: this does not work very well against the big boys who
have their own procedures and spam rules (e.g.hotmail and yahoo).
Incorrect results: some mail servers will give you incorrect results, for
instance catch-all servers, which will accept all incoming email addresses,
often forwarding incoming emails to a central mailbox. Yahoo
addresses displays this catch-all behavior."""


""" There are many tools and techniques verifying email syntax. However,
none of have yet to fully meet the RFC standard. The only way to
definitively prove if an email address exists is to send it an email,
something we are going to emulate soon. As a result, in our example we use
a simple, lenient regex that will let most things through if they have
an @ and a . after it """

# Email address to verify
inputAddress = input('Please enter the emailAddress to verify:')
addressToVerify = str(inputAddress)
address = addressToVerify.lower()
domain = ''

regex_ver = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'

#regex_stricter = '^(?!\.)("([^"\r\\]|\\["\r\\])*"|([-a-z0-9!#$%&'*+/=?^_`{|}~] |(?@[a-z0-9][\w\.-]*[a-z0-9]\.[a-z][a-z\.]*[a-z]$'


common_domains = ['gmail.com', 'hotmail.com', 'aol.com', 'yahoo.com',
                  'msn.com', 'msn.com', 'comcast.net', 'hotmail.co.uk',
                  'sbcglobal.net', 'yahoo.co.uk', 'yahoo.co.in',
                  'bellsouth.net', 'verizon.net', 'earthlink.net',
                  'cox.net', 'rediffmail.com', 'yahoo.ca', 'btinternet.com',
                  'btinternet.com', 'charter.net', 'shaw.ca', 'ntlworld.com']


# Syntax check
def checkValidEmail(addressToVerify):
    match = re.match(regex_ver, address)

    if match is None:
        print('Bad Syntax')
        raise ValueError('Bad Syntax')
    else:
        get_domain = addressToVerify.find('@')
        get_domain += 1
        domain = addressToVerify[get_domain:-1]
        return domain


# Next we need to get the MX record for the target domain
def checkMXRecords(domain):
    # Get domain for DNS lookup
    splitAddress = addressToVerify.split('@')
    domain = str(splitAddress[1])

    records = dns.resolver.query('%s', 'MX') % domain
    mxRecord = records[0].exchange
    mxRecord = str(mxRecord)

    # Get local server hostname
    host = socket.gethostname()

    # SMTP lib setup (use debug level for full output)
    server = smtplib.SMTP()
    server.set_debuglevel(0)

    # SMTP Conversation
    server.connect(mxRecord)
    server.helo(host)
    server.mail('me@domain.com')
    code, message = server.rcpt(str(addressToVerify))
    server.quit()

    # Assume 250 as Success
    if code == 250:
        print('Success')
    else:
        print('Bad')

    # MX record lookup
    records = dns.resolver.query(domain, 'MX')
    mxRecord = records[0].exchange
    mxRecord = str(mxRecord)

    # SMTP lib setup (use debug level for full output)
    server = smtplib.SMTP()
    server.set_debuglevel(0)

    # SMTP Conversation
    server.connect(mxRecord)
    server.helo(server.local_hostname) ### server.local_hostname(Get local server hostname)
    server.mail(fromAddress)
    code, message = server.rcpt(str(addressToVerify))
    server.quit()

    # print(code)
    # print(message)

    # Assume SMTP response 250 is success
    if code == 250:
        print('Success')
    else:
        print('Bad')
