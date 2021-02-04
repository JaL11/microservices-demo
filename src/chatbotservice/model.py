'''

Author: Ming Yeh Oliver Cheung

Copyright (c) 2021 Wise CSE Group 1
'''
import spacy, logging, random, os
from spacy.util import minibatch, compounding, decaying
from spacy.scorer import Scorer
from pathlib import Path

SEP = os.path.sep

class Model:

    def __init__(self):
        self.training_data = {"Fun_Fact": [ "can you tell me a fun fact?",
                                            "show me a fun fact",
                                            "i want a fun fact",
                                            "tell me anything",
                                            "i want to learn something new",
                                            "i want to learn about a fun fact"
                                            "tell me something",
                                            "talk to me",
                                            "say something",
                                            "tell me something new",
                                            "how about a fun fact"],
                                "Recommendation": ["recommend me something",
                                                    "show me your wares",
                                                    "what do you offer",
                                                    "i want to buy something",
                                                    "show me something interesting"],
                                "Welcome":["hello",
                                            "hi",
                                            "good day to you",
                                            "greetings",
                                            "morning",
                                            "hello there",
                                            "how are you",
                                            "how is your day",]}

    def preprocess_data(self):
        labelled_data = []
        for cat in self.training_data:
            for sentence in self.training_data[cat]:
                labelled_data = labelled_data + [(sentence, {'cats': {cat: 1.0}})]

        return labelled_data

    def load_model(self, labelled_data, model= None):
        """ loads a spacy language model and prepares pipeline
        
        Keywords argument:
        model -- spacy model to load, set to None for a new blank model

        Return:
        nlp -- loaded model

        """

        # TODO DYNAMIC ADJUSTMENT FOR STUFF THAT NEEDS TO BE ADDED TO PIPELINE
        if model is not None:
            nlp = spacy.load(model)
            logging.info("Loaded model %s", str(model))
        else:
            nlp = spacy.blank("en")  # create blank Language class
            logging.info("Created blank 'en' model")

        # create the built-in pipeline components and add them to the pipeline
        # nlp.create_pipe works for built-ins that are registered with spaCy

        if "textcat" not in nlp.pipe_names:
            textcat = nlp.create_pipe("textcat", config={"exclusive_classes": True})
            nlp.add_pipe(textcat, last=True)
        # otherwise, get it so we can add labels
        else:
            textcat = nlp.get_pipe("textcat")

            # add labels
        for _, annotations in labelled_data:
            for cat in annotations.get("cats"):
                textcat.add_label(cat)

        return nlp

    def train_intent(self, nlp, output_dir, train_data,n_iter = 70, dropout = 0.25):
        """Load the model, set up the pipeline and train the entity recognizer.
        

        Keyword arguments:
        model -- path to the model if existent
        output_dir -- path where model is saved at
        n_iter -- amount of times data is trained with
        train_data -- training data in BILOU Format

        Returns:
        output_dir -- path to model
        """

        logging.info("Started training intents...")
        nlp.begin_training()
        for iteration in range(n_iter):
            random.shuffle(train_data)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=dropout,  # dropout - make it harder to memorise data
                    losses=losses
                )
            logging.info("Finished %s iteration for text classification with %s losses", iteration, losses)
        logging.info("Finished training intents...")

        # save model to output directory
        if output_dir is not None:
            output_dir = Path(output_dir)
            if not output_dir.exists():
                output_dir.mkdir()
            nlp.to_disk(output_dir)
            logging.info("Saved model to %s", output_dir)

        return output_dir

if __name__ == "__main__":
    """Trains a language model"""

    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                        filename="logs.txt",
                        datefmt='%d/%m/%Y %I:%M:%S %p',
                        filemode='w', level=logging.DEBUG)

    logging.info("Start spacy model training")
    logging.info("Spacy is using GPU: %s", spacy.prefer_gpu())
    model = Model()
    labelled_data = model.preprocess_data()
    nlp = model.load_model(labelled_data, None)
    model = model.train_intent(nlp, "models" + SEP + "onlineshop", labelled_data)
    logging.info("Finished training, saved model at %s", model)