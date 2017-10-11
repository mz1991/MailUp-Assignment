import configparser
import os
import json
import requests
import re
from mail_up_client import MailUpClient

def run_mail_up_client():
    """Run the MailUp Rest Client"""
    print('*****{}*****'.format('Fetching Configuration...'))
    configuration = configparser.RawConfigParser()
    configuration.read('{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), \
                            'mail_up_configuration.ini'))
    print('*****{}*****'.format('Initializing MailUp Rest Client...'))
    mailup_simple_rest_client = MailUpClient(configuration)
    print('*****{}*****'.format('Authenticating...'))
    mailup_simple_rest_client.get_auth_token()
    print('*****{}*****'.format('Done Authentication'))

    print('List of available MailUp Lists')
    available_lists = mailup_simple_rest_client.get_mailup_lists()
    if len(available_lists) == 0:
        print('No Lists available, creating a dummy list...')
        mailup_simple_rest_client.create_mailup_list()
        available_lists = mailup_simple_rest_client.get_mailup_lists()

    for mailup_list in available_lists:
        print('{}'.format(mailup_list['Name']))
    list_found = False
    while not list_found:
        list_name = input("Enter the name of the list to \
which you would like to add the new group:\n")
        if list_name in [x['Name'] for x in available_lists]:
            list_found = True
            list_id = [x['IdList'] for x in available_lists if x['Name'] == list_name][0]
        else:
            print('{} list not available!'.format(list_name))

    group_name = input("Insert the name of the group:\n")
    group_notes = input("Add some notes\n")
    group_id = mailup_simple_rest_client.create_mailup_list_group(list_id, \
                                                                    group_name, group_notes)
    print("Created new group {} with id {}.".format(group_name, group_id))

    how_many_recipient = 0
    min_number_of_recipients = int(configuration['REQUIREMENST']['min_number_of_recipients'])
    while how_many_recipient < min_number_of_recipients:
        how_many_recipient = int(input("How many recipients you want to add to the group?\n"))
        if how_many_recipient < min_number_of_recipients:
            print('To follow the requirements you need to add at least 3 recipients')
   
    recipients = []
    for i in range(how_many_recipient):
        rep_name = input("{} - Insert recipient name:\n".format(str(i + 1)))
        valid_email = False
        while not valid_email:
            rep_email = input("{} - Insert recipient email:\n".format(str(i + 1)))
            if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", rep_email):
                valid_email = True
            else:
                print('{} not valid email'.format(rep_email))

        post_data = json.loads(configuration['MAIL_UP_API']['add_recipient_body']  \
                    .format(rep_name, rep_email))
        recipients.append(post_data)
    mailup_simple_rest_client.add_mailup_group_recipients(group_id, recipients)
    print("Added {} recipients to the group {}.".format(how_many_recipient, group_name))

    message_subject = input('Input subject of the new message:\n')
    message_content = input('Input content of the new message:\n')
    message_id = mailup_simple_rest_client.create_mailup_message(list_id,\
                                                                message_subject, message_content)
    print("Created new message with id {}.".format(message_id))

    number_of_sent_messages = mailup_simple_rest_client.send_mailup_message(group_id, message_id)
    print('{} messages sent!'.format(number_of_sent_messages))

if __name__ == "__main__":
    try:
        run_mail_up_client()
    except Exception as exp:
        print(exp)
