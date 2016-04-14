import cufflinks
import pandas as pd
from gmail import Gmail
import secret



def run():
    g = Gmail()
    # Store your Username/Pwd in secret.py, and don't include secret.py in your github
    g.login(secret.gmail_user, secret.gmail_pwd)
    messages = g.inbox().mail(to=secret.gmail_user)
    for email in messages:
        # email_read(email, subject) # can also unread(), delete(), spam(), or star()
        email.fetch()
        body = email.body
        subject = email.subject
        from_ = email.fr
        print 'From: %s, Subject: %s' % (from_, subject)
        if 'balance check' in subject.lower():
            import loan_balances
            for attachment in email.attachments:
                title = config.temp_folder + '/' + attachment.name
                attachment.save(title)