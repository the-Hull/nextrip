import pandas as pd
import numpy as np


paths = { 
    'user_profiles' : './_etl/tripadvisor/users_full_7034.xlsx', 
    'user_personalities' : './_etl/tripadvisor/pers_scores_1098.xlsx',
    'user_reviews' : './_etl/tripadvisor/reviews_32618_for_1098_users_with_location.xlsx'
    }

dsets = {}

for k, path in paths.items():
    dsets[k] = pd.read_excel(io = path)


## profiles ---------------------------------------------------------------------------------------

### Add 'missing' as travelStyle for NAs
dsets['user_profiles'].loc[dsets['user_profiles']['travelStyle'].isna() ,'travelStyle'] = 'missing'
### Calculate 2 most frequent classes and fill travel styles based on their weights
dsets['user_profiles']['travelStyle_split'] = dsets['user_profiles']['travelStyle'].apply(lambda x: x.strip().split(', '))

style_dic = {}
for wl in dsets['user_profiles']['travelStyle_split'].values:
  for k in wl:
    style_dic[k] = style_dic.get(k, 0) + 1


style_dic = dict(sorted(style_dic.items(), key = lambda x: x[1], reverse = True))

# weight_foodie = style_dic['Foodie'] / (style_dic['Foodie'] + style_dic['Like a Local'])
# weight_local = style_dic['Like a Local'] / (style_dic['Foodie'] + style_dic['Like a Local'])

total = np.sum([v for k, v in style_dic.items() if k not in  ['missing']])

weights = [v/total for k, v in style_dic.items() if k not in  ['missing']]
styles = [k for k in style_dic.keys() if k not in  ['missing']]



n_missing = len(dsets['user_profiles'].loc[dsets['user_profiles']['travelStyle'] == 'missing', "travelStyle"])
dsets['user_profiles'].loc[dsets['user_profiles']['travelStyle'] == 'missing', "travelStyle"] = \
    np.random.choice(a = styles, p = weights, size = n_missing)

### Adjust age
age_na = dsets['user_profiles']['ageRange'].isna()
dsets['user_profiles']['ageRange'] = dsets['user_profiles']['ageRange'] \
    .where(~age_na, dsets['user_profiles'][['ageRange']].mode().values[0][0])

### Get number of all reviews
cols = ['numHotelsReviews', 'numRestReviews',
       'numAttractReviews', 'numRatings']
nas = dsets['user_profiles'].loc[:, cols].isna()
dsets['user_profiles']['ratings_sum'] = dsets['user_profiles'] \
    .loc[:, cols].where(~nas, 0) \
        .apply(lambda x: x.astype('float'), axis = 1) \
            .apply(sum, axis = 1)


## user characteristics ---------------------------------------------------------------------------

### Join personalities and OHE age and travel style

# re-do
dsets['user_profiles']['travelStyle_split'] = dsets['user_profiles']['travelStyle'].apply(lambda x: x.strip().split(', '))

# Make OHE travel style df
row_list = [None] * len(dsets['user_profiles'])
for row in dsets['user_profiles'][['travelStyle_split']].iterrows():
    user_name = dsets['user_profiles']['username'][row[0]]    
    temp = pd.get_dummies(pd.Series(row[1][0])).apply(sum, axis = 0).to_frame().T
    temp['username'] = user_name
    row_list[row[0]] = temp

dsets['user_styles'] = pd.concat(row_list)
# fill NAs with 0
condi = dsets['user_styles'].isna()
dsets['user_styles'] = dsets['user_styles'].where(~condi, 0)


# Make OHE age
dsets['user_ageranges'] = pd.get_dummies(dsets['user_profiles'][['ageRange','username']], columns = ['ageRange'])

# MERGE age, styles, personalities
dsets['user_characteristics'] = pd.merge(
    left = pd.merge(
        left = dsets['user_personalities'], 
        right = dsets['user_ageranges'],
        how = 'left',
        on = 'username'),
    right = dsets['user_styles'],
    how = 'left',
    on = 'username')

# city reviews ------------------------------------------------------------------------------------
city_ratings_by_user = dsets['user_reviews'] \
    .groupby(['username', 'taObjectCity']) \
        .agg(
            n = ('rating', len), 
            rating_mean = ('rating', np.mean), 
            rating_median = ('rating', np.median)
            )

city_ratings_matrix = pd.pivot(
    city_ratings_by_user \
    .reset_index(level=[0,1]) \
        [['username', 'taObjectCity', 'rating_median']],
        index= 'username',
        columns= 'taObjectCity',
        values= 'rating_median'
        )
# fill missing values with medians
city_medians = city_ratings_matrix.median()
city_ratings_matrix = city_ratings_matrix.apply(lambda x: x.where(~x.isna(), city_medians[x.name]), axis = 0)

cities_gr_five_reviews = dsets['user_reviews'] \
    .groupby(['taObjectCity']) \
        .agg(
            n = ('rating', len), 
            rating_mean = ('rating', np.mean), 
            rating_median = ('rating', np.median)
            ) \
                .sort_values(by = 'n', ascending = False) \
                    .query('n > 5').index


# city_ratings_matrix = city_ratings_matrix.loc[:, cities_gr_five_reviews]

# Save relevant dicts/dfs -----------------------------------------------------------------------------

# dsets['user_characteristics'].to_json("./data/_processed/user_characteristics.json")
# city_ratings_matrix.to_json("./data/_processed/user_city_ratings.json")
dsets['city_ratings_matrix'] = city_ratings_matrix

# print(city_ratings_matrix.axes)

dsets['city_ratings_matrix'].axes[1].name = None
dsets['city_ratings_matrix'].index = dsets['city_ratings_matrix'].index.astype(str)

import pickle as pk

with open('./data/_processed/users_ratings_list.pkl', 'wb') as f:
   pk.dump(dsets, f)




