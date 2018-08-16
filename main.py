from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from werkzeug.security import generate_password_hash, check_password_hash
import operator
import random as rand
import numpy as np
import pandas as pd
from random import *
from support import SimilarUsersInfluence
from hotel_prof_com import HotelProfileCompare
from prof_com import ProfileCompare
from PreprocessModule.TextPreprocess import DataPreprocess
from ClassificationModule.DataClassification import IntegratedClassifier
from UserProfile.MainModule import FeatureExtaction

app = Flask(__name__)

#---------------- creating db connection --------------------------#
app.config['MONGO_DBNAME'] = 'zealous_01'
app.config['MONGO_URI'] = 'mongodb://shamila:Sha123@ds253960.mlab.com:53960/zealous_01'

twitter_blueprint = make_twitter_blueprint(api_key='ih6S8J97RJ4DZmkhVVzkYgnR8',
                                           api_secret='5zMcrDtKtwpFHQ5aJ8meCfPcw5UkwyDp8uPmtGCbOX3tUanjxe',
                                           redirect_to='twitter_log')
app.register_blueprint(twitter_blueprint, url_prefix='/twitter_login')

mongo = PyMongo(app)

RECOMMEND = 5
K = 0.75

@app.route('/')
def index():
    if 'user_email' in session:
        return redirect(url_for('home'))

    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'email': request.form['email']})

    if login_user:
        if login_user and check_password_hash(login_user['password'], request.form['pass']):
            session['user_email'] = request.form['email']
            return redirect(url_for('index'))

    return 'Invalid email & password combination'

@app.route('/logout')
def logout():
    # destroy session variable
    session.pop('user_email', None)
    return redirect(url_for('index'))


@app.route('/home')
def home():
    # access collections of database
    hotels = mongo.db.hotels
    users = mongo.db.users
    usr_hotel_rating = mongo.db.usr_hotel_rating

    # check user logged in
    if 'user_email' in session:
        all_users = users.find()
        all_hotels = hotels.find()
        all_usr_hotel_rating  = usr_hotel_rating .find()

        login_user = users.find_one({'email': session['user_email']})

        # sort user's environment preferences
        sorted_user_env_list = sorted(login_user['environment_p'].items(), key=operator.itemgetter(1), reverse=True)
        sorted_user_env_dic = {key: value for (key, value) in sorted_user_env_list}

        # sort user's food preferences
        sorted_user_food_pref_list = sorted(login_user['food_pref'].items(), key=operator.itemgetter(1), reverse=True)
        sorted_user_food_pref_dic = {key: value for (key, value) in sorted_user_food_pref_list}

        currant_usr_rating = usr_hotel_rating.find_one({"user_id": login_user['_id']})

        # compare other users profiles
        similar_user_ids = []
        for user_v in all_users:
            # check this is I'm
            if user_v['_id'] == login_user['_id']:
                continue

            similarity = 0
            # compare current user's environment preference with other users
            similarity = ProfileCompare.compare_environment_preference(currant_usr_pref = sorted_user_env_dic,
                                                                      other_usr_pref = user_v['environment_p'],
                                                                      similar = similarity)

            # compare current user's food preference with other users
            similarity = ProfileCompare.compare_food_preference(currant_usr_pref = sorted_user_food_pref_dic,
                                                                other_usr_pref = user_v['food_pref'],
                                                                similar = similarity)

            # compare current user's economy level with other users
            similarity = ProfileCompare.compare_eco_level(currant_usr_eco = login_user['eco_level'],
                                                                other_usr_eco = user_v['eco_level'],
                                                                similar = similarity)


            if similarity >= 6:
                # print(user_v['u_name'],'-',similarity)
                similar_user = usr_hotel_rating.find_one({"user_id": user_v['_id']})
                similar_user_ids.append(similar_user['user_id'])

        similar_usrs_final_ratings = SimilarUsersInfluence.find_similar_users_influence(sim_ids = similar_user_ids,
                                                                                        usr_h_ratings = usr_hotel_rating,
                                                                                        all_h = all_hotels,
                                                                                        usrs = users)

        final_hotel_rating = {} #
        currant_user_rating_dict = {} # currant user hotel ratings without effect of similar users
        # calculate final hotel ratings
        for k, v in currant_usr_rating['hotel_rating'].items():
            rate = 0
            if similar_usrs_final_ratings != {}:
                for k2, v2 in similar_usrs_final_ratings.items():
                    if k == k2:
                        rate = (K*v) + np.mean(v2)*(1-K) # formula
                        # print(rate)
                final_hotel_rating[k] = rate
            else:
                final_hotel_rating[k] = v
            currant_user_rating_dict[k] = v

        sorted_currant_user_rating_list = sorted(currant_user_rating_dict.items(), key=operator.itemgetter(1), reverse=True)
        sorted_currant_user_rating_dict = {key: value for (key, value) in sorted_currant_user_rating_list}
        print('\nCurrant user ratings without similar user\'s influence: \n',sorted_currant_user_rating_dict)

        print('\nFinal hotel ratings: \n',final_hotel_rating)

        # sort hotel names and rating dictionary
        sorted_h = sorted(final_hotel_rating.items(), key=operator.itemgetter(1), reverse=True)
        sorted_h2 = {key: value for (key, value) in sorted_h}

        # print sorted output of all hotels
        df = pd.DataFrame.from_dict(sorted_h2, orient='index', columns=['Rating'])
        print(df)

        hotel_arr = []
        for key, value in sorted_h2.items():
            # print(key,' - ', value)
            if value >= RECOMMEND:
                hotel_arr.append(hotels.find({"h_name": key}))

        return render_template('home.html', allhotels = hotel_arr, user = login_user )
    else:
        return redirect(url_for('index'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'email': request.form['email']})

        # check if this is existing user
        if existing_user is None:
            hashpass = request.form['pass']

            # insert values to users collection
            users.insert({'u_name': request.form['username'],
                          'email': request.form['email'],
                          'password': generate_password_hash(hashpass),
                          'age': request.form['age'],
                          'food_pref': {"chinese": round(rand.uniform(0, 1), 2),
                                        "seafood": round(rand.uniform(0, 1), 2),
                                        "bevarage": round(rand.uniform(0, 1), 2)},
                          'environment_p': {"seaside": round(rand.uniform(0, 1), 2),
                                            "urban": round(rand.uniform(0, 1), 2),
                                            "forest": round(rand.uniform(0, 1), 2),
                                            "mountain": round(rand.uniform(0, 1), 2)},
                          'eco_level': randint(1, 6)
                          })

            # create session variable
            session['user_email'] = request.form['email']

            return redirect(url_for('add_account'))

        return 'That user already exists!'

    return render_template('register.html')


