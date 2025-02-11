import requests
from bs4 import BeautifulSoup
import re
import convertCalendar

def scrape():
    # URL of the website you want to scrape
    url = "https://skolmeny.se/"

    # Send a GET request to the website
    response = requests.get(url)

    # Ensure the request was successful (status code 200)
    if response.status_code != 200:
        exit(f'Failed to retrieve the page. Status code: {response.status_code}')

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")  # You can also use "lxml" if installed

    # Get all text from the parsed HTML (removes tags)
    text = soup.get_text(separator="\n", strip=True)

    # Print the extracted text
    #print(text)
    text = text[:text.find('E-post')]
    text = text[text.find('MENY'):]
    text = re.sub("[^a-zA-ZåäöÅÄÖ0-9/\n ]", "", text)
    text = text.replace('\n\n', '\n')
    text = text.split('\n')[:-1]
    new_text = []
    skip = False
    for i,part in enumerate(text):
        if skip:
            skip = False
            continue
        if '/' in part:
            new_text.append(f'{part}, {text[i+1]}')   
            skip = True     
        else:
            new_text.append(part)

    dict_text = {}
    till_now = ''
    till_now_2 = ''
    for i, part in enumerate(new_text):
        if 'MENY' in part:
            part = part.capitalize()
            dict_text[part] = {}
            till_now = part
        else:
            if '/' in part:
                dict_text[till_now][part] = []
                till_now_2 = part
            else:
                dict_text[till_now][till_now_2].append(part)
    print(dict_text)
    return dict_text

if __name__ == '__main__':
    menu_data = scrape()
    data = convertCalendar.get_current_weeks()
    try:
        old_weeks = data['w'] 
    except KeyError:
        old_weeks = []
    weeks = convertCalendar.convert_data(menu_data, old_weeks)
    convertCalendar.write_to_json({'w':weeks})
