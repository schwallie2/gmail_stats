import time
import pandas as pd
from gmail import Gmail

import secret


def login_to_gmail(g):
    ct = 0
    while ct < 5:
        g.login(secret.gmail_user, secret.gmail_pwd)
        if g.logged_in:
            return True
        else:
            time.sleep(5)
            ct += 1
    return False

def clean_email(clean):
    # Often shows up as "Your Name" <your.email@gmail.com>
    return clean.split('<')[-1].rstrip('>')

def parse_emails(messages, store):
    ct = 0
    for email in messages:
        email.fetch()  # Have to fetch the object to get the details
        subject = email.subject
        if 'Re:' not in subject:
            # Start a new "thread"
            pass
        subject = subject.split('Re: ')[-1]
        from_ = clean_email(email.fr)
        to = clean_email(email.to)
        headers = email.headers
        received_time = headers['Date']
        adder = {'fr': from_, 'received': pd.Timestamp(received_time),
                 'to': to}
        if subject in store:
            store[subject].append(adder)
        else:
            print ct
            store[subject] = [adder]
            ct += 1
    return store

def run():
    g = Gmail()
    # Store your Username/Pwd in secret.py, and don't include secret.py in your github
    success = login_to_gmail(g)
    if not success:
        return  # TODO: Add error handling
    # Return list of gmail message objects
    to_me = g.inbox().mail()
    received = parse_emails(to_me, store={})
    return received

def match_dicts():
    new = {}
    for key, val in sent.items():
        if key == '':
            continue
        if key in received:
            matching = received[key]
            print matching
            new[key] = val.append(received)