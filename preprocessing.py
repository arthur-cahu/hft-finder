import pandas as pd


def preprocess(df_x):
    """Preprocesses the data; note that some features get replaced.

    Parameters
    ----------
    df_x : DataFrame
        data from the train_X file

    Returns
    -------
    DataFrame
        Ready to train X table.
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
    df_out.fillna(24 * 3600, inplace=True)
    # since the only NaN values left are time intervals, we set them to a max value of a day
    return df_out


def preprocess_y(df_x, df_y):
    """Preprocesses the data; note that some features get replaced.

    Parameters
    ----------
    df_x : DataFrame
        data from the train_X file
    df_y : DataFrame
        data from the train_Y file

    Returns
    -------
    Series
        Corresponding `⟨HFT│MIX│Non−HFT⟩` y-value for each line of X.
    """
    # map each trader to its category:
    cat = df_y.set_index("Trader").squeeze()

    s_out = pd.Series(cat[trader] for trader in df_x["Trader"])
    return s_out
