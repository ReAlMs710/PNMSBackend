import openai

class ConversationRunner:
    def __init__(self):
        openai.api_key = 'sk-proj-nMqG2JPigq7udXlJfFbRT3BlbkFJPXQbeZtbSq4QBV318Bnl'
        self.state = 0
        self.responses = []

    def next(self, user_input=None):
        if self.state == 0:
            self.state += 1
            return "Hello! What's your name?"
        elif self.state == 1:
            self.responses.append(user_input)
            self.state += 1
            return "How are you feeling today?"
        elif self.state == 2:
            self.responses.append(user_input)
            self.state += 1
            return "Where are you from?"
        elif self.state == 3:
            self.responses.append(user_input)
            self.state += 1
            return self.grade_conversation()
        else:
            return "Conversation has ended."

    def grade_conversation(self):
        feedback = []
        questions = [
            "Did the user properly state their name? ",
            "Did the user properly state how they are feeling today?",
            "Did the user properly state where they are from?"
        ]
        
        pass_count = 0
        
        for i, response in enumerate(self.responses):
            try:
                result = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": f"{questions[i]}\n\nUser response: {response}"}
                    ],
                    max_tokens=150
                )
                feedback_text = result.choices[0].message['content'].strip()
                feedback.append(feedback_text)
                
                if "properly" in feedback_text.lower():
                    pass_count += 1
            except Exception as e:
                feedback.append(f"Error: {e}")
        
        pass_threshold = len(questions)  # All questions must be answered properly to pass
        pass_status = "You have passed!" if pass_count == pass_threshold else "You have not passed."
        
        feedback.append(pass_status)
        return "\n".join(feedback)