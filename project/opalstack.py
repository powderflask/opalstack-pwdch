# project/opalstack.py

from os import path
from requests.auth import AuthBase
import requests
from project import app

ENDPOINT_BASE = path.join(app.config['OPALSTACK_API_URL'],
                          'api/{version}'.format(version=app.config['OPALSTACK_API_VERSION']))
API_TOKEN = app.config['OPALSTACK_API_TOKEN']

class TokenAuth(AuthBase):
    """Attaches HTTP Token Authentication to the given Request object."""

    def __init__(self, token):
        # setup any auth-related data here
        self.token = token

    def __call__(self, r):
        # modify and return the request
        r.headers["Authorization"] = f"Token {self.token}"
        r.headers["Content-Type"] = "application/json"
        return r


def get_request(endpoint, data=None):
    """ Make request to endpoint, check for success, return json.loads(response.content) """
    abs_endpoint = path.join(ENDPOINT_BASE, endpoint)
    r = requests.get(
        abs_endpoint,
        auth=TokenAuth(API_TOKEN),
        json=data,
    )
    if r.ok:
        return r.json()
    else:
        # TODO: log these messages.
        print("API returned non-200 error code for ", abs_endpoint)
        print(r.status_code, r.reason, r.text)
        return None


def post_request(endpoint, data=None):
    """ Make request to endpoint, check for success, return True if successful, False otherwise """
    abs_endpoint = path.join(ENDPOINT_BASE, endpoint)
    r = requests.post(
        abs_endpoint,
        auth=TokenAuth(API_TOKEN),
        json=data,
    )
    if not r.ok:
        # TODO: log these messages.
        print("API returned non-200 error code for ", abs_endpoint, data)
        print(r.status_code, r.reason, r.text)
    return r.ok


def get_mailuser(mailbox):
    """ Return dict from opalstack for given mailbox name, or None """
    mailusers = get_request("mailuser/list/")
    for record in mailusers['mailusers']:
        if record['name'] == mailbox:
            return get_request("mailuser/read/{}".format(record['id']))
    return None


def get_email_adderess(email_addr):
    """ Return dict from opalstack for given email address, or None """
    mails = get_request("mail/list/")
    for record in mails['mails']:
        if record['address'] == email_addr:
            return get_request("mail/read/{}".format(record['id']))
    return None


def validate_email_destination(os_mailbox, os_email):
    """ return True iff O.S. mailbox record is a destination linked to given O.S. email record """
    destinations = os_email.get('destinations', None)
    return os_mailbox['id'] in destinations


def change_password(os_mailbox, password):
    """ Attempt to set given O.S. mailuser password.  Return True iff successful. """
    return post_request('mailuser/pwdch/',
                             data=[{'id': os_mailbox['id'], 'password': password}])
