import imapclient
import smtplib
import datetime
import pyzmail
import time
import subprocess
import os
import requests

def checkInternet():
    try:
        requests.get('https://www.google.com')
        return True
    except requests.ConnectionError:
        return False

dt = datetime.datetime.now()
today = dt.strftime('%d-%b-%Y')
print(today)

while not checkInternet():
    print('Waiting for network...')
    time.sleep(5)

imapObj = imapclient.IMAPClient('imap.gmail.com', ssl = True)
imapObj.login('ajaydyavathi@gmail.com', 'abvpekfnaadlsplh')
imapObj.select_folder('INBOX', readonly = False)

while True:
    if checkInternet():
        imapObj.select_folder('INBOX', readonly = False)
        UIDs = imapObj.search(['UNSEEN'])
        if UIDs == []:
            print('No new mail from dyavathiajay@gmail.com')
            time.sleep(2)
        for each in UIDs:
            print(each)
            raw = imapObj.fetch([each], ['BODY[]'])
            msg = pyzmail.PyzMessage.factory(raw[each][b'BODY[]'])
            mfrom = msg.get_addresses('from')
            if 'dyavathiajay@gmail.com' in str(mfrom):
                if msg.text_part != None:
                    mbody = msg.text_part.get_payload().decode(msg.text_part.charset)
                    print(mbody)
                    mbody = mbody.split('"')[1]
                    print(mbody)
                    if 'subprocess' in msg.get_subject().lower():
                        try:
                            subprocess.Popen(['open', mbody])
                        except:
                            print('Subprocess terminated!')
                    if 'os' in msg.get_subject().lower():
                        try:
                            os.system(mbody)
                        except:
                            print('OS Terminated!')
                        
            else:
                print('No mail from dyavathiajay@gmail.com')
            
    else:
        print('Waiting for internet connection...')
    time.sleep(2)    
            
    
