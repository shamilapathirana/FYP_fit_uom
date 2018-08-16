from nltk.tokenize import word_tokenize,regexp_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer,WordNetLemmatizer
import re
from nltk.corpus import wordnet as wn

# stop_words = set(stopwords.words("english"))
# print(stop_words)

# stop_words_file = open("stop_words.txt",'r')

# stop_words = set(stop_words_file.readlines())

# stop_words = [line.rstrip() for line in stop_words_file]

# print(stop_words)


text = "She doesn't cats at that moment."

class Preprocessor:


    # tokenize and stop word removal
    def tokenizeWords(self,phrase):
        filtered_words = []

        # remove non alphanueric characters
        nonalphanumeric_less_phrase = re.sub(r'[^A-Za-z\s]+', '', phrase)

        # tokenize the phase
        tokenized_text = word_tokenize(str(nonalphanumeric_less_phrase))
        # print(tokenized_text)

        #replace negation words
        replaced_negation_words = self.replace_negation(tokenized_text)

        for word in replaced_negation_words:
            if word not in self.stopWords():
                filtered_words.append(word)

        return filtered_words





    # ps = SnowballStemmer('english')
    # lememtizer = WordNetLemmatizer()
    #
    # for word in filtered_words:
    #     stemmed_words.append(ps.stem(word))
    #
    # print(stemmed_words)
    #
    #
    # for word in filtered_words:
    #     lemmetized_words.append(lememtizer.lemmatize(word))
    #
    # print(lemmetized_words)

    # replace negation
    def replace_negation(self,tokenized_word_list):
        filtered_replace_negation = []

        for w in tokenized_word_list:
            try:
                filtered_replace_negation.append(self.select_negation(w))
            except:
                filtered_replace_negation.append(w)

        return filtered_replace_negation




    # wn.synsets('dog', pos=wn.VERB)
    # [Synset('chase.v.01')]
    def stopWords(self):
        stop_words_file = open("stop_words.txt", 'r')
        stop_words = [line.rstrip() for line in stop_words_file]
        return stop_words










    def select_negation(self,x):
        return {
            "no": 'not',
            "never": 'not',
            "cannot": 'not',
            "n't":'not',
            "doesn't":'not',
            "haven't":'not',
            "can't":'not',
            "isn't":'not',
            "aren't":'not',
            "shouldn't":'not',
            "weren't":'not',
            "hasn't ":'not',
            "wasn't ":'not',
            "doesnt":'not',
            "didn't":'not',
            "couldn't":'not',
            "wouldn't":'not',
            "won't ":'not',
            "needn't":'not',
            "mightn't":'not',
            "daren't ":'not',
            "isn’t ":'not',
            "aren’t": 'not',
            "wasn’t ": 'not',
            "weren’t": 'not',
            "hasn’t": 'not',
            "haven’t": 'not',
            "hadn’t": 'not',
            "didn’t": 'not',
            "doesn’t": 'not',
            "don’t ": 'not',
            "can’t": 'not',
            "couldn’t": 'not',
            "won’t": 'not',
            "wouldn’t ": 'not',
            "shouldn’t": 'not',
            "mustn’t": 'not',
            "needn’t ": 'not',
            "mightn’t ": 'not',
            "daren’t": 'not'
        }.get(x, x)



#print(Preprocessor().tokenizeWords(text))




