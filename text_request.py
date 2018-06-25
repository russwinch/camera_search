import requests

debug = True
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
           'Body': 'another tester'}

try:
    r = requests.post(url, auth=auth, data=payload)
except requests.ConnectionError as e:
    # log e
    print(e)
else:
    if r.status_code != 201:
        # log r.json()
        print(r.json())
