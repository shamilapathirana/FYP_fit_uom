import operator


class ProfileCompare:

    def compare_environment_preference(currant_usr_pref, other_usr_pref, similar):
        sorted_usr_env_list = sorted(other_usr_pref.items(), key=operator.itemgetter(1), reverse=True)
        sorted_usr_env_dic = {key: value for (key, value) in sorted_usr_env_list}

        if list(currant_usr_pref)[0] == list(sorted_usr_env_dic)[0]:
            similar += 3
            if list(currant_usr_pref)[1] == list(sorted_usr_env_dic)[1]:
                similar  += 1
        elif list(currant_usr_pref)[0] == list(sorted_usr_env_dic)[1] or list(currant_usr_pref)[1] == list(sorted_usr_env_dic)[0]:
            similar += 2
        return similar

    def compare_food_preference(currant_usr_pref, other_usr_pref, similar):
        sorted_usr_food_list = sorted(other_usr_pref.items(), key=operator.itemgetter(1), reverse=True)
        sorted_usr_food_dic = {key: value for (key, value) in sorted_usr_food_list}

        if list(currant_usr_pref)[0] == list(sorted_usr_food_dic)[0]:
            similar += 3
            if list(currant_usr_pref)[1] == list(sorted_usr_food_dic)[1]:
                similar  += 1
        elif list(currant_usr_pref)[0] == list(sorted_usr_food_dic)[1] or list(currant_usr_pref)[1] == list(sorted_usr_food_dic)[0]:
            similar += 2
        return similar

    def compare_eco_level(currant_usr_eco, other_usr_eco, similar):
        if currant_usr_eco - other_usr_eco == 0:
            similar += 3
        elif abs(currant_usr_eco - other_usr_eco) == 1:
            similar += 1.5
        return similar