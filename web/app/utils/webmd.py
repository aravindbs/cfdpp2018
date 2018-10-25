import requests
from bs4 import BeautifulSoup 
import json
import re



def webmd_scrape (search_text, page_no=1):
    url = "https://www.webmd.com/search/search_results/default.aspx"
    params = { "query" : search_text,
            "page" : page_no}

    resp = requests.get(url, params)

    soup = BeautifulSoup(resp.text, features="html.parser")
    divs = soup.find_all('div', {"class" : "search-text-container"})
    results = []
    #print (divs)

    for div in divs:
        result = {}
        title = div.find('p', {"class" : "search-results-doc-title"})
        desc =  div.find('p', {"class" : "search-results-doc-description"})
    #  print (title)
        link =  title.find('a').get('href')

        result['title'] = re.sub(r'\s+', ' ', title.text).strip()
        result['desc'] = re.sub(r'\s+', ' ', desc.text).strip()
        result['link'] = link
        results.append(result)

    # print (json.dumps (results, indent = 4))
    return results
