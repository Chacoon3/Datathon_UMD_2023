import pandas as pd


def join_geo_info(df_main : pd.DataFrame, df_rev_geo : pd.DataFrame) ->pd.DataFrame:
    df_res = df_main.copy(deep=True)
    df_rev = df_rev_geo.copy(deep=True)

    df_res['coordinate'] = df_res.index.map(
        lambda i: str((df_res['LATITUDE'][i], df_res['LONGITUDE'][i]))
    )

    df_rev['coordinate'] = df_rev['coordinate'].map(lambda v: str(v))

    df_res = pd.merge(df_res, df_rev, on = 'coordinate')
    return df_res