import pandas as pd
import pickle as pk
# import numpy as np
# import re


# USER_CHARS = pd.read_json('./data/_processed/user_characteristics.json')
# CITY_REVIEWS = pd.read_json('./data/_processed/user_city_ratings.json')

with open("./data/_processed/users_ratings_list.pkl", "rb") as f:
    dsets = pk.load(f)



USER_CHARS = dsets['user_characteristics'] 
CITY_REVIEWS = dsets['city_ratings_matrix']



# if __name__=='__main__':

#     # r = re.compile("ageRange.*")
#     # ages = list(filter(r.match, USER_CHARS.columns))

    # print(dsets['city_ratings_matrix'].head())