import pandas as pd


def main():
    df=readinfo()

    #Assign day of week
    #df['day-of-week'] = df['date'].dt.day_name()
    df['date'] = pd.to_datetime(df['Date'])
    df['day_of_week'] = df['date'].dt.day_name()

    #filter sunday
    new_df=df.loc[df['day_of_week'] == 'Monday']

    #calculate ROI
    new_df['ROI'] =  ( new_df['Close'].diff() ) / new_df['Close']
    print (new_df)

def readinfo():
    print("Hello World!")
    df = pd.read_csv('/home/amazon/Downloads/BTCUSD.csv')
    #print(df)
    return df


main()