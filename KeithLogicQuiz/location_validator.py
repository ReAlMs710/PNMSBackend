import requests

class LocationValidator:
    def __init__(self):
        self.valid_locations = []

    def initialize_valid_locations(self):
        try:
            response = requests.get("https://restcountries.com/v3.1/all")
            countries = response.json()
            
            for country in countries:
                self.valid_locations.append(country['name']['common'].lower())
                self.valid_locations.extend([alt.lower() for alt in country['altSpellings']])
                if 'demonyms' in country:
                    self.valid_locations.extend(demonym.lower() for demonyms in country['demonyms'].values() for demonym in demonyms.values())
        except:
            # If there's any error, fall back to the original list
            self.valid_locations = [
                "usa", "united states", "united states of america", "canada", "india", 
                "uk", "united kingdom", "england", "germany", "france", "spain", "italy"
            ]

    def is_valid_location(self, location):
        return any(loc in location.lower() for loc in self.valid_locations)