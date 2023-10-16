import pandas as pd
import numpy as np
from sklearn.metrics import euclidean_distances

class Distancer:
    def __init__(self, user_matrix, method = 'euclidean'):

        assert isinstance(user_matrix, pd.core.frame.DataFrame), 'Supply pandas DataFrame'

        self.user_matrix = user_matrix
        self.method = method
        self.joint = None

    def __repr__(self):
        return f'distance calculation using {self.method}'

    def calculate(self, new_user):

        assert isinstance(new_user, pd.core.frame.DataFrame)

        assert (self.user_matrix.shape[1]) == new_user.shape[1], "need same number of features"
        # assert all(self.user_matrix.columns in new_user.columns)

        match self.method:
            case 'euclidean':


                joint = pd.concat([self.user_matrix, new_user], axis = 0)

                
                self.joint = joint
                distances = euclidean_distances(
                    joint.drop('username', axis = 1),
                    )
            
            # default to euclidean
            case _:
                distances = None
                raise ValueError("Method unknown, please provide euclidean")

        distances = pd.DataFrame(distances)

        distances.index = joint['username']
        distances.columns = joint['username']

            
        self.distances = distances

        return distances


    def top_n_closest(self, n):

        assert self.joint is not None, "Please provide a new user and calculate distances first"

        distances_new_user = self.distances.iloc[:-1,-1].sort_values(ascending=True)[0:n]
        
        return distances_new_user