from bs4 import BeautifulSoup
import requests
import urllib.parse
from collections import deque
import re
import pyfiglet
from termcolor import colored

def print_banner():
    ascii_banner = pyfiglet.figlet_format("Email_finder")
    colored_banner = colored(ascii_banner, 'green')
    name=colored("--------------------------------------------developed by sankar(v.1.0)--------------------------","red")

    print(colored_banner)
    print(name)
    

def get_user_url():
    return input('[+] Enter your URL: ')
def get_user_range():
    range=int(input('[+] Enter your Email range: '))
    return range

def get_base_url(url):
    parts = urllib.parse.urlsplit(url)
    return '{0.scheme}://{0.netloc}'.format(parts)

def get_path(url, parts):
    return url[:url.rfind('/') + 1] if '/' in parts.path else url

def fetch_emails_from_text(text):
    return set(re.findall(r'[a-z0-9.\-+_]+@[a-z0-9.\-+_]+\.[a-z]+', text, re.I))

def fetch_links_from_soup(soup, base_url, path):
    links = set()
    for anchor in soup.find_all("a"):
        link = anchor.attrs.get('href', '')
        if link.startswith('/'):
            link = base_url + link
        elif not link.startswith('http'):
            link = path + link
        links.add(link)
    return links

def process_url(url):
    try:
        response = requests.get(url)
        return response.text
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        return ''

def main():
    print_banner()
    user_url = get_user_url()
    target=get_user_range()
    urls = deque([user_url])
    scraped_urls = set()
    emails = set()
    count = 0

    try:
        while len(urls):
            count += 1
            if count == target:
                break
            url = urls.popleft()
            scraped_urls.add(url)
            base_url = get_base_url(url)
            parts = urllib.parse.urlsplit(url)
            path = get_path(url, parts)
            print('[%d] Processing %s' % (count, url))

            page_content = process_url(url)
            if not page_content:
                continue

            new_emails = fetch_emails_from_text(page_content)
            emails.update(new_emails)

            soup = BeautifulSoup(page_content, features="lxml")
            new_links = fetch_links_from_soup(soup, base_url, path)
            
            for link in new_links:
                if link not in urls and link not in scraped_urls:
                    urls.append(link)

    except KeyboardInterrupt:
        print('[-] Closing')

    for mail in emails:
        print(mail)

if __name__ == "__main__":
    main()
