
def preprocess(df_in):
    df_out = df_in.copy()

    # "Ratio columns", i.e. features #17-19, are NaN when the denominator is 0;
    # we invert them instead, since the numerator is never 0:
    # a line means that there is at least one event
    ratio_cols = ['OMR', 'OCR', 'OTR']
    inverted_ratio_cols = ['I' + s for s in ratio_cols]
    df_out.drop(ratio_cols, axis = "columns", inplace=True)
    df_out[inverted_ratio_cols] = (1/df_in.loc[:, ratio_cols]).fillna(0)

    return df_out