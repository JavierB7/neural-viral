import spacy
nlp = spacy.load("../model")


text = (
    "La Unión PD098059 fue fundada por seis países de Europa occidental "
    "(j, Alemania, glycoprotein, RUNX1, Sex-determining region Y protein, homeobox protein 1, y Luxemburgo) y "
    "se amplió en seis ocasiones."
)


doc = nlp(text)
for ent in doc.ents:
    print(ent.text, ent.label_)