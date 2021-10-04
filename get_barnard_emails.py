import requests
from bs4 import BeautifulSoup
import subprocess
import json
import numpy as np


cookies = None

# This somehow fixes ssl.SSLError: [SSL: DH_KEY_TOO_SMALL] dh key too small
# See https://stackoverflow.com/a/41041028
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass

def generate_cookies():
    '''
    Retrieves valid cookies from a Puppeteer script. Full path for node
    is specified because cron jobs are executed without shell.
    '''
    global cookies
    output = subprocess.check_output(['/usr/local/bin/node', 'get-cookies.js'])
    cookies = json.loads(output.decode('utf-8').rstrip())

generate_cookies()
   
r = requests.get(
    'https://directory.columbia.edu/people/search?filter.email=*@barnard.edu&pageSize=10000',
    cookies=cookies
    )
soup = BeautifulSoup(r.text, 'html.parser')

emails = []
rows = soup.find_all('tr')
for row in rows:
  if '<strong>Title:</strong><br/>Student</div>' in str(row):
    emails.append(row.find('a', {'class': 'mailto'}).get_text())

np.savetxt('barnard_emails.csv', emails, delimiter=',', fmt='%s')
