import json
import utils as utl
import requests

class MailUpClient:
    """A simple MailUp Rest API Client"""
    def __init__(self, configuration):
        self.configuration = configuration
        self.access_token = None
        self.refresh_token = None

    def get_auth_token(self, refresh_token_post=False):
        """Return access token and refresh access token"""
        client_id = self.configuration['MAIL_UP_KEYS']['client_id']
        client_secret = self.configuration['MAIL_UP_KEYS']['client_secret']
        username = self.configuration['MAIL_UP_KEYS']['username']
        password = self.configuration['MAIL_UP_KEYS']['password']
        if not refresh_token_post:
            url = self.configuration['MAIL_UP_API']['auth_endpoint'] + \
                self.configuration['MAIL_UP_API']['auth_post_body'].format(\
                client_id, client_secret, username, password)
        else:
            url = self.configuration['MAIL_UP_API']['auth_endpoint'] + \
                self.configuration['MAIL_UP_API']['auth_post_body_refresh'].format(\
                client_id, client_secret, username, password, self.refresh_token)

        headers = {}
        headers["Content-Type"] = 'application/x-www-form-urlencoded'
        auth_response = requests.post(url, headers=headers)

        if auth_response.status_code == 401 and refresh_token_post:
            self.get_auth_token(True)
        elif auth_response.status_code == 200 or auth_response.status_code == 302:
            # http://help.mailup.com/display/mailupapi/Authenticating+with+OAuth+v2
            # HTTP 200 or 302 is returned in case of successful authorization
            json_response = auth_response.json()
            self.refresh_token = json_response['refresh_token']
            self.access_token = json_response['access_token']
        else:
            raise Exception('Auth Exception')

    def get_mailup_lists(self):
        """Get the MailUp Lists for the auth user"""
        http_response = utl.do_get(self.configuration['MAIL_UP_API']['get_lists_endpoint'],\
                                utl.buid_auth_header(self.access_token), self)
        if http_response.status_code == 200:
            return http_response.json()['Items']
        else:
            raise Exception("Exception, HTTP {}".format(http_response.status_code))

    def create_mailup_list(self):
        """Create a new dummy mail up list and return the list id"""
        # The creation of the new list is not specified in the requirements
        # so let's create a dummy list if the provided list does not exist.
        new_list_post_data = {
            "Name":"Interview assignment list",
            "Business":True,
            "Customer":True,
            "OwnerEmail":"zuccon.matteo@gmail.com",
            "ReplyTo":"zuccon.matteo@gmail.com",
            "NLSenderName": "Matteo Zuccon",
            "CountryCode": "IT",
            "CompanyName":"Matteo Zuccon",
            "ContactName":"Matteo Zuccon",
            "Address":"Your address",
            "City":"Your city",
            "CountryCode":"IT",
            "PermissionReminder":"Your permission reminder",
            "WebSiteUrl":"https://whiletrue.run",
            "UseDefaultSettings":True
        }
        http_response = utl.do_post(self.configuration['MAIL_UP_API']['create_list_endpoint'], \
                                new_list_post_data,\
                                utl.buid_auth_header(self.access_token), self)
        if http_response.status_code == 200:
            return http_response.json()['IdList']
        else:
            raise Exception("Exception, HTTP {}".format(http_response.status_code))

    def create_mailup_list_group(self, list_id, group_name='', notes=''):
        """ Create a new MailUp group """
        post_data = json.loads(self.configuration['MAIL_UP_API']['create_group_body']  \
                        .format(group_name, notes))

        http_response = utl.do_post(self.configuration['MAIL_UP_API']\
                                    ['create_group_endpoint'].format(list_id),\
                                    post_data, utl.buid_auth_header\
                                    (self.access_token), self)

        if http_response.status_code == 200:
            return http_response.json()['idGroup']
        else:
            raise Exception("Exception, HTTP {}".format(http_response.status_code))

    def add_mailup_group_recipients(self, group_id, recipient_list):
        """Add a list of recipients to a group"""
        http_response = utl.do_post(self.configuration['MAIL_UP_API']\
                        ['add_recipient_to_group_endpoint']\
                        .format(group_id), \
                        recipient_list, \
                        utl.buid_auth_header(self.access_token), self)
        if http_response.status_code != 200:
            raise Exception("Exception, HTTP {}".format(http_response.status_code))

    def create_mailup_message(self, list_id, subject, content):
        """Create a MailUp message"""
        post_data = json.loads(self.configuration['MAIL_UP_API']['create_message_body']  \
                    .format(subject, content))

        http_response = utl.do_post(self.configuration['MAIL_UP_API']['create_message_enpoint']\
                                    .format(list_id), \
                                    post_data, \
                                    utl.buid_auth_header(self.access_token), self)

        if http_response.status_code == 200:
            return http_response.json()['idMessage']
        else:
            raise Exception("Exception, HTTP {}".format(http_response.status_code))

    def send_mailup_message(self, group_id, message_id):
        """ Send MailUp message"""
        http_response = utl.do_post(self.configuration['MAIL_UP_API']\
                                ['send_message_to_group_endpoint']\
                                .format(group_id, message_id), None, \
                                utl.buid_auth_header(self.access_token), self)
        if http_response.status_code == 200:
            return http_response.json()['Sent']
        else:
            raise Exception("Exception, HTTP {}".format(http_response.status_code))
