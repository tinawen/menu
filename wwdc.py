#!/usr/bin/env python                                                                                                                                       
import sys
import pickle
import urllib2
from twilio.rest import TwilioRestClient

request = urllib2.Request('https://developer.apple.com/wwdc/')
response = urllib2.urlopen(request)
htmlString = response.read()
file_path = '/home/tina/MenuProject/menuproject/output/htmlString.txt'
account = "AC6ed0bb6c3e18ef4a799373059c4b7ba0"
token = "f2666152761d58313af1060fa1c00a96"
client = TwilioRestClient(account, token)
receivers = ["+18572043104", "+16073412476"]

try:
    file = pickle.load( open(file_path , 'rb'))
    if pickle.load( open(file_path, 'rb')) == htmlString:
        print("Values haven't changed!")
        sys.exit(0)
    else:
        pickle.dump( htmlString, open(file_path, "wb" ) )
        if "WWDC 2013" in htmlString:
            for receiver in receivers:
                message = client.sms.messages.create(to=receiver, from_="+14088833524",
                                                     body="Go buy your WWDC tickets!!!")
                call = client.calls.create(to=receiver, 
                           from_="+14088833524", 
                           url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")
        else:
            print('Value changed')
except IOError:
    pickle.dump( htmlString, open(file_path, "wb" ) )
    print('Created new file.')



