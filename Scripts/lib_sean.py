import pandas as pd


def clean_data(df_main: pd.DataFrame, df_rev_geo: pd.DataFrame) ->pd.DataFrame:
    df = df_main.copy(deep = True)

    df = __clean_columns(df)
    df = __join_geo_info(df, df_rev_geo)
    df = __drop_rows(df)

    return df



def __join_geo_info(df_main : pd.DataFrame, df_rev_geo : pd.DataFrame) ->pd.DataFrame:
    df_res = df_main.copy(deep=True)
    df_rev = df_rev_geo.copy(deep=True)

    df_res['coordinate'] = df_res.index.map(
        lambda i: str((df_res['LATITUDE'][i], df_res['LONGITUDE'][i]))
    )

    df_rev['coordinate'] = df_rev['coordinate'].map(lambda v: str(v))

    df_res = pd.merge(df_res, df_rev, on = 'coordinate')
    return df_res


def __clean_columns(df_main: pd.DataFrame) ->pd.DataFrame:
    
    df = df_main.copy(deep=True)

    df.CONSTRUCTION_YEAR.fillna(df.CONSTRUCTION_YEAR.median(), inplace=True)
    df.REVIEWS_PER_MONTH.fillna(round(df.REVIEWS_PER_MONTH.mean(), 2), inplace=True)
    df.NUMBER_OF_REVIEWS .fillna(int(df.NUMBER_OF_REVIEWS.mean()), inplace=True)


    df.LAST_REVIEW = pd.to_datetime(df.LAST_REVIEW)
    df.LAST_REVIEW = (df.LAST_REVIEW - pd.Timestamp('1970-01-01')) / pd.Timedelta('1D')
    median_date = df.LAST_REVIEW.median()
    df.LAST_REVIEW.fillna(median_date, inplace=True)
    df.LAST_REVIEW = pd.to_datetime(df.LAST_REVIEW, unit='D')
    
    return(df)


def __drop_rows(df_main: pd.DataFrame) ->pd.DataFrame:
    df = df_main.copy(deep=True)

    df.dropna(axis=0, subset = 'NEIGHBORHOOD', how='any', inplace=True)
    return df