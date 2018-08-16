from support import CompareFeatures
import operator

class HotelProfileCompare:
    def insert_matrix(all_h, logged_user, usr_h_rating):

        all_hotels = all_h.find()  # {"famous_food": "chinese"}

        # sort current user environment preferences
        sorted_user_env_list = sorted(logged_user['environment_p'].items(), key=operator.itemgetter(1), reverse=True)
        sorted_user_env_dic = {key: value for (key, value) in sorted_user_env_list}

        # sort current user food preferences
        sorted_user_food_pref_list = sorted(logged_user['food_pref'].items(), key=operator.itemgetter(1),
                                            reverse=True)
        sorted_user_food_pref_dic = {key: value for (key, value) in sorted_user_food_pref_list}

        h_rating_hash = {}

        # hotel profile comparison
        for hotel_v in all_hotels:

            rating = 0

            # check user's food preference with hotel's famous food
            rating1 = CompareFeatures.check_food_preference(h_food=hotel_v['food'],
                                                           usr_food=sorted_user_food_pref_dic, rate=rating)
            # check user's environment preference with hotel's environment
            rating2 = CompareFeatures.check_environment_preference(env_hotel=hotel_v['environment'],
                                                                  user_env=sorted_user_env_dic, rate=rating1)
            # check user's economy with hotel class
            rating3 = CompareFeatures.check_economy_level(h_class=hotel_v['class'], usr_eco=logged_user['eco_level'],
                                                         rate=rating2)
            # check hospitality of the staff
            rating4 = CompareFeatures.check_staff_hospitality(h_staff=hotel_v['staff'], rate=rating3)

            # check hotel's food quality
            final_rate = CompareFeatures.check_food_quality(food=hotel_v['food_q'], rate=rating4)

            # create hotel names and rating dictionary
            h_rating_hash[hotel_v['h_name']] = final_rate

        # insert hotel names and rating dictionary into usr_hotel_rating collection
        usr_h_rating.insert({'user_id': logged_user['_id'], 'hotel_rating': h_rating_hash})
