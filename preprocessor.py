import pandas as pd


def preprocess(df,region):
   # only summer season. 
    df = df[df['Season'] == 'Summer']

    # left join on NOC.
    df = df.merge(region,on ='NOC',how='left')

    # drop duplicates.
    df.drop_duplicates(inplace=True)

    # apply one hot encoding on medal and concatinate it to df.
    df = pd.concat([df,pd.get_dummies(df['Medal'],dtype=int)],axis=1)

    return df
