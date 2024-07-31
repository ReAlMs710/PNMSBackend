from response_extractor import ResponseExtractor

class ConversationHandler:
    def __init__(self, location_validator, logger):
        self.logger = logger
        self.state = 0
        self.location_validator = location_validator
        self.response_extractor = ResponseExtractor()

    def printandlog(self, str):
        self.logger.log(str)
        # print(str)

    def run_conversation(self, user_input=""):
        response = ""
        extracted_info = ""

        match self.state:
            case 0:
                response = "Keith: Hello! What is your name?"
                self.state += 1
            case 1:
                extracted_info = self.response_extractor.extract_name(user_input)
                response = f"Keith: Nice to meet you, {extracted_info}! How are you doing today?"
                self.state += 1
            case 2:
                extracted_info = self.response_extractor.extract_status(user_input)
                response = "Keith: That's great to hear! Where are you from?"
                self.state += 1
            case 3:
                extracted_info = self.response_extractor.extract_location(user_input)
                response = f"Keith: Wonderful! It was nice talking to you. Goodbye!"
                self.state += 1
            case _:
                response = "Conversation has ended."

        self.printandlog(response)
        return response, extracted_info