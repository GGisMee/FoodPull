from datetime import datetime
from icalendar import Calendar, Event
import json
import os
# Your menu data
menu_data = {
    'Meny vecka 7': {
        '10/2, måndag': ['Kebab i tomatsås serveras med ris', 'Kebab i tomatsås med ris veg'],
        '11/2, tisdag': ['Kycklingfärsbiff med rostad potatis och varm dragonås', 'Morotsbiff med rostad potatis och dragonsås'],
        '12/2, onsdag': ['Pastagratäng med nötfärs och tomat', 'Pastagratäng med tomat och salladsost'],
        '13/2, torsdag': ['Torsknuggets med potatismos och remouladsås', 'Grönsaksburgare med potatismos och remouladsås'],
        '14/2, fredag': ['Kyckling i kokos och chili serveras med ris', 'Linser och grönsaker med kokos och chili serveras med ris', 'Med reservation för ev ändringar']
    },
    'Meny vecka 8': {
        '17/2, måndag': ['Kyckling tandoori serveras med ris', 'Vegetarisk tandoori serveras med ris'],
        '18/2, tisdag': ['Oxpytt serveras med rödbetor', 'Pytt i panna med rödbetor Växtbaserad'],
        '19/2, onsdag': ['Korv med makaroner och ketchup', 'Korv med makaroner ketchup växtbaserad'],
        '20/2, torsdag': ['Potatis och purjolökssoppa med mjukt bröd och ost', 'Potatis och purjolökssoppa med mjukt bröd och ost'],
        '21/2, fredag': ['Köttbullar med kokt potatis och gräddsås', 'Köttfria köttbullar med kokt potatis och gräddsås', 'Med reservation för ev ändringar']
    }
}

def get_current_weeks():
    # Read data from JSON file
    if not os.path.exists('input.json'):
        return {}

    with open('input.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def write_to_json(data:str):
    with open('input.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def convert_data(data, old_weeks):
    # Create calendar
    cal = Calendar()
    weeks = []
    for week, days in data.items():
        for i,part in enumerate(week):
            if part.isdigit():
                week_num =  int(week[i:])
                break
        weeks.append(week_num)
        
        if week_num in old_weeks:
            continue
        
        for date_str, meals in days.items():
            date_part, _ = date_str.split(', ')  # Extract "10/2" from "10/2, måndag"
            day, month = map(int, date_part.split('/'))  # Convert to numbers

            # Assume year is 2024
            starttime = datetime(2025, month, day, 10,50)
            endtime = datetime(2025, month, day, 12,10)

            # Create calendar event
            event = Event()
            event.add('summary', ", \n".join(meals))  # Meal details
            event.add('dtstart', starttime)  # Start date
            event.add('dtend', endtime)  # End date (same day)
            # print(", \n".join(meals))

            cal.add_component(event)

    # Save to ICS file
    with open("menu.ics", "ab") as f:
        f.write(cal.to_ical())

    print("ICS file 'menu.ics' created successfully!")
    return weeks


if __name__ == '__main__':
    data = get_current_weeks()
    try:
        old_weeks = data['w'] 
    except KeyError:
        old_weeks = []
    weeks = convert_data(menu_data, old_weeks)
    write_to_json({'w':weeks})