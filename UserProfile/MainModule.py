from UserProfile.Ontology import OntologyModule
from UserProfile.SentimentAnalyzer import SentimentAnalysis
from UserProfile.NeuralNetworkClassifier import NeuralNetwork
from UserProfile.ScoreGenerator import ScoreCalculator
from flask_pymongo import MongoClient


class FeatureExtaction:
    def create_profile(user_id):
        MongoDBuri = 'mongodb://shamila:Sha123@ds253960.mlab.com:53960/zealous_01'

        client = MongoClient(MongoDBuri, connectTimeoutMS='30000')
        database = client.get_database(name='zealous_01')
        users = database.users
        raw_tweets = database.raw_tweets

        food = []
        environment = []
        economy = []

        # ----------------get logged user data--------------#
        tweet_detail = raw_tweets.find_one({'user_id': user_id})
        # --------------------------------------------------#
        # print(tweet_detail)
        user_tweet = tweet_detail['user_tweets']
        for k, v in user_tweet.items():
            food_preference = []
            env_preference = []
            economy_level = []
            if v == 'Food':
                food_preference = OntologyModule.food_ontology(k)
                if not food_preference:
                    food_preference.append(NeuralNetwork.food_classify(k))
                score = SentimentAnalysis.food_sentiment_score(k)

                for pref in food_preference:
                    food.append((pref, score))

            elif v == 'Environment':
                env_preference = OntologyModule.env_ontology(k)
                if not env_preference:
                    env_preference.append(NeuralNetwork.env_classify(k))
                score = SentimentAnalysis.env_sentiment_score(k)

                for pref in env_preference:
                    environment.append((pref, score))

            elif v == 'Finance':
                economy_level = OntologyModule.eco_ontology(k)
                if not economy_level:
                    economy_level.append(NeuralNetwork.eco_classify(k))

                for pref in economy_level:
                    economy.append(pref)

        food_total = 15
        env_total = 15
        eco_high_count = 0
        eco_low_count = 0
        chine = []
        sea = []
        rur = []
        mount = []
        beach = []
        indian = []
        economy_size = len(economy)

        for elementf in food:
            if elementf[0]=='Chinese':
                chine.append(elementf[1])
            elif elementf[0]=='Seafood':
                sea.append(elementf[1])
            elif elementf[0] == 'Indian':
                indian.append(elementf[1])
            food_total = food_total + elementf[1]

        for elementf in environment:
            if elementf[0] == 'Beach':
                beach.append(elementf[1])
            elif elementf[0] == 'Rural':
                rur.append(elementf[1])
            elif elementf[0] == 'Mountains':
                mount.append(elementf[1])
            env_total = env_total + elementf[1]

        for elementf in economy:
            if elementf[0] == 'High':
                eco_high_count = eco_high_count + 1
            elif elementf[0] == 'Low':
                eco_low_count = eco_low_count + 1

        if len(chine) > 0:
            final_chinese = round(ScoreCalculator.score_generate(array=chine, total=food_total), 3)
        else:
            final_chinese = 0.0
        if len(indian) > 0:
            final_indian = round(ScoreCalculator.score_generate(array=indian, total=food_total), 3)
        else:
            final_indian = 0.0
        if len(sea) > 0:
            final_sea = round(ScoreCalculator.score_generate(array=sea, total=food_total), 3)
        else:
            final_sea = 0.0
        if len(beach) > 0:
            final_beach = round(ScoreCalculator.score_generate(array=beach, total=env_total), 3)
        else:
            final_beach = 0.0
        if len(mount) > 0:
            final_mountain = round(ScoreCalculator.score_generate(array=mount, total=env_total), 3)
        else:
            final_mountain = 0.0
        if len(rur) > 0:
            final_rural = round(ScoreCalculator.score_generate(array=rur, total=env_total), 3)
        else:
            final_rural = 0.0
        if economy_size > 0:
            economy_level = ScoreCalculator.get_eco_level(high_count=eco_high_count, eco_size=economy_size)
        else:
            economy_level = 3
        # ---------------------------DB Write here --------------------#
        # print(final_beach, final_chinese, final_mountain, final_rural, final_sea, economy_level)
        users.update_one({"_id": user_id},
                         {'$set': {'eco_level': int(economy_level),
                                   'food_pref': {"chinese": final_chinese,
                                                 "seafood": final_sea,
                                                 "bevarage": final_indian
                                                },
                                   'environment_p': {"seaside": final_beach,
                                                     "forest": final_rural,
                                                     "mountain": final_mountain}}})
        # -------------------------------------------------------------#