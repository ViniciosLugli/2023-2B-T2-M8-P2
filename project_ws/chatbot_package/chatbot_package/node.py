import re
import os

# Set DEBUG flag based on the environment variable 'DEBUG'
DEBUG = True if os.environ.get('DEBUG') else False
# Define a debug printing function that only prints if DEBUG is True
debug_print = print if DEBUG else lambda *args, **kwargs: None

# Class to extract tokens using regular expressions


class RegexExtractor:
    # Predefined patterns for matching commands in sentences
    PATTERNS = [
        re.compile(r'(take me to|go to|head to|lead me to)\s+(shelf\s+[A-Z]\d+|office\s+\d+|sector\s+\d+|room\s+\d+)', re.IGNORECASE),
    ]

    @staticmethod
    def extract(sentence):
        # Check each pattern for a match in the sentence
        for pattern in RegexExtractor.PATTERNS:
            match = pattern.search(sentence)
            if match:
                # Return matched groups as a list if a match is found
                return list(match.groups())
        # Return an empty list if no matches are found
        return []

# Class to classify tokens into categories


class Lexer:
    # Keywords that indicate a location
    LOCATION_KEYWORDS = {'shelf', 'office', 'sector', 'room'}

    def classify(self, tokens):
        classified_tokens = []
        # Classify each token based on predefined keywords
        for token in tokens:
            if token.split()[0].lower() in self.LOCATION_KEYWORDS:
                classified_tokens.append((token, 'Location'))
            else:
                classified_tokens.append((token, 'Unknown'))

        return classified_tokens

# Class to recognize intents from classified tokens


class IntentRecognizer:
    # Mapping of categories to intent creation functions
    INTENT_MAP = {
        'Location': lambda location: 'NavigateTo' + location.title(),
    }

    def recognize(self, classified_tokens):
        intents = []
        args = []
        # Create intents and args based on the token categories
        for token, category in classified_tokens:
            if category in self.INTENT_MAP:
                intent = self.INTENT_MAP[category](token.split()[0])
                intents.append(intent)
                args.append(token.split()[1])
        return (intents, args)

# Class to map intents to specific actions


class ActionMapper:
    # Mapping of intents to action functions
    ACTIONS = {
        'NavigateToShelf': lambda location: f'Moving to shelf {location}',
        'NavigateToOffice': lambda location: f'Moving to office {location}',
        'NavigateToSector': lambda location: f'Moving to sector {location}',
        'NavigateToRoom': lambda location: f'Moving to room {location}',
    }

    def map_action(self, intents, args):
        actions = []
        # Map each intent to its corresponding action
        for (intent, arg) in zip(intents, args):
            if intent in self.ACTIONS:
                action = self.ACTIONS[intent](arg)
                actions.append(action)
        return actions

# Main chatbot class


class ChatBot:
    def __init__(self):
        # Initialize components of the chatbot
        self.extractor = RegexExtractor()
        self.lexer = Lexer()
        self.intent_recognizer = IntentRecognizer()
        self.action_mapper = ActionMapper()

    def process(self, sentence):
        # Extract tokens from the sentence
        tokens = self.extractor.extract(sentence)
        debug_print(tokens, end=' => ')

        # Return a message if no valid tokens are found
        if not tokens:
            return ['No valid command recognized']

        # Classify extracted tokens
        classified_tokens = self.lexer.classify(tokens)
        debug_print(classified_tokens, end=' => ')

        # Recognize intents from the classified tokens
        (intents, args) = self.intent_recognizer.recognize(classified_tokens[1:])
        debug_print((intents, args), end=' => ')

        # Map intents to actions
        actions = self.action_mapper.map_action(intents, args)
        debug_print(actions)

        # Return a message if no valid actions are found
        if not actions:
            return ['No valid action recognized']
        return actions[0]


# Main execution block
def main():
    bot = ChatBot()

    '''
    Examples inputs:
    take me to shelf A1
    go to office 1
    go to shelf C3
    head to sector 2
    lead me to room 3
    '''

    # Continuously process user input until the program is stopped
    while True:
        try:
            sentence = input('Enter a command: ')
            print(bot.process(sentence))
        except KeyboardInterrupt:
            print('\nExiting...')
            break
        except Exception as e:
            print(e)
