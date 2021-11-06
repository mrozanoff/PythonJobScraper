#python code using bs4 to find most reliable job opportunities from indeed

#Matthew Rozanoff

import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def get_url(pos, loc, fullT, evpLvl):   #get the indeed link
    template = "https://www.indeed.com/jobs?q={}&l={}&jt={}&explvl={}"

    url = template.format(pos, loc, fullT, evpLvl)
    return url


def get_record(card, soup):    #get data from a single record
 
    title = soup.find("h2", class_="jobTitle").get_text()

    company = card.find('span','companyName').text.strip()

    location = card.find('div','companyLocation').text

    summary = card.find('div','job-snippet').text.strip()

    post_date = card.find('span','date').text

    link = 'https://www.indeed.com' + card.get('href')
    
    try:
        salary = card.find('span','salaryText').text
    except AttributeError:
        salary = ''

    record = (title, company, location, post_date,salary,  summary, link)

    return record


def main(pos, loc, fullT, evpLvl):
    records = []
        
    url = get_url(pos, loc, fullT, evpLvl)

    while True:   #creating dictionary

        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('a', 'tapItem')         
        
        
        for card in cards:
            record = get_record(card, soup)
            
            records.append(record)
        break


    with open('jobResults.csv', 'w') as f:  #writing the csv
        writer = csv.writer(f)
        writer.writerow(['JobTitle', 'Company', 'Location', 'PostDate','Salary', 'Summary', 'Link'])
        writer.writerows(records)


main("python", "New York NY", "fulltime", "entry level")


