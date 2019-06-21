from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit

rooms_ix,bedrooms_ix, population_ix, households_ix=3,4,5,6


class CombinedAttributesAdder(BaseEstimator, TransformerMixin):

    def __init__(self,add_bedrooms_per_room = True):
        self.add_bedrooms_per_room = add_bedrooms_per_room

    def fit(self,X,y=None):
        return self

    def transform(self, X, y=None):
        rooms_per_household = X[:, rooms_ix] / X[:, households_ix]
        population_per_household = X[:, population_ix] / X[:, households_ix]
        if self.add_bedrooms_per_room:
            bedrooms_per_room = X[:, bedrooms_ix] / X[:, rooms_ix]
            return np.c_[X, rooms_per_household, population_per_household, bedrooms_per_room]
        else:
            return np.c_[X, rooms_per_household, population_per_household]

#TODO this isn't finished. params for the bins?
def stratifiedRandomSplit(data, testPortion, samplingAttrib ):

        # make a categoricl attribute
        data["categories"] = pd.cut(data[samplingAttrib], bins=[0., 1.5, 3.0, 4.5, 6., np.inf],
                                    labels=[1, 2, 3, 4, 5])

        # make arrays of shuffled indices from the dataset that both have the same distribution
        split = StratifiedShuffleSplit(n_splits=1, test_size=testPortion, random_state=42)

        # add the rows from each array to the respective output arrays
        for train_index, test_index in split.split(data, data["income_cat"]):
            testSet = data.loc[test_index]
            trainSet = data.loc[train_index]

        # remove the categoric attribute we created earlier
        for set_ in (testSet, trainSet):
            set_.drop("categories", axis=1, inplace=True)
            # victory!
        return testSet, trainSet
