import requests
import re
from bs4 import BeautifulSoup
import concurrent.futures
import time

scoutURL = "https://universalstorebuy.myshopify.com/policies/privacy-policy"
RemainingURLs = []

def find_emails_in_text(scoutURL):
    # try:        
    secondPage = requests.get(scoutURL, timeout=2)

    # htmlcontent = secondPage.text

    secSoup = BeautifulSoup(secondPage.text, "html.parser")

    # secondResults = secSoup.find(id="MainContent")

    secondPython_jobs = secSoup.get_text()
    # print(type(secondPython_jobs))
    # print(secondPython_jobs)

    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    emails = [] 
    # for paragraph in secondPython_jobs:
    found_emails = re.findall(email_pattern, secondPython_jobs)
    emails.extend(found_emails)

    print(emails)
    return emails


def getemails(data):
    emails_found = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(find_emails_in_text, url) for url in data] 
        for future in concurrent.futures.as_completed(futures):
            try:
                emails = future.result()
                emails_found.extend(emails)
            except Exception as e:
                # print(f"Error occurred: {e}")
                RemainingURLs.append(scoutURL)
                
    print("Finished processing all URLs.")  
    print("Remaining URLs:")        
    print(RemainingURLs)
    print("Emails found:")
    unique_emails = set(emails_found)
    emails_found = list(unique_emails)
    print(emails_found)
    return emails_found