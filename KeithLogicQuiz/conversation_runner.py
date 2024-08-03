import openai

class ConversationRunner:
    def __init__(self, api_key, lesson_plan, user_language, lesson_questions):
        openai.api_key = api_key
        self.lesson_plan = lesson_plan
        self.user_language = user_language
        self.lesson_questions = lesson_questions
        self.state = 0
        self.responses = []
        self.conversation_ended = False

    def translate_text(self, text, to_english=False):
        try:
            if to_english:
                prompt = f"Translate the following text into English:\n\n{text}"
            else:
                prompt = f"Translate the following text into {self.user_language}:\n\n{text}"
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that translates text accurately."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )
            
            return response.choices[0]['message']['content'].strip()
        except Exception as e:
            print(f"Error during translation: {e}")
            return "Sorry, there was an error during translation."

    def teach_lesson(self):
        prompt = f"""Your task is to teach a beginner about {self.lesson_plan}. The user's primary language is {self.user_language}, but you should teach the core concepts in English. Follow these steps:

1. Teaching Phase:
   - Introduce the lesson in {self.user_language}.
   - Teach the core concepts in English, but provide explanations and context in {self.user_language}.
   - Focus only on the content related to the testing questions.

2. Practice Phase:
   - Ask at least 10 practice questions in {self.user_language}, but include the key terms in English.
   - Do this ONE AT A TIME.
   - After each response, evaluate it in {self.user_language}, explain any errors, then ask the next question.
   - DO NOT SKIP THIS STEP.

3. Test Phase:
   - Announce that the test is starting in {self.user_language}.
   - Ask one full, relevant question at a time related to {self.lesson_plan} in {self.user_language}, but keep key terms in English.
   - Wait for the student's response after each question.
   - If they answer incorrectly or incompletely, explain what they did wrong in {self.user_language} and provide the correct information.
   - Continue until all test questions have been asked and answered.

Remember to be patient, encouraging, and supportive throughout the entire process. Adapt your teaching style based on the student's responses and understanding.

Please begin with the Teaching Phase."""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": "Please start the lesson."}
                ],
                max_tokens=500
            )
            
            return response.choices[0]['message']['content'].strip()
        except Exception as e:
            print(f"Error during teaching lesson: {e}")
            return f"Lo siento, hubo un error durante la fase de enseñanza." if self.user_language == "Spanish" else "Sorry, there was an error during the teaching phase."

    def test_user(self):
        questions = self.translate_text(', '.join(self.lesson_questions))
        return f"{'¡Excelente! Ahora vamos a evaluar tu comprensión. Por favor, responde las siguientes preguntas' if self.user_language == 'Spanish' else 'Great! Now let\'s test your understanding. Please answer the following questions'}:\n\n{questions}"

    def evaluate_responses(self):
        evaluation_prompt = f"""You are a fair and constructive evaluator. The student was taught about {self.lesson_plan} in {self.user_language}, with key terms in English. They were asked these questions: {', '.join(self.lesson_questions)}. Their responses were: {', '.join(self.responses)}. 

Evaluate their performance and provide feedback. The feedback should be in {self.user_language}, but you can use English terms where appropriate. Consider:
1. Did they understand the key English terms?
2. How well did they apply the concepts?
3. What areas need improvement?
4. What did they do well?

Provide encouraging and constructive feedback."""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": evaluation_prompt},
                    {"role": "user", "content": "Please evaluate the student's responses."}
                ],
                max_tokens=300
            )
            
            feedback = response.choices[0]['message']['content'].strip()
            return feedback
        except Exception as e:
            print(f"Error during evaluation: {e}")
            return "Lo siento, hubo un error durante la evaluación." if self.user_language == "Spanish" else "Sorry, there was an error during evaluation."

    def next(self, user_input=None):
        if self.conversation_ended:
            return "La lección ya ha terminado. ¡Gracias por participar!" if self.user_language == "Spanish" else "The lesson has already ended. Thank you for participating!"

        if self.state == 0:
            self.state += 1
            return self.teach_lesson()
        elif self.state == 1:
            self.state += 1
            return self.test_user()
        elif 2 <= self.state < len(self.lesson_questions) + 2:
            if user_input:
                self.responses.append(user_input)
            if self.state - 1 < len(self.lesson_questions):
                next_question = self.lesson_questions[self.state - 2]
                translated_question = self.translate_text(next_question)
                self.state += 1
                return f"{'Gracias. Siguiente pregunta' if self.user_language == 'Spanish' else 'Thank you. Next question'}: {translated_question}"
            else:
                self.state += 1
                return "Gracias por completar las preguntas. Evaluando las respuestas ahora." if self.user_language == "Spanish" else "Thank you for completing the questions. Evaluating responses now."
        elif self.state == len(self.lesson_questions) + 2:
            if user_input:
                self.responses.append(user_input)
            feedback = self.evaluate_responses()
            self.conversation_ended = True
            return feedback
        else:
            self.conversation_ended = True
            return "La lección ha terminado. ¡Gracias por participar!" if self.user_language == "Spanish" else "The lesson has ended. Thank you for participating!"