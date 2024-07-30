from chatbot import ChatBot

def main():
    api_key = 'sk-proj-nMqG2JPigq7udXlJfFbRT3BlbkFJPXQbeZtbSq4QBV318Bnl'
    chatbot = ChatBot(api_key)
    chatbot.run_conversation()

if __name__ == "__main__":
    main()