from spacy.lang.en import English
from model import train_and_save_model
from settings import MADE_BY


nlp = English()

print("Made by: {}".format(MADE_BY))
print("Training neural network!")
train_and_save_model(nlp)
print("Training complete!, your model was saved in /model folder.")
print("Now you can run test.py to use your created model.")