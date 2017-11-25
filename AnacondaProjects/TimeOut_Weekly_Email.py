import urllib2
import lxml
from lxml import html,etree
import datetime
from bs4 import BeautifulSoup
import re
url= 'https://www.timeout.com/san-francisco/things-to-do/things-to-do-in-san-francisco-this-week'
source=urllib2.urlopen(url).read()
tree=BeautifulSoup(source,'lxml')
tre=html.document_fromstring(source)
Events=[]
Info=[]
Links=[]
for t in tre.cssselect('div.feature-item__column'):
    #print(len(t))
    for child in t:
        #print child
        if child.tag=='h3':
            #print child.text_content()
            #print etree.tostring(child, method='text')
            #h3_tag=etree.tostring(child, method='text')
            Events.append(child.text_content())
        if child.tag=='div':
            for child2 in child:
                if child2.text_content()!='' and child2.tag=='p':
                    info=child2.text_content()
                    #print child2.text_content(),'\n'
                    Info.append(info)
        if child.tag=='a':
            Link=child.get('href')
            #print Link
            if Link.startswith('/'):
                Link='https://www.timeout.com'+Link
                #print Link
                Links.append(Link)


This_Week=zip(Events,Info,Links)
#for i in This_Week:
#    print i[0],i[1],i[2],'\n'

stuff_i_like=['drag','dance','run']
My_events=[]
message=''
for food in stuff_i_like:
    #print food
    for hh in This_Week:
        #print hh
        # checking for text AND making sure I don't have duplicates
        if food in hh[1] and hh not in My_events:
            #print "YAY! I found some %s!" % food
            My_events.append(hh)

#print "I think you might like %d of them, yipeeeee!" % len(My_events)
for p in tree.find_all('span',{'class':'post_info__date'}):
    date_of_post=p.text
week=datetime.datetime.now()
week=week.strftime('%b-%d-%Y %a')
message = 'Hey Your_Name,\n'
#print "The scraper found %d events today, %s !" % (len(This_Week),week)
message += "The scraper found %d events today, %s \nTimeOut- %s" % (len(This_Week),week,date_of_post)
message+= "\n\n I think you might like %d of them!\n\n" % len(My_events)
for i in My_events:
    message += '\n'.join(i)
message += '\n\nHere are the other things going on:\n\n'
for i in This_Week:
    message += '\n'.join(i)

message = message.encode('utf-8')
# To read more about encoding:
# http://diveintopython.org/xml_processing/unicode.html
message = message.replace('\t', '').replace('\r', '')
message += '\n\nXOXO,\n Your Py Script'

#print message

import smtplib

fromMy='hugginghelps@yahoo.com'
to='hugginghelps@yahoo.com'
subj='Fun stuff this week (TimeOut)'
date=week

msg='From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s'%(fromMy,to,subj,date,message)
username= str('your_email')
password=str('your_password')
try:
    #server=smtplib.SMTP('smtp.mail.yahoo.com',587)
    server = smtplib.SMTP("smtp.mail.yahoo.com",587 )
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromMy,to,msg)
    server.quit()
    print 'ok the email has sent'
except:
    print 'can\'t send the Email'
