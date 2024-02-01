
from main import get_weather, forecast
from sklearn.metrics import mean_squared_error, r2_score
import unittest
from datetime import datetime, timedelta



class Tests(unittest.TestCase):

    def test_Madrid_temperature(self):
        date = "2023-12-23"
        days = 5

        d1 = datetime.strptime(date, "%Y-%m-%d")
        d2 = (d1 - timedelta(days))

        df = get_weather("Madrid", d1.strftime("%Y-%m-%d"), days)
        dftest = forecast("Madrid", d2.strftime("%Y-%m-%d"), days)

        self.assertTrue(r2_score(df["temperature_2m"],dftest["temperature_2m"]) > 0)
    def test_Madrid_humidity(self):
        date = "2023-12-23"
        days = 5

        d1 = datetime.strptime(date, "%Y-%m-%d")
        d2 = (d1 - timedelta(days))

        df = get_weather("Madrid", d1.strftime("%Y-%m-%d"), days)
        dftest = forecast("Madrid", d2.strftime("%Y-%m-%d"), days)

        self.assertTrue(r2_score(df["relative_humidity_2m"],dftest["relative_humidity_2m"]) > 0)
    def test_Amsterdam_temperature(self):
        date = "2023-08-23"
        days = 5

        d1 = datetime.strptime(date, "%Y-%m-%d")
        d2 = (d1 - timedelta(days))

        df = get_weather("Amsterdam", d1.strftime("%Y-%m-%d"), days)
        dftest = forecast("Amsterdam", d2.strftime("%Y-%m-%d"), days)

        self.assertTrue(r2_score(df["temperature_2m"],dftest["temperature_2m"]) > 0)
    def test_Amsterdam_humidity(self):
        date = "2023-08-23"
        days = 5

        d1 = datetime.strptime(date, "%Y-%m-%d")
        d2 = (d1 - timedelta(days))

        df = get_weather("Amsterdam", d1.strftime("%Y-%m-%d"), days)
        dftest = forecast("Amsterdam", d2.strftime("%Y-%m-%d"), days)

        self.assertTrue(r2_score(df["relative_humidity_2m"],dftest["relative_humidity_2m"]) > 0)
    def test_getweather_future(self):
        today = datetime.today()
        future = today + timedelta(10)
        
        try:
            df = get_weather('Kyiv',future.strftime("%Y-%m-%d"))
        except:
            self.assertTrue(True)
    
    def test_getweather_Niamey(self):
        date = "2023-08-23"
        df = get_weather("Niamey", date, 5)
        self.assertTrue(len(df.index) == 6*24)

    def test_getweather_Zinder(self):
        date = "2007-03-01"
        df = get_weather("Zinder",date,99)
        self.assertTrue(len(df.index) == 100*24)



unittest.main()
