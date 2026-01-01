import requests
import re
from bs4 import BeautifulSoup
import concurrent.futures
import time

RemainingURLs = []
Responses = {}

def find_emails_in_text(scoutURL):
    # print('first')
    try:
        page = requests.get(scoutURL, timeout=10)
    except requests.exceptions.RequestException as e:
        # print(f"Request failed for {scoutURL}: {e}")
        RemainingURLs.append(scoutURL)
        return []

    secSoup = BeautifulSoup(page.text, "html.parser")
    
    secondPython_jobs = secSoup.get_text()

    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    emails = [] 
    # for paragraph in secondPython_jobs:
    found_emails = re.findall(email_pattern, secondPython_jobs)
    emails.extend(found_emails)
    Responses[scoutURL] = emails
    
    print(emails)
    return emails


def getemails(data):
    emails_found = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(find_emails_in_text, url) for url in data] 
        #print all futures as they complete
        for future in concurrent.futures.as_completed(futures):
            try:
                emails = future.result()
                emails_found.extend(emails)
            except Exception as e:
                # print(f"Error occurred: {e}")
                continue
                
                                
    print("Finished processing all URLs.")  
    print(f'Number of remaining URLs: {len(RemainingURLs)} include: ')        
    print(RemainingURLs)
    print("Emails found:")
    unique_emails = set(emails_found)
    emails_found = list(unique_emails)
    print(emails_found)
    return {"Responses": Responses, "RemainingURLs": RemainingURLs}