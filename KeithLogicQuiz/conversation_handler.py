from response_extractor import ResponseExtractor

class ConversationHandler:
    def __init__(self, location_validator):
        self.location_validator = location_validator
        self.response_extractor = ResponseExtractor()
        self.conversation = [
            "Hello! What is your name?",
            "Nice to meet you, {}! How are you doing today?",
            "That's great to hear, {}! Where are you from?",
            "Wonderful! It was nice talking to you, {}. Goodbye!"
        ]

    def run_conversation(self, logger):
        responses = []

        logger.log("Keith: Hello! What is your name?")
        print("Keith: Hello! What is your name?")
        user_response = input("User: ")
        logger.log(f"User: {user_response}")
        user_name = self.response_extractor.extract_name(user_response)
        responses.append(user_name)

        logger.log(f"Keith: Nice to meet you, {user_name}! How are you doing today?")
        print(f"Keith: Nice to meet you, {user_name}! How are you doing today?")
        user_response = input("User: ")
        logger.log(f"User: {user_response}")
        user_status = self.response_extractor.extract_status(user_response)
        responses.append(user_status)

        logger.log(f"Keith: That's great to hear, {user_name}! Where are you from?")
        print(f"Keith: That's great to hear, {user_name}! Where are you from?")
        user_response = input("User: ")
        logger.log(f"User: {user_response}")
        user_location = self.response_extractor.extract_location(user_response)
        responses.append(user_location)

        logger.log(f"Keith: Wonderful! It was nice talking to you, {user_name}. Goodbye!")
        print(f"Keith: Wonderful! It was nice talking to you, {user_name}. Goodbye!")

        return responses