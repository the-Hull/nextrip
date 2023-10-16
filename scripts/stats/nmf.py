import pandas as pd
import numpy as np
from sklearn.decomposition import NMF

def subset_reviews(usernames, city_ratings_matrix):
    subset = city_ratings_matrix.loc[[str(u) for u in usernames], :]
    return subset



class nmfer:

    def __init__(self, reviews, n_components = 20):       
        self.n_components = n_components
        self.reviews = reviews
        self.model = None
        self.visited_cities = None
    
    def __repr__(self):
        return f'NMF set up for {self.n_components} on {len(self.reviews)} reviews for {len(self.reviews.columns)} cities.'


    def set_model(self):
        self.model = NMF(n_components=self.n_components, random_state=1,max_iter = 300)
        self.model.fit(self.reviews)

        return self.model

    def new_review(self, top_cities, bottom_cities = None, other_ratings = 2.5):
    
        new_review = self.reviews.copy()
        new_review = new_review.iloc[-1:,:]
        new_review.iloc[0,:] = other_ratings

        new_review.index = ['_flaskuser']

        assert top_cities is not None, "provide top cities"

        # check if top cities all exist in cities
        cities = list(new_review.columns)
        city_check = [tc in cities for tc in top_cities]
        
        assert all(city_check), f'Provided city/cities not in database:\n {np.array(top_cities)[[not c for c in city_check]]}'
        
        new_review.loc[:,top_cities] = 5

        if bottom_cities:

            # city_check = [tc in cities for tc in bottom_cities]
            # assert all(city_check), f'Provided city/cities not in database:\n {np.array(top_cities)[[not c for c in city_check]]}'
            new_review.loc[:,bottom_cities] = 0

        

        self.visited_cities = top_cities + bottom_cities if bottom_cities is not None else top_cities

        return new_review
    
    def get_best_cities(self, X, n = 5):

        assert self.model is not None, "use set_model() first."
        assert self.visited_cities is not None, "use new_review() first."


        preds = self.model.transform(X)

        preds = np.dot(preds, self.model.components_)

        preds = pd.DataFrame(preds, columns = self.reviews.columns).T
        preds.columns = ['predicted_rating']
        preds.sort_values(by = 'predicted_rating', inplace=True, ascending = False)
        preds.drop(index = self.visited_cities, inplace = True)



        return preds.iloc[0:n, ]
