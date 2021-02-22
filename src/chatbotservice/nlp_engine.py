'''

Author: Ming Yeh Oliver Cheung

Copyright (c) 2021 Wise CSE Group 1
'''
import spacy, logging

class NlpEngine:
    """ Loads the nlp model and uses it to classify user input
    """
    def __init__(self, model):
        logging.info("Started Meta Engine...")
        self.nlp = self.load(model)
        self.doc = None

    def load(self, model_path):
        """ load a given spacy model


            Keyword arguments:
            model_path -- path to where model is located

            Returns:
            nlp -- spacy pipeline containing language model

        """
        nlp = spacy.load(model_path)
        logging.info("Loaded spacy model at %s", model_path)

        return nlp

    def make_doc(self, text):
        if text:
            self.doc = self.nlp(text)
            logging.info("Processed text %s in pipeline", text)

    def textcat(self, input_text):
        """ extract intents from given text


        Keyword arguments:
        input_text -- sentence that should be processed for intent as a string

        Returns:
        result -- intent with label and certainty

        """
        self.make_doc(input_text)

        logging.info("Classifying text...")
        if len(self.doc.cats) == 0:  # if no intents return empty dict
            return {}
        intent = max(self.doc.cats, key=self.doc.cats.get)

        logging.debug("Found intents: %s", self.doc.cats)

        if self.doc.cats[intent] < 0.3:
            logging.info("Intent certainty too low, defaults to None")
            return None

        logging.info("Succesfully classified text returning intent")
        return intent