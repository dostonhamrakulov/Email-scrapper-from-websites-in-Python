import re
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlsplit
import pandas as pd
import requests
from collections import deque

def email_finder_from_base_url(base_url):
    email = check_base_url_in_db(base_url)
    domain = urlsplit(base_url)[1].split('.')[1]
    if email is not None:
        return email
    new_urls = deque([base_url])
    processed_urls = set()
    emails = []
    attemps = 0
    while len(new_urls):
        if len(emails) > 1:
            break
        if attemps == 30:
            break
        # move next url from the queue to the set of processed urls
        url = new_urls.popleft()
        print(url)
        processed_urls.add(url)


        response = connect_to_page(url, base_url )
        if response == 'Website request error':
            save_results_in_db(base_url, response)
            return response


        links = get_website_links(response, base_url, domain)
        if links == None:
            log(f'{str(datetime.now())},no page links in website,{base_url}, {url}')
            continue
        new_links = [x for x in links if x not in processed_urls]
        new_urls += new_links


        email = find_emails(response)
        if len(email) !=0:
            for e in email:
                if e not in emails:
                    emails.append(e)
        attemps += 1

    emails = clean_emails(emails)
    if len(emails) == 0:
        emails = None
    save_results_in_db(base_url, emails)
    return emails


def clean_emails(emails :list):
    emails = [x.strip() for x in emails]
    emails = list(dict.fromkeys(emails))
    return emails


def connect_to_page(url, base_url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response
        else:
            log(f'{str(datetime.now())},Website request error, {base_url}, {url}, {response.status_code}')
            return 'Website request error'
    except Exception as e:
        log(f'{str(datetime.now())},Website request error, {base_url}, {url}, {e}')
        return 'Website request error'


def get_website_links(response, base_url, domain):
    soup = BeautifulSoup(response.text, features="lxml")
    urls = [anchor.get('href') for anchor in soup.find_all("a") if anchor.get('href') is not None]
    if len(urls) ==0:
        return None
    urls = clean_urls(urls, base_url, domain)
    return urls


def clean_urls(urls :list, base_url : str, domain :str):
    clean_url = []
    for url in urls:

        if url.startswith(('http://', 'https://')) and domain in url:
            clean_url.append(url)

        if url.startswith('/'):
            clean_url.append(base_url + url)
    return clean_url


def find_emails( response):
    emails = re.findall(r"[a-z][a-z0-9\.\-+_]+@[a-z0-9\-+_]+\.[a-z\.]+", response.text, re.I)
    return emails


def log(logs :str):
    f = open('logs.csv', 'a')
    f.write(logs + '\n')
    f.close()


def extract_base_url( link :str):
    parts = urlsplit(link)
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    if base_url == None:
        log(f'{str(datetime.now())},Unmatched base url,,{link},')
        return 'Unmatched base url'
    return base_url


def save_results_in_db(base_url, emails):
    f = open('email_db.csv', 'a')
    f.write(f'{str(datetime.now())}~{base_url}~{str(emails)}\n')
    f.close()


def check_base_url_in_db(base_url):
    df = pd.read_csv('email_db.csv', sep = '~')
    if len(df[df['base_url'] == base_url]['emails']) != 0:
        return df[df['base_url'] == base_url]['emails'].values[0]
    return None
# email_finder_from_base_url('https://beechespharmacy.co.uk/')