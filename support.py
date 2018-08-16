import operator
import numpy as np

class CompareFeatures:

    def check_staff_hospitality(h_staff, rate):

        if h_staff == 1:
            rate += 0.75
        elif h_staff == 0:
            rate += 0.25
        else:
            rate -= 0.5
        return rate

    def check_environment_preference(env_hotel, user_env, rate):

        sorted_hotel_env_list = sorted(env_hotel.items(), key=operator.itemgetter(1), reverse=True)
        sorted_hotel_env_dic = {key: value for (key, value) in sorted_hotel_env_list}

        if list(user_env)[0] == list(sorted_hotel_env_dic)[0]:
            rate += (4 * list(sorted_hotel_env_dic.values())[0])

            if list(user_env)[1] == list(sorted_hotel_env_dic)[1]:
                rate += (3 * list(sorted_hotel_env_dic.values())[1])

        elif list(user_env)[1] == list(sorted_hotel_env_dic)[0]:
            rate += (3 * list(sorted_hotel_env_dic.values())[0])

            if list(user_env)[2] == list(sorted_hotel_env_dic)[1]:
                rate += (1 * list(sorted_hotel_env_dic.values())[1])

        elif list(user_env)[2] == list(sorted_hotel_env_dic)[0]:
            rate += (-1 * list(sorted_hotel_env_dic.values())[0])

        return rate

    def check_economy_level(h_class, usr_eco, rate):
        if h_class - usr_eco == 0:
            rate += 2
        elif abs(h_class - usr_eco) == 1:
            rate += 1
        elif abs(h_class - usr_eco) == 2:
            rate = rate
        else:
            if h_class > usr_eco:
                rate-= 2
        return rate

    def check_food_preference(h_food, usr_food, rate):
        sorted_hotel_food_pref_list = sorted(h_food.items(), key=operator.itemgetter(1), reverse=True)
        sorted_hotel_food_pref_dic = {key: value for (key, value) in sorted_hotel_food_pref_list}

        if list(usr_food)[0] == list(sorted_hotel_food_pref_dic)[0]:
            rate += (2 * list(sorted_hotel_food_pref_dic.values())[0])

            if list(usr_food)[1] == list(sorted_hotel_food_pref_dic)[1]:
                rate += (1 * list(sorted_hotel_food_pref_dic.values())[1])

        elif list(usr_food)[1] == list(sorted_hotel_food_pref_dic)[0]:
            rate += (1 * list(sorted_hotel_food_pref_dic.values())[0])

        return rate

    def check_food_quality(food, rate):
        if food == 5 or food == 4:
            rate += 1
        elif food == 3 or food == 2:
            rate += 0.5
        else:
            rate -= 1
        return rate




class SimilarUsersInfluence:

    def find_similar_users_influence(sim_ids, usr_h_ratings, all_h, usrs):
        hash_table = {}
        np.v_arr = []
        count = 0  # count number of similar users
        # find similar user's hotel list
        for i in sim_ids:
            sim = usr_h_ratings.find_one({"user_id": i})
            s_user = usrs.find_one({"_id": sim['user_id']})
            print('Similar user',count+1,'email: ', s_user['email'])

            for k, v in sim['hotel_rating'].items():
                np.v_arr.append(v)  # ratings insert into array
                hash_table[k] = v
            count += 1

        all_count = all_h.count()  # count all number of hotels
        hash_table2 = {}
        i = 0
        for k2, v2 in hash_table.items():
            # break subset from hotel rating array
            np.rate_arr = np.v_arr[(0 + i):(all_count + 1 + i):all_count]
            i += 1
            hash_table2[k2] = np.rate_arr  # assign array subsets to hotel names
        return hash_table2

# def main():
#     a = CompareFeatures()
#     a.check_food_quality()
#
#
# if __name__ =='__main__':
#     main()