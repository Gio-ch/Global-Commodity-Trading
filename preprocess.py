# Description: Adjust the trade_usd column for inflation: to be run once before the app is deployed
import cpi
import pandas as pd
cpi.update()

def inflate_col(data, col='trade_usd'):
    """
    Adjust a column for inflation
    """
    return data.apply(lambda x: cpi.inflate(x[col],
                      x.year), axis=1) 
    
df = pd.read_csv("data/commodity_trade_statistics_data.csv",low_memory=False,)  
df['trade_usd'] = inflate_col(df, col='trade_usd')
df.to_csv("data/commodity_trade_statistics_data_adjusted.csv",index=False)

