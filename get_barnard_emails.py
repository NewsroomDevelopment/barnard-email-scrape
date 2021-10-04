import requests
from bs4 import BeautifulSoup
import subprocess
import json


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
    'https://directory.columbia.edu/people/search?filter.searchTerm=a&pageSize=5000',
    cookies=cookies)

soup = BeautifulSoup(r.text, 'html.parser')
all_emails = [a.text for a in soup.find_all('a', {'class': 'mailto'})]
print(len(all_emails))

