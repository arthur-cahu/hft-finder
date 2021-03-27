
def preprocess(df_x):
    df = df_x.copy()
    # "Ratio columns", i.e. features #17-19, are NaN when the denominator is 0;
    # we invert them instead, since the numerator is never 0
    ratio_cols = ['OMR', 'OCR', 'OTR']
    inverted_ratio_cols = ['I' + s for s in ratio_cols]
    df.drop(ratio_cols)
    df.loc[:, inverted_ratio_cols] = 1/df_x.loc[:, ratio_cols]
    df.loc[:, inverted_ratio_cols].fillna(0, inplace=True)
