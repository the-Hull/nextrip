import pandas as pd
# import numpy as np
# import re


USER_CHARS = pd.read_json('./data/_processed/user_characteristics.json')
CITY_REVIEWS = pd.read_json('./data/_processed/user_city_ratings.json')

# if __name__=='__main__':

    # r = re.compile("ageRange.*")
    # ages = list(filter(r.match, USER_CHARS.columns))

    # print(ages)