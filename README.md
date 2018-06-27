Camera Finder
------

Scrapes www.wexphotovideo.com looking for used Canon 5D Mk III's and
sends a text message if found.

Requires a Twilio account, project and phone number.


*instance/config.py* should contain the following:

file_location = 'found_cameras.txt'  # file for previously identified cameras

    class live():
        account_sid = 'Twilio live SID'
        auth_token = 'Twilio live auth token'
        from_number = 'Twilio phone number'
        my_number = 'Phone number to send the message to'


    class test():
        account_sid = 'Twilio test SID'
        auth_token = 'Twilio test auth token'
        from_number = '+15005550006'  # Twilio success test number
        my_number = 'Phone number to send the message to'  # can be any number
