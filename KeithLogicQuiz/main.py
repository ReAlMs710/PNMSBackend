from conversation_runner import ConversationRunner

def main():
    runner = ConversationRunner()

    # Start conversation
    while True:
        user_input = input("User: ")
        response = runner.next(user_input)
        print(response)
        if "Conversation Score" in response:
            break

if __name__ == "__main__":
    main()
