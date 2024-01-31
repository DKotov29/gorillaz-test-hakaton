#pip install prophet

from main import get_weather
from prophet import Prophet
import pandas as pd



#values with boundaries
logistic_trend_values = {
        'relative_humidity_2m' : [0, 100]   
}
DAY_ERROR = 5 

def forecast(location, date_start, predict_days):
    
    df = get_weather(location, date_start)
    df = df.dropna()

    result = pd.DataFrame()

    for column in df.columns.to_list()[1:]:
        train_df = pd.DataFrame()
        train_df['ds'] = df['date']
        train_df['y'] = df[column]

        is_logistic = column in logistic_trend_values

        if(is_logistic):
            train_df['floor'] = logistic_trend_values[column][0]
            train_df['cap'] = logistic_trend_values[column][1]

        model = Prophet(growth= "logistic" if is_logistic else "linear")
        model.fit(train_df)

        future = model.make_future_dataframe(periods = 24*(DAY_ERROR + predict_days), freq = 'H')

        if(is_logistic):
            future['floor'] = logistic_trend_values[column][0]
            future['cap'] = logistic_trend_values[column][1]

        forecast = model.predict(future)
        result['date'] = forecast['ds']
        result[column] = forecast['yhat']
                                  
    #todo: return sliced result only with predicted days
    return result





  

