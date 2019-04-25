# abf-screenshotTaker.py
# Given a txt file (sites.txt) that is a list of domains (often uppercase), take 
#    an "above the fold" (abf) screenshot of each

# TODO: run headless ... for now is fun watching it
# TODO: use f-strings instead of old-school string formatting

from selenium import webdriver
from datetime import datetime

import os, time, traceback

subDir = 'screenshots'                          #create a directory to save in
os.makedirs(subDir, exist_ok=True)              

driver = webdriver.Firefox()

dateStamp = datetime.today().strftime('%Y-%m-%d')

# splitlines() method splits the string at line breaks and returns a list of lines in the string
with open("sites.txt") as f:
   sites = f.read().splitlines()

for site in sites:
   siteReadable = site.lower()
   url = 'http://' + siteReadable               # TODO: watch for issues with https vs http???
   print('getting: ' + url)  

   try:
      driver.get(url);
      time.sleep(2)                             # page needs to settle down in some cases
      element = driver.find_element_by_tag_name('html');
      pageImageFile = './' + subDir + '/' + siteReadable + '-' + dateStamp + '.png'
      driver.save_screenshot(pageImageFile);
      time.sleep(2)
   
   # TODO: better error handling ... raise for status ... log the type of error (ex, 404)
   except:
      print('there was a problem at: %s ' % (siteReadable))      
      errorFile = open('errorInfo.txt', 'a')
      errorFile.write('error on %s at %s ' % (dateStamp, siteReadable) + '\n')
      errorFile.write(traceback.format_exc())
      errorFile.close()
      continue
    
driver.quit()
print('done processing')