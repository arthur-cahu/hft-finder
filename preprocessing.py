import pandas as pd


def preprocess_x(df_x):
    """Preprocesses the X data; note that some features get replaced.

    Parameters
    ----------
    df_x : DataFrame
        data from the train_X file

    Returns
    -------
    DataFrame
        Ready to use X table.
    """
    df_out = df_x.copy()

    # "Ratio columns", i.e. features #17-19, are NaN when the denominator is 0;
    # we invert them instead, since the numerator is never 0:
    # a line means that there is at least one event
    ratio_cols = ['OMR', 'OCR', 'OTR']
    inverted_ratio_cols = ['I' + s for s in ratio_cols]
    df_out.drop(ratio_cols, axis="columns", inplace=True)
    df_out[inverted_ratio_cols] = (1 / df_x.loc[:, ratio_cols]).fillna(0)
    df_out.drop(["Share", "Day", "Trader"], axis=1, inplace=True)
    
    # frequencies instead of time differencials
    dt_cols = [s for s in df_out.columns if 'dt' in s]
    df_out.drop(dt_cols, axis="columns", inplace=True)
    freq_cols = [s.replace("dt", "freq") for s in dt_cols]
    df_out[freq_cols] = (1/df_x.loc[:, dt_cols]).fillna(0)

    #df_out.fillna(24 * 3600, inplace=True)
    # since the only NaN values left are time intervals, we set them to a max value of a day
    return df_out

classes = {"NON HFT": 0, "MIX": 1, "HFT":2}

def preprocess_y(df_x, df_y):
    """Preprocesses the y data; note that some features get replaced.

    Parameters
    ----------
    df_x : DataFrame
        data from the train_X file
    df_y : DataFrame
        data from the train_Y file

    Returns
    -------
    Series
        Ready to train y-table; see `preprocessing.classes` for the class mapping.
    """
    # map each trader to its category:
    cat = df_y.set_index("Trader").squeeze()

    s_out = pd.Series(classes[cat[trader]] for trader in df_x["Trader"])
    s_out.set_axis(df_x.index, axis = 0, inplace=True)
    return s_out
