'''

Author: Ming Yeh Oliver Cheung

Copyright (c) 2021 Wise CSE Group 1
'''
import spacy, logging, random, os, json
from spacy.util import minibatch, compounding, decaying
from spacy.scorer import Scorer
from pathlib import Path

SEP = os.path.sep

class Trainer:

    def __init__(self, path):
        self.training_data = self.convert_data(path)

    def convert_data(self, path):
        """ takes training Data in RASA Format and converts it into the BILOU Format
        
        Keyword arguments:
        path -- path to the Training Data file

        Returns:
        TRAINING_DATA -- TRAINING DATA as BILOU Format
        """

        training_data = []

        with open(path) as json_file:
            data = json.load(json_file)

        examples = data['rasa_nlu_data']['common_examples']
        all_cats = set()
        [all_cats.add(example["intent"]) for example in examples]
        #access dictionary and save into variables
        examples = data['rasa_nlu_data']['common_examples']
        for example in examples:
            intents = {}
            entities = []
            sentence = example["text"]
            cat = example["intent"]
            for cats in all_cats:
                if cats == cat:
                    intents[cats] = 1.0
                else:
                    intents[cats] = 0.0
            for entity in example["entities"]:
                label = entity["entity"]
                label_start = entity["start"]
                label_end = entity["end"]   
                tupel = (label_start, label_end, label)
                entities.append((tupel))
            

            #puts the labels in the right format into TRAINING_DATA
            training_data = training_data + [(sentence, {"entities":entities},{'cats':intents}),]
        
        return training_data

    def load_model(self, model= None):
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
        for _, _,annotations in self.training_data:
            for cat in annotations.get("cats"):
                textcat.add_label(cat)

        return nlp

    def train_intent(self, nlp, output_dir, n_iter = 3, dropout = 0.25):
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
            random.shuffle(self.training_data)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(self.training_data, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, _,annotations = zip(*batch)
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
    model = Trainer("trainingdata.json")    
    nlp = model.load_model()
    model = model.train_intent(nlp, "onlineshop")
    logging.info("Finished training, saved model at %s", model)