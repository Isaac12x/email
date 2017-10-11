from sys import argv
import requests
import json
import re

script = argv

arrow = "=+>"
print "First Name"
first_name = raw_input(arrow)
if first_name.split(" ")[:-1]:
    last_name = first_name
else:
    print "Last Name"
    last_name = raw_input(arrow)
print "Add a list of comma separated domains"
domains = raw_input(arrow)

# text = open(file_to_open, 'r')
# new_data = text.read().replace('\n', ',')
# email_list = []
# # create a list
# for rand in new_data:
#     email = ''
#     if rand is ',':
#         email_list.append(email)
#     elif rand is ' ':
#         email = ''
#     else:
#         email += rand
# email_list = re.match(r"^[,]+$", new_data, re.X)
#
#
# text = open(file_to_open, 'w')
# text.write(new_data)
# text.close()


def add_names():
    arrow = "=+>"
    print "First Name"
    first_name = raw_input(arrow)
    if first_name.split(" ")[:-1]:
        last_name = first_name
    else:
        print "Last Name"
        last_name = raw_input(arrow)
    print "Add a list of comma separated domains"
    domains = raw_input(arrow)


def generate_emails(first, last_name, domain):
    """ Generator with theese recipes:

    first@domain
    last@domain
    firstlast@domain
    firstlast1@domain
    first.last@domain
    first.last1@domain
    flast@domain
    firstla@domain
    firstlas@domain
    flas@domain
    f.last@domain
    firstl@domain
    first.l@domain
    fl@domain
    f.l@domain
    lastfirst@domain
    last.first@domain
    lastf@domain
    last.f@domain
    lf@domain
    l.f@domain """

    email_list = []
    # generator
    try:
        gen_list = [
                    '{0}'.format(first),
                    '{0}'.format(last_name),
                    '{0}{1}'.format(first, last_name),
                    '{0}{1}1'.format(first, last_name),
                    '{0}.{1}'.format(first, last_name),
                    '{0}.{1}1'.format(first, last_name),
                    '{0}{1}'.format(first[0], last_name),
                    '{0}{1}'.format(first, last_name[:2]),
                    '{0}{1}'.format(first, last_name[:3]),
                    '{0}.{1}'.format(first[0], last_name),
                    '{0}{1}'.format(first, last_name[0]),
                    '{0}.{1}'.format(first, last_name[0]),
                    '{0}.{1}'.format(first[0], last_name[0]),
                    '{0}{1}'.format(last_name, first),
                    '{0}.{1}'.format(last_name, first),
                    '{0}{1}'.format(last_name, first[0]),
                    '{0}{1}'.format(last_name[0], first[0]),
                    '{0}.{1}'.format(last_name[0], first[0]),
                    ]

        for email in gen_list:
            generated_email = "{0}@{1}".format(email, domain)
            email_list.append(generated_email)

        return email_list
    except ValueError:
        add_names()


def check_for_disposable_emails(email):
    """ Returns true if the email is any good
    false otherwise """

    url_to_check = 'https://www.validator.pizza/email/%s' % (email)

    try:
        response = requests.get(url_to_check)
        data = json.loads(response.text)
        print(data)
        if response.status_code is 200:
            if data['mx'] is not True & data['disposable'] is not False:
                return True
    except:
        return False


def save_emails_to_file(emails):
    """ Assumes emails is a list of emails

    """
    text_file = open('file.txt', 'wt')
    for email in emails:
        # This is done to remove '' from the email
        text_file.write(email)
        text_file.write(',\n')

    text_file.close()


# Implementation
emails = generate_emails(first_name, last_name, domains)
save_emails_to_file(emails)
