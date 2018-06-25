import requests
from requests.exceptions import HTTPError


def text_message(debug=False, message=None):
    if debug:
        from instance.config import test as config
    else:
        from instance.config import live as config

    url = ('https://api.twilio.com/2010-04-01/Accounts/'
           + config.account_sid
           + '/Messages.json')
    auth = (config.account_sid, config.auth_token)
    payload = {'To': config.my_number,
               'From': config.from_number,
               'Body': message}

    if message:
        r = requests.post(url, auth=auth, data=payload)
        if r.status_code != 201:
            raise HTTPError("HTTP Error {}".format(r.status_code))
            # log r.json()
    return r


if __name__ == '__main__':
    res = text_message(debug=True, message='testing')
    print(res.text)
