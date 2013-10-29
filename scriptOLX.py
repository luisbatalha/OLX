from random import randint
import mechanize
import cookielib
from bs4 import BeautifulSoup
import html2text
from threading import Timer
from time import sleep


#calculates the price 
def Price(price):
  return price + randint(-5,5)

def SubmitForm(browser,link, text, name, email):

  browser.open(link)
  browser.select_form(nr=0)

  browser.form['form[a_text]'] = text
  browser.form['form[a_name]'] = name
  browser.form['form[a_email]'] = email

  req = browser.click(type="submit", nr=0)
  browser.open(req)


#sends 5 emails with offers around p1 and a 5th around p2
def SendEmails(br,step,link_to_product_page, percentage1, percentage2, price):

  if step == 1:
    SubmitForm(br,link_to_product_page,"Text 1 offering price " + str(int(Price(price*(1-percentage1)))) + ' euros',"Name1","Email1" )
  if step == 2:
    SubmitForm(br,link_to_product_page,'Text 2 offering price ' + str(int(Price(price*(1-percentage1)))) + ' euros',"Name2","Email2" )
  if step == 3:
    SubmitForm(br,link_to_product_page,'Text 3 offering price ' + str(int(Price(price*(1-percentage1)))) + ' euros',"Name3","Email3" )
  if step == 4:
    SubmitForm(br,link_to_product_page,'Text 4 offering price ' + str(int(Price(price*(1-percentage1)))) + ' euros',"Name4","Email4" )
  if step == 5:
    SubmitForm(br,link_to_product_page,'Text 5 offering price ' + str(int(price*(1-percentage2))) + ' euros',"Name5","Email5" )
  

# End of Functions


br = mechanize.Browser()

cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)


br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


f = open('myfile', 'r+')
lines = f.readlines()

# searches for Iphone 5
br.open('http://www.olx.pt/nf/search/iphone+5+ios')

a = 0

# vector to store the links to the product pages 
vector_link_product = []
vector_link_price = []

soup = BeautifulSoup(br.response().read())
# finds last ad page 
lastpage = soup.findAll('a', attrs={"class" : 'hover_grad_bl'})[-1]

for n in range (1, int(lastpage.renderContents())):

  br.open('http://www.olx.pt/nf/search/iphone+5+ios/-p-' + str(n))

  soup = BeautifulSoup(br.response().read())
  cols = soup.findAll('div', attrs={"class" : 'price'})  

  for i in range(0, len(cols)):
    # finds the title of the ad
    title = cols[i].previousSibling.previousSibling.renderContents()
    link_product = cols[i].previousSibling.previousSibling['href']
    # finds the id of the ad
    idnb = cols[i].previousSibling.previousSibling['href'][-9:]
    # finds the price
    price = cols[i].renderContents()[cols[i].renderContents().find('> ') + 2 : cols[i].renderContents().find(',') - len(cols[i].renderContents())]
    if price.isdigit() == False :
      price = 10000

    # checks:
    # 1. the item is an Iphone 5 and not an Iphone 3G,4,4S ...
    # 2. the price is between the price range that we defined, we dont want to get any case something
    # 3. the idnb is not in the list
    if title.find('5')!=-1 and int(price) > 180 and int(price) < 360:
      for k in range(0, len(lines)):
        if int(idnb) == int(lines[k]):
          a = 1
      if a == 0:
        # put the id on the list
        f.write( idnb +'\n')  
        vector_link_product.append(link_product)
        vector_link_price.append(price)


print str(len(vector_link_product)) + " IPHONES FOUND. " + str(len(vector_link_product)*5)   + " emails to send."
for t in range(0, len(vector_link_product)):
  print vector_link_product[t]
print "Sending Emails ..."


print "Email 1 sent to:"
for k in range(0, len(vector_link_product)):
  SendEmails(br,1,vector_link_product[k], 0.7,0.6, int(vector_link_price[k]))
  print vector_link_product[k]
  sleep(90)

sleep(1800) 
print "==================================="
print "Email 2 sent to:"
for k in range(0, len(vector_link_product)):
  SendEmails(br,2,vector_link_product[k], 0.7,0.6, int(vector_link_price[k]))
  print vector_link_product[k]
  sleep(90)

sleep(2800)
print "==================================="
print "Email 3 sent to:"
for k in range(0, len(vector_link_product)):
  SendEmails(br,3,vector_link_product[k], 0.7,0.6, int(vector_link_price[k]))
  print vector_link_product[k]
  sleep(90)

sleep(3800)
print "==================================="
print "Email 4 sent to:"
for k in range(0, len(vector_link_product)):
  SendEmails(br,4,vector_link_product[k], 0.7,0.6, int(vector_link_price[k]))
  print vector_link_product[k]
  sleep(90)

sleep(1800)
print "==================================="
print "Email 5 sent to:"
for k in range(0, len(vector_link_product)):
  SendEmails(br,5,vector_link_product[k], 0.7,0.6, int(vector_link_price[k]))
  print vector_link_product[k]
  sleep(90)

print "All Emails have been sent!"



# Closes file
f.close()






  

