import requests
from bs4 import BeautifulSoup


# URL of the page to crawl
url = 'https://book.interpark.com/display/collectlist.do?_method=bestsellerHourNewYearList201605_xml'


# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the data you're interested in.
    # For example, to get all book titles (you'll need to adjust this based on the actual structure of the HTML):
    titles = soup.find_all('h2', class_='title_of_book')
    for title in titles:
        print(title.get_text().strip())
else:
    print("Failed to retrieve the webpage")

