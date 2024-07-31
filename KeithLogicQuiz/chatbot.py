import openai
from conversation_handler import ConversationHandler
from location_validator import LocationValidator
from conversation_grader import ConversationGrader
from logger import Logger

class ChatBot:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key
        self.logger = Logger("chatlogconvo.txt")
        self.location_validator = LocationValidator()
        self.conversation_handler = ConversationHandler(self.location_validator, self.logger)
        self.conversation_grader = ConversationGrader(self.location_validator)
        self.responses = []

    def run_conversation(self):
        self.location_validator.initialize_valid_locations()
        while self.conversation_handler.state < 4:
            user_input = input("User: ") if self.conversation_handler.state > 0 else ""
            if user_input.lower() == "grade my english":
                english_input = input("Please enter the text you want graded: ")
                feedback = self.grade_english(english_input)
                print(f"AI: {feedback}")
                self.logger.log(f"User: {user_input}")
                self.logger.log(f"AI: {feedback}")
                continue

            response, extracted_info = self.conversation_handler.run_conversation(user_input)
            if extracted_info:
                self.responses.append(extracted_info)
            print(response)
            self.logger.log(f"User: {user_input}")
            self.logger.log(f"AI: {response}")

        score, feedback = self.conversation_grader.grade_conversation(self.responses)
        
        print(f"\nConversation Score: {score}")
        if feedback:
            print("Feedback:")
            for item in feedback:
                print(f"- {item}")

    def grade_english(self, text):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Grade the following text for English proficiency and provide feedback:\n\n{text}",
            max_tokens=150
        )
        feedback = response.choices[0].text.strip()
        return feedback