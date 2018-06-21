from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk import pos_tag

wnl = WordNetLemmatizer()

sentence = "i am going to get some fast dogs and then lets go running after i am done"
print(sentence)
tokenized_sentence = word_tokenize(sentence)
pos_tag_sentence = pos_tag(tokenized_sentence)

def get_wordnet_pos(treebank_tag):
    # pos_tag uses treebank corpus
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

new_sentence = []

for i in pos_tag_sentence:
    tag = get_wordnet_pos(i[1])

    # words like to and and don't need to be lemmatized and return ""
    if tag != "":
        word = wnl.lemmatize(i[0], tag)
        new_sentence.append(word)
    # and to, and, and other words
    else:
        new_sentence.append(i[0])

new_sentence = " ".join(new_sentence)
print(new_sentence)