@app.route('/add_account', methods=['POST', 'GET'])
def add_account():
    if request.method == 'POST':
        if request.form['action'] == 'twitter':
            return redirect(url_for('twitter_login'))
        elif request.form['action'] == 'not_twitter':
            return redirect(url_for('complete_user_profile'))
    return render_template('add_accounts.html')

@app.route('/twitter_log')
def twitter_login():
    return redirect(url_for('twitter.login'))


@app.route('/twitter')
def twitter_log():
    # if not twitter.authorized:
    #     return redirect(url_for('twitter.login'))
    tweet_info = twitter.get('statuses/user_timeline.json?count=200')
    hotels = mongo.db.hotels
    usr_hotel_rating = mongo.db.usr_hotel_rating
    if tweet_info.ok:
        all_tweets = []
        tweets = tweet_info.json()
        if len(tweets) != 0:
            dict = {}
            for tweet in tweets:
                preprocessed_tweet = DataPreprocess.text_preprocess(tweet=tweet['text'])
                all_tweets.append(preprocessed_tweet)
            predict_list = IntegratedClassifier.accuracy_based_predict(all_tweets)
            for i in range(len(predict_list)):
                dict[all_tweets[i]] = predict_list[i]
            # print(dict)
            users = mongo.db.users
            login_user = users.find_one({'email': session['user_email']})
            raw_tweets = mongo.db.raw_tweets
            raw_tweets.insert({'user_id': login_user['_id'],
                               'user_tweets': dict})

            # -------------------------------------------------------------------

            # Jithmi's module insert here
            FeatureExtaction.create_profile(login_user['_id'])

            # --------------------------------------------------------------------

            login_user2 = users.find_one({'email': session['user_email']})
            HotelProfileCompare.insert_matrix(all_h=hotels, logged_user=login_user2, usr_h_rating=usr_hotel_rating)

    return redirect(url_for('home'))

@app.route('/complete_user_profile', methods=['POST', 'GET'])
def complete_user_profile():
    users = mongo.db.users
    hotels = mongo.db.hotels
    usr_hotel_rating = mongo.db.usr_hotel_rating
    login_user = users.find_one({'email': session['user_email']})

    if request.method == 'POST':
        # get values from complete profile view
        china = request.form['chinese_food']
        sea = request.form['sea_food']
        bev = request.form['beverage']
        seaside = request.form['seaside']
        mountain = request.form['mountain']
        forest = request.form['forest']
        urban = request.form['urban']
        eco_level = int(request.form['eco_level'])

        # update values of current user's preferences
        users.update_one({"_id": login_user['_id']},
                         { '$set': {'eco_level': eco_level,
                                    'food_pref': {"chinese": china,
                                                  "seafood": sea,
                                                  "bevarage": bev},
                                    'environment_p': {"seaside": seaside,
                                                      "urban": urban,
                                                      "forest": forest,
                                                      "mountain": mountain}}})

        login_user2 = users.find_one({'email': session['user_email']})

        HotelProfileCompare.insert_matrix(all_h=hotels, logged_user=login_user2, usr_h_rating=usr_hotel_rating)

        return redirect(url_for('home'))

    return render_template('complete_profile.html', reg_user = login_user)

@app.route('/user_profile')
def user_prof():
    users = mongo.db.users
    if 'user_email' in session:
        login_user = users.find_one({'email': session['user_email']})
        return render_template('user_profile.html', user = login_user)

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)