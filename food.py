import requests
from bs4 import BeautifulSoup

# URL of the website you want to scrape
url = "https://skolmeny.se/"

# Send a GET request to the website
response = requests.get(url)

# Ensure the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")  # You can also use "lxml" if installed
    
    # Get all text from the parsed HTML (removes tags)
    text = soup.get_text(separator="\n", strip=True)
    
    # Print the extracted text
    #print(text)
    text = text[:text.find('E-post')]
    text = text[text.find('MENY'):]
    print(text)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
