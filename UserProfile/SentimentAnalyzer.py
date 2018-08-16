import os
import pickle

class SentimentAnalysis:

    def food_sentiment_score(tweet):
        scriptpath = os.path.dirname(__file__)

        tweets = []
        tweets.append(tweet)

        cv = open(scriptpath + "\\Models\\food_countvector.pickle", "rb")
        feedback_vec = pickle.load(cv)
        cv.close()

        tfidf = open(scriptpath + "\\Models\\food_tfidf.pickle", "rb")
        tfidf_transformer = pickle.load(tfidf)
        tfidf.close()

        classifier_t = open(scriptpath + "\\Models\\food_sentimentclassifier.pickle", "rb")
        clf = pickle.load(classifier_t)
        classifier_t.close()

        tweets_new_counts = feedback_vec.transform(tweets)
        tweets_new_tfidf = tfidf_transformer.transform(tweets_new_counts)

        pred1 = clf.predict(tweets_new_tfidf)
        pred2 = clf.predict_proba(tweets_new_tfidf)

        if pred1[0] == 'pos':
            return pred2[0][1]
        else:
            return pred2[0][0] * -1

    def env_sentiment_score(tweet):
        scriptpath = os.path.dirname(__file__)

        tweets = []
        tweets.append(tweet)

        cv = open(scriptpath + "\\Models\\env_countvector.pickle", "rb")
        feedback_vec = pickle.load(cv)
        cv.close()

        tfidf = open(scriptpath + "\\Models\\env_tfidf.pickle", "rb")
        tfidf_transformer = pickle.load(tfidf)
        tfidf.close()

        classifier_t = open(scriptpath + "\\Models\\env_sentimentclassifier.pickle", "rb")
        clf = pickle.load(classifier_t)
        classifier_t.close()

        tweets_new_counts = feedback_vec.transform(tweets)
        tweets_new_tfidf = tfidf_transformer.transform(tweets_new_counts)

        pred1 = clf.predict(tweets_new_tfidf)
        pred2 = clf.predict_proba(tweets_new_tfidf)

        if pred1[0] == 'pos':
            return pred2[0][1]
        else:
            return pred2[0][0] * -1