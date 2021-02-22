'''

Author: Ming Yeh Oliver Cheung

Copyright (c) 2021 Wise CSE Group 1
'''
import logging, random, os 
import chatbot_client
from nlp_engine import NlpEngine
from monitor import Monitor

SEP = os.path.sep

class MetaEngine:
    """ Creates a meta-engine that can handles user messages
        and chooses an appropriate action from a dict 
    """

    def __init__(self):
        """ initialises Meta-engine with all necessary components
        """
        logging.info("Started Meta Engine...")
        self.nlp = NlpEngine("models" + SEP + "onlineshop")
        self.actions = {"Fun_Fact": 
                            ["Google has the largest index of websites in the world.",
                            "The original name of Google was Backrub.",
                            "The Google search technology is called PageRank."],
                        "Welcome":
                            ["Hello there!", 
                            "Hi!",
                            "Welcome to our amazing online shop!",
                            "Beautiful day isn't it?",
                            "Feels like a perfect day for online shopping!",],
                        "Help":
                            ["I can recommend you items, greet you and tell you a fun fact",
                            "Try asking for recommendation :)",
                            "Try asking for a fun fact :)",
                            "Try greeting me :)"],
                        None: ["I'm sorry coulnd't quite understand you there, mind rephrasing that for me?",
                                "Currently I'm not smart enough for that yet but I'll try my best to improve!",
                                "I'm sorry, I didn't understand that."]}

    def handle_message(self, text, user_id = "test"):
        """ Gets classification of user input 
            and chooses appropriate return message

        Args:
            text (str): Input message from User

        Returns:
            [str]: message that is randomly chosen from self.actions and send to you user
        """
        user_action = self.nlp.textcat(text)
        logging.info(f"Found action {user_action}")
        if (user_action == "Recommendation"):
            messages = get_recommendations(user_id)
        else:
            messages = self.actions.get(user_action)

        try:
            random.shuffle(messages)
        except:
            return str(messages)
        return str(messages[0])

    def get_recommendations(self, id, products = ["test"]):
        """ Gets recommendations from recommendationservice
        """
        return[chatbot_client.get_rec(id)]    

if __name__ == "__main__":
    """For quick local testing purposes only!"""
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                        filename="logs.txt",
                        datefmt='%d/%m/%Y %I:%M:%S %p',
                        filemode='w', level=logging.DEBUG)

    engine = MetaEngine()

    while True:
        message = input("Please enter something: ")
        print(engine.handle_message(message))

