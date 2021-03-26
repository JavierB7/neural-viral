import spacy
import random
from spacy.matcher import PhraseMatcher
from constants import LABELS
from reader import get_mined_objects, get_examples


def clean_overlapping_tokens(entities):
    seen_ranges = set()
    new_entities = []
    for start, end, label in entities:
        if start not in seen_ranges and end - 1 not in seen_ranges:
            new_entities.append((start, end, label))
        seen_ranges.update((start, end))
    return new_entities


def build_training_data(nlp_object, matcher):
    print("-Building training data...")
    TRAINING_DATA = []
    mined = get_mined_objects()
    examples = get_examples()
    print("-Read examples file successfully!")
    for key in LABELS:
        patters = list(nlp_object.pipe(mined[key]))
        matcher.add(LABELS[key], None, *patters)

    for doc in nlp_object.pipe(examples):
        spans = [(doc[start:end], doc.vocab.strings[match_id])
                 for match_id, start, end in matcher(doc)]
        entities = [(span.start_char, span.end_char, label)
                    for (span, label) in spans]
        entities = clean_overlapping_tokens(entities)
        training_example = (doc.text, {"entities": entities})
        TRAINING_DATA.append(training_example)
    return TRAINING_DATA


def execute_training_loop(nlp_object, matcher):
    training_data = build_training_data(nlp_object, matcher)
    print("-Training data built successfully!")
    print("-Executing training loop...")
    for i in range(10):
        random.shuffle(training_data)
        for batch in spacy.util.minibatch(training_data, size=10):
            texts = [text for text, annotation in batch]
            annotations = [annotation for text, annotation in batch]
            try:
                nlp_object.update(texts, annotations)
            except ValueError as exception:
                print(exception)
                error = exception
    return nlp_object


def train_and_save_model(nlp_object):
    matcher = PhraseMatcher(nlp_object.vocab)
    ner = nlp_object.create_pipe("ner")
    nlp_object.add_pipe(ner)
    for key in LABELS:
        ner.add_label(LABELS[key])
    nlp_object.begin_training()
    nlp_object = execute_training_loop(nlp_object, matcher)
    print("-Training loop executed successfully!")
    print("-Saving model...")
    nlp_object.to_disk("../model")
