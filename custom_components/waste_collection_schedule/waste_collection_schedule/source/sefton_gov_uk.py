import datetime
from bs4 import BeautifulSoup
import requests
from waste_collection_schedule import Collection


TITLE = "Sefton Council" # Title will show up in README.md and info.md
DESCRIPTION = "Source for Sefton Council, UK"  # Describe your source
URL = "https://www.sefton.gov.uk/"  # Insert url to service homepage. URL will show up in README.md and info.md
TEST_CASES = {  # Insert arguments for test cases to be used by test_sources.py script
    "Issue2369": {"houseNumberOrName": "1", "Streetname": "Ken Mews", "Postcode": "L20 6GF"},
    "Housename": {"houseNumberOrName": "Gladstone House", "Streetname": "Rosemary Lane", "Postcode": "L37 3JB"},
    "Issue2496": {"houseNumberOrName": "22", "Streetname": "Elton Avenue", "Postcode": "L23 8UW"}
}

API_URL = "https://www.sefton.gov.uk/bins-and-recycling/bins-and-recycling/when-is-my-bin-collection-day/"
ICON_MAP = {   # Optional: Dict of waste types and suitable mdi icons
    "RESIDUAL": "mdi:trash-can",
    "RECYCLING": "mdi:recycle",
    "GREEN": "mdi:leaf",
}

#### Arguments affecting the configuration GUI ####

HOW_TO_GET_ARGUMENTS_DESCRIPTION = { # Optional dictionary to describe how to get the arguments, will be shown in the GUI configuration form above the input fields, does not need to be translated in all languages
    "en": "Using a browser, go to [sefton.gov.uk](https://www.sefton.gov.uk/bins-and-recycling/bins-and-recycling/when-is-my-bin-collection-day/). "
    "For _Postcode_ and _Street name_ use the values you'd enter on Sefton's first page."
    "Search, and then for _House Name or Number_ you need the value that comes before the street name you entered on the first screen."
    "e.g. if your streetname is 'Liverpool Road' and the select box has an option of '1A Liverpool Road' enter '1A' as your _House Name or Number_."
}

PARAM_DESCRIPTIONS = { # Optional dict to describe the arguments, will be shown in the GUI configuration below the respective input field
    "en": {
        "houseNumberOrName": "House name or number",
        "Streetname": "Street name",
        "Postcode": "Postcode"
    }
}


#### End of arguments affecting the configuration GUI ####

class Source:
    def __init__(self, houseNumberOrName:str | int, Streetname:str, Postcode:str):  # argX correspond to the args dict in the source configuration
        self._houseNumberOrName = houseNumberOrName.upper()
        self._Streetname = Streetname
        self._Postcode = Postcode

    def fetch(self) -> list[Collection]:

        with requests.Session() as sess:
            request = sess.get('https://www.sefton.gov.uk/bins-and-recycling/bins-and-recycling/when-is-my-bin-collection-day/')
            
            soup = BeautifulSoup(request.content, 'html.parser')
            hidden = soup.find_all("input", {'type':'hidden'}, limit=2)
            payload = {x["name"]: x["value"] for x in hidden}
            payload['Postcode'] = self._Postcode
            payload['Streetname'] = self._Streetname
            request = sess.post('https://www.sefton.gov.uk/bins-and-recycling/bins-and-recycling/when-is-my-bin-collection-day/', data=payload)
            #We should now have the page displaying the select list for addresses, parse again to find the form elements we need.
            soup = BeautifulSoup(request.content, 'html.parser')
            hidden = soup.find_all("input", {'type':'hidden'})
            payload = {x["name"]: x["value"] for x in hidden}
            payload['action'] = 'Select'
            option_tags = soup.select('select option')
            for option in option_tags:
                if option.text.upper().strip().startswith(self._houseNumberOrName):
                    payload['selectedValue'] = option['value']
                    break
            request = sess.post('https://www.sefton.gov.uk/bins-and-recycling/bins-and-recycling/when-is-my-bin-collection-day/', data=payload)
            soup = BeautifulSoup(request.content, 'html.parser')
            tables = soup.find_all('table')
            entries = []
            if len(tables) > 0:
                for table in tables:
                    binType = table.td.text.split()[0]
                    binCollectionDate = datetime.datetime.strptime(table.td.findNext('td').findNext('td').text, "%d/%m/%Y").date()
                    entries.append(Collection(date=binCollectionDate, t=binType, icon=ICON_MAP.get(binType.upper())))
            else:
                raise Exception('No entries could be parsed, check the Sefton website is working and your arguments exactly match what you enter online.')
        
        return entries