import re

class ConversationGrader:
    def __init__(self, location_validator):
        self.location_validator = location_validator

    def grade_conversation(self, responses):
        score = 100
        feedback = []

        if not responses[0] or len(responses[0].split()) < 2 or self.contains_profanity(responses[0]):
            score -= 40
            feedback.append("The name should be at least two words and not contain inappropriate language.")

        if not responses[1] or self.contains_profanity(responses[1]):
            score -= 30
            feedback.append("The status should not contain inappropriate language.")

        if not responses[2] or not self.is_meaningful(responses[2]) or self.contains_profanity(responses[2]) or not self.location_validator.is_valid_location(responses[2]):
            score -= 30
            feedback.append("The location should be a meaningful response, not contain inappropriate language, and be a valid location.")

        return max(score, 0), feedback

    def contains_profanity(self, response):
        profanities = ["fuck", "shit", "damn", "bitch"]
        return any(profane in response.lower() for profane in profanities)

    def is_meaningful(self, response):
        meaningless_responses = ["i forgor", "I don't know", "unknown", "not sure"]
        return response.lower() not in meaningless_responses

    def is_valid_name(self, name):
        return len(name.split()) >= 2 and re.match(r"^[a-zA-Z\s']+$", name)