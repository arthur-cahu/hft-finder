"""Loads data with some default read_csv settings.
CSV files need to be in the same folder for the load_data and load_test functions to work.
"""

import os
import pandas as pd
from copy import copy

# default read_csv settings
defaults = {"header": 0}
defaults_x = {"index_col": 0}
defaults_y = {}


def load_csv(filename, data_folder=".\data", **kwargs):
    """Loads the selected csv file.

    Args:
        filename (path-like): "local" file name in the specified folder.
        folder (path-like, optional): folder where the file is located. Defaults to ".\data".
    Any additional kwargs will be passed on to `pandas.read_csv` and override defaults (see `data_loader.py`).

    Returns:
        df: a dataframe containing the data of the input file.
    """
    
    full_filename = os.path.join(data_folder, filename)
    settings = copy(defaults)
    settings.update(kwargs)
    return pd.read_csv(full_filename, **settings)


def load_data(data_folder=".\data", **kwargs):
    """Loads the training DataFrames as a couple.

    Args:
        data_folder (path-like): The data folder to look for the csv files in. Defaults to ".\data".
        data_filenames (list of path-likes, optional): The filenames of the training data. Defaults to ["data_x.csv", "data_y.csv"].
    Any additional kwargs will be passed on to `pandas.read_csv` and override defaults (see `data_loader.py`).

    Returns:
        data_x, data_y: the training DataFrames. 
    """
    for filename in os.listdir(data_folder):
        if filename.find("train_X")>=0:
            train_x_filename = filename
        elif filename.find("train_Y")>=0:
            train_y_filename = filename

    settings = copy(defaults_x)
    settings.update(kwargs)
    
    data_x = load_csv(train_x_filename, data_folder, **settings)
    settings = copy(defaults_y)
    settings.update(kwargs)
    data_y = load_csv(train_y_filename, data_folder, **settings)
    return data_x, data_y


def load_test(data_folder=".\data", **kwargs):
    """Loads the test DataFrame.

    Args:
        data_folder (path-like): The data folder to look for the csv file in. Defaults to ".\data".
        data_filenames (path-like, optional): The filename of the test data. Defaults to "test.csv".
    Any additional kwargs will be passed on to `pandas.read_csv` and override defaults (see `data_loader.py`).

    Returns:
        test_x: the test DataFrame.
    """

    settings = copy(defaults_x)
    settings.update(kwargs)

    for filename in os.listdir(data_folder):
        if filename.find("test_X")>=0:
            test_filename = filename
    test_x = load_csv(test_filename, data_folder, **settings)
    return test_x
