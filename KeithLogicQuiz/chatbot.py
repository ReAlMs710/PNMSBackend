import openai
from conversation_handler import ConversationHandler
from location_validator import LocationValidator
from conversation_grader import ConversationGrader
from logger import Logger

class ChatBot:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key
        self.location_validator = LocationValidator()
        self.conversation_handler = ConversationHandler(self.location_validator)
        self.conversation_grader = ConversationGrader(self.location_validator)
        self.logger = Logger("chatlogconvo.txt")

    def run_conversation(self):
        self.location_validator.initialize_valid_locations()
        responses = self.conversation_handler.run_conversation(self.logger)
        score, feedback = self.conversation_grader.grade_conversation(responses)
        
        print(f"\nConversation Score: {score}")
        if feedback:
            print("Feedback:")
            for item in feedback:
                print(f"- {item}")