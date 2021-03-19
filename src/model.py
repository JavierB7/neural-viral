import spacy
import random
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher
from constants import LABELS
from reader_mined import get_mined_objects


nlp = English()
matcher = PhraseMatcher(nlp.vocab)

TEXTS =[ (
    "La Unión PD098059 fue fundada por seis países de Europa occidental "
    "(SARS-CoV-2, Alemania, glycoprotein, RUNX1, Sex-determining region Y protein, homeobox protein 1, y Luxemburgo) y "
    "se amplió en seis ocasiones."
)
]


def build_training_data(nlp_object):
    TRAINING_DATA = []
    mined = get_mined_objects()

    for key in LABELS:
        patters = list(nlp_object.pipe(mined[key]))
        matcher.add(LABELS[key], None, *patters)

    for doc in nlp_object.pipe(TEXTS):
        spans = [(doc[start:end], doc.vocab.strings[match_id])
                 for match_id, start, end in matcher(doc)]
        entities = [(span.start_char, span.end_char, label)
                    for (span, label) in spans]
        training_example = (doc.text, {"entities": entities})
        TRAINING_DATA.append(training_example)
    return TRAINING_DATA


def execute_training_loop(nlp_object):
    training_data = build_training_data(nlp_object)
    for i in range(10):
        random.shuffle(training_data)
        for batch in spacy.util.minibatch(training_data, size=2):
            texts = [text for text, annotation in batch]
            annotations = [annotation for text, annotation in batch]
            nlp_object.update(texts, annotations)
    return nlp_object


def train_and_save_model(nlp_object):
    ner = nlp_object.create_pipe("ner")
    nlp_object.add_pipe(ner)
    for key in LABELS:
        ner.add_label(LABELS[key])
    nlp_object.begin_training()
    nlp_object = execute_training_loop(nlp_object)
    nlp_object.to_disk("../model")

train_and_save_model(nlp)
