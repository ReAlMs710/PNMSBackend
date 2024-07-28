import openai
import datetime
import re

# Replace with your own OpenAI API key
openai.api_key = 'sk-proj-nMqG2JPigq7udXlJfFbRT3BlbkFJPXQbeZtbSq4QBV318Bnl'

def log_conversation(log_file, message):
    with open(log_file, "a") as file:
        file.write(f"{datetime.datetime.now()}: {message}\n")

def extract_name(response):
    if 'name is' in response:
        return response.split('name is')[-1].strip()
    return response.strip()

def extract_status(response):
    if 'I am' in response:
        return response.split('I am')[-1].strip()
    if "I'm" in response:
        return response.split("I'm")[-1].strip()
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

def is_valid_location(location):
    # A simple list of known locations. You can expand this list.
    known_locations = [
        "USA", "United States", "United States of America", "Canada", "India", 
        "UK", "United Kingdom", "England", "Germany", "France", "Spain", "Italy"
    ]
    return any(loc.lower() in location.lower() for loc in known_locations)

def is_valid_name(name):
    # Check if the name is at least two words and not just random characters
    return len(name.split()) >= 2 and re.match(r'^[a-zA-Z\s]+$', name)

def grade_conversation(responses):
    score = 100
    feedback = []

    # Check name response
    if not responses[0] or not is_valid_name(responses[0]) or contains_profanity(responses[0]):
        score -= 40
        feedback.append("The name should be at least two words and not contain inappropriate language.")

    # Check status response
    if not responses[1] or len(responses[1].split()) < 2 or contains_profanity(responses[1]):
        score -= 30
        feedback.append("The status should be more than one word and not contain inappropriate language.")

    # Check location response
    if not responses[2] or not is_meaningful(responses[2]) or contains_profanity(responses[2]) or not is_valid_location(responses[2]):
        score -= 30
        feedback.append("The location should be a meaningful response, not contain inappropriate language, and be a valid location.")

    return max(score, 0), feedback

def main():
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

    log_conversation(log_file, f"AI: {conversation[1].format(user_name)}")
    print(f"AI: {conversation[1].format(user_name)}")
    user_response = input("User: ")
    log_conversation(log_file, f"User: {user_response}")
    user_status = extract_status(user_response)
    responses.append(user_status)

    log_conversation(log_file, f"AI: {conversation[2].format(user_name)}")
    print(f"AI: {conversation[2].format(user_name)}")
    user_response = input("User: ")
    log_conversation(log_file, f"User: {user_response}")
    user_location = extract_location(user_response)
    responses.append(user_location)

    log_conversation(log_file, f"AI: {conversation[3].format(user_name)}")
    print(f"AI: {conversation[3].format(user_name)}")

    score, feedback = grade_conversation(responses)
    log_conversation(log_file, f"AI: Your conversation score is {score}%")
    print(f"AI: Your conversation score is {score}%")
    
    if feedback:
        feedback_message = "Feedback on your responses:\n" + "\n".join(feedback)
        log_conversation(log_file, f"AI: {feedback_message}")
        print(f"AI: {feedback_message}")

if __name__ == "__main__":
    main()
