import pandas as pd
def preprocess(df_in):
    """Preprocesses the data; note that some features get replaced.

    Parameters
    ----------
    df_in : DataFrame

    Returns
    -------
    DataFrame
    """
    df_out = df_in.copy()

    # "Ratio columns", i.e. features #17-19, are NaN when the denominator is 0;
    # we invert them instead, since the numerator is never 0:
    # a line means that there is at least one event
    ratio_cols = ['OMR', 'OCR', 'OTR']
    inverted_ratio_cols = ['I' + s for s in ratio_cols]
    df_out.drop(ratio_cols, axis = "columns", inplace=True)
    df_out[inverted_ratio_cols] = (1/df_in.loc[:, ratio_cols]).fillna(0)
    df_out.drop(["Share","Day","Trader"],axis=1,inplace=True)
    df_out.fillna(24*3600,inplace=True)
    return df_out




def preprocess_y(df_x,df_in):
    """Preprocesses the data; note that some features get replaced.

    Parameters
    ----------
    df_x  : DataFrame X containing the list of traders
    df_in : DataFrame of answers

    Returns
    -------
    DataFrame
    """
    df_out = pd.DataFrame()
    df_out["Trader"] = df_x["Trader"]
    tab = []
    for t in df_out["Trader"].values:
        for j,a in enumerate(df_in["Trader"]):
            if a==t:
                tab.append(df_in.iloc[j]["type"])
    df_out["HFT"] = tab
    df_out.drop("Trader", axis =1,inplace=True)

    return df_out