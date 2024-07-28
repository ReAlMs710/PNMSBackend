import openai
import datetime
import re
import requests

# Replace with your own OpenAI API key
openai.api_key = 'sk-proj-nMqG2JPigq7udXlJfFbRT3BlbkFJPXQbeZtbSq4QBV318Bnl'

# Global variable to store valid locations
valid_locations = []

def initialize_valid_locations():
    global valid_locations
    try:
        response = requests.get("https://restcountries.com/v3.1/all")
        countries = response.json()
        
        for country in countries:
            valid_locations.append(country['name']['common'].lower())
            valid_locations.extend([alt.lower() for alt in country['altSpellings']])
            if 'demonyms' in country:
                valid_locations.extend(demonym.lower() for demonyms in country['demonyms'].values() for demonym in demonyms.values())
    except:
        # If there's any error, fall back to the original list
        valid_locations = [
            "usa", "united states", "united states of america", "canada", "india", 
            "uk", "united kingdom", "england", "germany", "france", "spain", "italy"
        ]

def is_valid_location(location):
    return any(loc in location.lower() for loc in valid_locations)

def log_conversation(log_file, message):
    with open(log_file, "a") as file:
        file.write(f"{datetime.datetime.now()}: {message}\n")

def extract_name(response):
    response = response.lower()
    name_indicators = ["name is", "i'm", "i am", "call me", "it's"]
    
    for indicator in name_indicators:
        if indicator in response:
            name_part = response.split(indicator)[-1].strip()
            # Split the name part and take the last two words (if available)
            name_words = name_part.split()
            if len(name_words) >= 2:
                return ' '.join(name_words[:2]).title()
            elif len(name_words) == 1:
                return name_words[0].title()
    
    # If no indicator is found, take the last two words of the response
    words = response.split()
    if len(words) >= 2:
        return ' '.join(words[-2:]).title()
    elif len(words) == 1:
        return words[0].title()
    
    return response.strip().title()

def extract_status(response):
    response = response.lower()
    status_indicators = ["i am", "i'm", "feeling", "doing"]
    for indicator in status_indicators:
        if indicator in response:
            return response.split(indicator)[-1].strip()
    return response.strip()

def extract_location(response):
    if 'I am from' in response:
        return response.split('I am from')[-1].strip()
    return response.strip()

def is_meaningful(response):
    meaningless_responses = ["i forgor", "I don't know", "unknown", "not sure"]
    return response.lower() not in meaningless_responses

def contains_profanity(response):
    # A simple profanity filter, you can expand this list
    profanities = ["fuck", "shit", "damn", "bitch"]
    return any(profane in response.lower() for profane in profanities)

def is_valid_name(name):
    # Allow names with apostrophes (e.g., O'Brien)
    return len(name.split()) >= 2 and re.match(r"^[a-zA-Z\s']+$", name)

def grade_conversation(responses):
    score = 100
    feedback = []

    # Check name response
    if not responses[0] or len(responses[0].split()) < 2 or contains_profanity(responses[0]):
        score -= 40
        feedback.append("The name should be at least two words and not contain inappropriate language.")

    # Check status response
    if not responses[1] or contains_profanity(responses[1]):
        score -= 30
        feedback.append("The status should not contain inappropriate language.")

    # Check location response
    if not responses[2] or not is_meaningful(responses[2]) or contains_profanity(responses[2]) or not is_valid_location(responses[2]):
        score -= 30
        feedback.append("The location should be a meaningful response, not contain inappropriate language, and be a valid location.")

    return max(score, 0), feedback

def main():
    initialize_valid_locations()
    log_file = "chatlogconvo.txt"
    conversation = [
        "Hello! What is your name?",
        "Nice to meet you, {}! How are you doing today?",
        "That's great to hear, {}! Where are you from?",
        "Wonderful! It was nice talking to you, {}. Goodbye!"
    ]

    responses = []

    log_conversation(log_file, "AI: Hello! What is your name?")
    print("AI: Hello! What is your name?")
    user_response = input("User: ")
    log_conversation(log_file, f"User: {user_response}")
    user_name = extract_name(user_response)
    responses.append(user_name)

    log_conversation(log_file, f"AI: Nice to meet you, {user_name}! How are you doing today?")
    print(f"AI: Nice to meet you, {user_name}! How are you doing today?")
    user_response = input("User: ")
    log_conversation(log_file, f"User: {user_response}")
    user_status = extract_status(user_response)
    responses.append(user_status)

    log_conversation(log_file, f"AI: That's great to hear, {user_name}! Where are you from?")
    print(f"AI: That's great to hear, {user_name}! Where are you from?")
    user_response = input("User: ")
    log_conversation(log_file, f"User: {user_response}")
    user_location = extract_location(user_response)
    responses.append(user_location)

    log_conversation(log_file, f"AI: Wonderful! It was nice talking to you, {user_name}. Goodbye!")
    print(f"AI: Wonderful! It was nice talking to you, {user_name}. Goodbye!")

    # ... rest of the function remains the same

if __name__ == "__main__":
    main()