import numpy as np
import os
import pickle
from ClassificationModule.AccuracyBasedClassifier import AccuracyBased



class IntegratedClassifier:

    # Accuracy based Classifier
    def accuracy_based_predict(tweets):
        scriptpath = os.path.dirname(__file__)

        # ----------------Load TF-IDF Vectorizer----------------------#
        tf_vector = open(scriptpath+"/PickleData/TFIDFvector.pickle", "rb")
        tfidf_vector = pickle.load(tf_vector)
        tf_vector.close()
        # ------------------------------------------------------------#

        # ---------------Load MNB classifier--------------------------#
        mnb_classifier = open(scriptpath+"/PickleData/MNBclassifier.pickle", "rb")
        multinomialNB_classifier = pickle.load(mnb_classifier)
        mnb_classifier.close()
        # ------------------------------------------------------------#

        # --------------------MNB accuracy----------------------------#
        mnb_accuracy = open(scriptpath+"/PickleData/MNBaccuracy.pickle", "rb")
        acc_MNB = pickle.load(mnb_accuracy)
        mnb_accuracy.close()
        # ------------------------------------------------------------#

        # --------------------Linear SVC Classifier-------------------#
        lsvc_classifier = open(scriptpath+"/PickleData/LSVCclassifier.pickle", "rb")
        linearSVC_classifier = pickle.load(lsvc_classifier)
        lsvc_classifier.close()
        # ------------------------------------------------------------#

        # --------------------LSVC accuracy---------------------------#
        lsvc_accuracy = open(scriptpath+"/PickleData/LSVCaccuracy.pickle", "rb")
        acc_LSVC = pickle.load(lsvc_accuracy)
        lsvc_accuracy.close()
        # ------------------------------------------------------------#

        # --------------------LRClassifier----------------------------#
        logr_classifier = open(scriptpath+"/PickleData/LRclassifier.pickle", "rb")
        logisticRegression_classifier = pickle.load(logr_classifier)
        logr_classifier.close()
        # ------------------------------------------------------------#

        # --------------------LSVC accuracy---------------------------#
        logr_accuracy = open(scriptpath+"/PickleData/LRaccuracy.pickle", "rb")
        acc_LogR = pickle.load(logr_accuracy)
        logr_accuracy.close()
        # ------------------------------------------------------------#

        tweets_tf = tfidf_vector.transform(tweets)
        prediction_array = AccuracyBased.predict(mnb_classifier=multinomialNB_classifier, mnb_acc=acc_MNB,
                                           logreg_classifier=logisticRegression_classifier, logreg_acc=acc_LogR,
                                           linsvc_classifier=linearSVC_classifier, linsvc_acc=acc_LSVC,
                                           tweets_tf=tweets_tf)
        return prediction_array
