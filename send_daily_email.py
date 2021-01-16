# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 20:56:35 2021

@author: mitch

To do:
Koppelen Dataframe aan deze file


"""

# email: https://handsoffinvesting.com/automating-your-stock-analysis-with-python/

#Body_of_Email = """\
#Subject: Daily Stock Report
#Stocks of the day:
#""" + df.to_string(index=False) + """\
#
#Sincerely,
#Your Computer"""


#msg = email.message_from_string(Body_of_Email)
#msg['From'] = "gwoon_mitch@live.nl"
#msg['To'] = "mitchmolenaar@gmail.com"
#msg['Subject'] = "Stocks"

#s = smtplib.SMTP("smtp.live.com",587)
#s.ehlo() # Hostname to send for this command defaults to the fully qualified domain name of the local host.
#s.starttls() #Puts connection to SMTP server in TLS mode
#s.ehlo()
#s.login('gwoon_mitch@live.nl', 'xxxxxxxxxxxxxxxxx')          --> adapt                              

#s.sendmail("gwoon_mitch@live.nl","mitchmolenaar@gmail.com", msg.as_string())

#s.quit()