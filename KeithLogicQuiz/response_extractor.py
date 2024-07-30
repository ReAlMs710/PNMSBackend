class ResponseExtractor:
    def extract_name(self, response):
        response = response.lower()
        name_indicators = ["name is", "i'm", "i am", "call me", "it's"]
        
        for indicator in name_indicators:
            if indicator in response:
                name_part = response.split(indicator)[-1].strip()
                name_words = name_part.split()
                if len(name_words) >= 2:
                    return ' '.join(name_words[:2]).title()
                elif len(name_words) == 1:
                    return name_words[0].title()
        
        words = response.split()
        if len(words) >= 2:
            return ' '.join(words[-2:]).title()
        elif len(words) == 1:
            return words[0].title()
        
        return response.strip().title()

    def extract_status(self, response):
        response = response.lower()
        status_indicators = ["i am", "i'm", "feeling", "doing"]
        for indicator in status_indicators:
            if indicator in response:
                return response.split(indicator)[-1].strip()
        return response.strip()

    def extract_location(self, response):
        if 'I am from' in response:
            return response.split('I am from')[-1].strip()
        return response.strip()