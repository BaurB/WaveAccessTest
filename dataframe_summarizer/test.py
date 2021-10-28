'''Testing constructed module

Main test with examples are in Jupyter notebook
'''
import urllib.request
from pathlib import Path
import os
import pandas as pd
import pytest
import numpy as np
from dataframe_stats import StatisticalDescription

def load_iris_dataset():
    """Loads iris dataset from official url. Script is used because pytest constantly showed
    error during the sklearn.datasets.load_iris import
    """
    url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
    column_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']

    filepath = Path('data/iris_data')
    filepath.parent.mkdir(exist_ok=True)

    urllib.request.urlretrieve(url, str(filepath))
    df = pd.read_csv(str(filepath), names=column_names)

    filepath.unlink()
    df.to_csv(filepath, index=False)

    return df.iloc[:, 0:4] # Return only numerical columns

@pytest.fixture()
def iris_dataset():
    df = load_iris_dataset()
    return df

def test_summarizer_and_caclulate_stats(iris_dataset):
    summarizer = StatisticalDescription(iris_dataset.columns)
    assert summarizer is not None
    statistics = summarizer.populate_df(iris_dataset)
    expected_shape = (13, 4)
    # print('my stats shape:',statistics.shape)
    assert statistics is not None
    assert statistics is not None
    assert statistics.shape == expected_shape