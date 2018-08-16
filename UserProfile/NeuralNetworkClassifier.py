from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import random
import itertools
import os
import pickle
import numpy as np
from keras.models import load_model

class NeuralNetwork:

    def food_classify(tweet):
        scriptpath = os.path.dirname(__file__)

        mymodel = load_model(scriptpath + "\\Models\\foodmode1.h5")

        food_tokenize = open(scriptpath + "\\Models\\food_tokenize.pickle", "rb")
        tokenize = pickle.load(food_tokenize)
        food_tokenize.close()

        new_tweet = tokenize.texts_to_matrix([tweet])

        food_encoder = open(scriptpath + "\\Models\\food_encoder.pickle", "rb")
        encoder = pickle.load(food_encoder)
        food_tokenize.close()

        text_labels = encoder.classes_
        prediction = mymodel.predict(np.array([new_tweet[0]]))
        predicted_label = text_labels[np.argmax(prediction)]
        return predicted_label


    def env_classify(tweet):
        scriptpath = os.path.dirname(__file__)

        mymodel = load_model(scriptpath + "\\Models\\envmodel.h5")

        env_tokenize = open(scriptpath + "\\Models\\env_tokenize.pickle", "rb")
        tokenize = pickle.load(env_tokenize)
        env_tokenize.close()

        new_tweet = tokenize.texts_to_matrix([tweet])

        env_encoder = open(scriptpath + "\\Models\\env_encoder.pickle", "rb")
        encoder = pickle.load(env_encoder)
        env_encoder.close()

        text_labels = encoder.classes_
        prediction = mymodel.predict(np.array([new_tweet[0]]))
        predicted_label = text_labels[np.argmax(prediction)]
        return predicted_label

    def eco_classify(tweet):
        scriptpath = os.path.dirname(__file__)

        mymodel = load_model(scriptpath + "\\Models\\economymode1.h5")

        eco_tokenize = open(scriptpath + "\\Models\\eco_tokenize.pickle", "rb")
        tokenize = pickle.load(eco_tokenize)
        eco_tokenize.close()

        new_tweet = tokenize.texts_to_matrix([tweet])

        eco_encoder = open(scriptpath + "\\Models\\eco_encoder.pickle", "rb")
        encoder = pickle.load(eco_encoder)
        eco_encoder.close()

        text_labels = encoder.classes_
        prediction = mymodel.predict(np.array([new_tweet[0]]))
        predicted_label = text_labels[np.argmax(prediction)]
        return predicted_label

