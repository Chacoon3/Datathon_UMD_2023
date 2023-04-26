import pandas as pd
import regex as re
import numpy as np
from urllib.error import HTTPError

import googlemaps
import time


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


def col_renamer(name:str) -> str:
    name = name.lower()
    name = name.replace(' ', '_')
    name = name.replace('-', '_')
    return name


def get_coordinates(address_list: list | pd.Series | np.ndarray, api_key: str, query_interval: float = 0.02):
    gm_obj = googlemaps.Client(key = api_key)
    res = []
    for ad in address_list:
            time.sleep(query_interval)
            try:
                geocode_result = gm_obj.geocode(ad)
                location = geocode_result[0]['geometry']['location']
                coordinate = (location['lat'], location['lng'])
            except HTTPError:
                print('http error at ' + ad)
                coordinate = (0,0)
            res.append(coordinate)

            if len(res) % 1000 == 0:
                print('geocoding in process... completed ' + str(len(res)))
    return res


def dataframe_filter_by_percentile(df: pd.DataFrame, by: str, percentile: float):    
    if by not in df.columns:
        raise Exception(by +'not found in columns!')
    
    df_res = df.copy(deep=True)
    
    if df_res[by].dtype == object:
        val_freq = df_res[by].value_counts()
        freq_quantile = val_freq.quantile(percentile)
        val_to_keep = val_freq[val_freq >= freq_quantile].index
        df_res = df_res.loc[df_res[by].map(lambda v: v in val_to_keep), :]
    else:
        quantile = df_res[by].quantile(percentile)
        df_res = df_res[df_res[by] >= quantile]

    return df_res