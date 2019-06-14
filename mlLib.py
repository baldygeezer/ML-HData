import pandas as pd
import numpy as numpty
from sklearn.model_selection import StratifiedShuffleSplit


def stratifiedSlice (data, testPortion, Numlabels):

    data["income_cat"]= pd.cut(data["median_income"],bins=[0., 1.5, 3.0, 4.5, 6., numpty.inf], labels=[1, 2, 3, 4, 5])
    split=StratifiedShuffleSplit(n_splits=1,test_size=testPortion, random_state=42)
    for train_index, test_index in split.split(data, data["income_cat"]):
        testSet=data.loc[test_index]
        trainSet=data.loc[train_index]
    for set_ in (testSet,trainSet):
        set_.drop("income_cat",axis=1,inplace=True)
    return testSet, trainSet