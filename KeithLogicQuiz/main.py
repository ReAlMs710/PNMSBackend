from conversation_runner import ConversationRunner

def main():
    # Initialize the ConversationRunner with necessary parameters
    runner = ConversationRunner(
        api_key="sk-proj-nMqG2JPigq7udXlJfFbRT3BlbkFJPXQbeZtbSq4QBV318Bnl",
        lesson_plan="basic greetings and introductions",
        user_language="spanish",
        lesson_questions=[
            "How do you say 'Hello' in Spanish?",
            "What's the phrase for 'How are you?' in Spanish?",
            "How would you introduce yourself in Spanish?"
        ]
    )

    # Start conversation
    response = runner.next()
    print("Assistant:", response)

    while not runner.conversation_ended:
        user_input = input("User: ")
        response = runner.next(user_input)
        print("Assistant:", response)

if __name__ == "__main__":
    main()