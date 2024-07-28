import openai
import datetime

# Replace with your own OpenAI API key
openai.api_key = 'your-api-key-here'

def log_conversation(log_file, message):
    with open(log_file, "a") as file:
        file.write(f"{datetime.datetime.now()}: {message}\n")

def get_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    return response.choices[0].text.strip()

def main():
    log_file = "chatlogconvo.txt"
    conversation = [
        "Hello! What is your name?",
        "Nice to meet you, {}! How are you doing today?",
        "That's great to hear, {}! Where are you from?",
        "Wonderful! It was nice talking to you, {}. Goodbye!"
    ]

    prompt = "Hello! What is your name?"
    log_conversation(log_file, "AI: Hello! What is your name?")
    print("AI: Hello! What is your name?")
    user_name = input("User: ")
    log_conversation(log_file, f"User: {user_name}")

    prompt += f"\nUser: {user_name}\nAI: {conversation[1].format(user_name)}"
    log_conversation(log_file, f"AI: {conversation[1].format(user_name)}")
    print(f"AI: {conversation[1].format(user_name)}")
    user_status = input("User: ")
    log_conversation(log_file, f"User: {user_status}")

    prompt += f"\nUser: {user_status}\nAI: {conversation[2].format(user_name)}"
    log_conversation(log_file, f"AI: {conversation[2].format(user_name)}")
    print(f"AI: {conversation[2].format(user_name)}")
    user_location = input("User: ")
    log_conversation(log_file, f"User: {user_location}")

    prompt += f"\nUser: {user_location}\nAI: {conversation[3].format(user_name)}"
    log_conversation(log_file, f"AI: {conversation[3].format(user_name)}")
    print(f"AI: {conversation[3].format(user_name)}")

if __name__ == "__main__":
    main()
