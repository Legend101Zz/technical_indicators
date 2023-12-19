#SMA INDICATORS (2 moving averages)


from backtesting import Backtest, Strategy
import pandas as pd
import numpy as np
import talib




class MyStrategy(Strategy):


    i_ma1 = 200 # Set indicator value here 
    i_ma2 = 10 # Set indicator value here 

    def init(self):
        self.ma1 = self.I(talib.SMA, self.data.Close, self.i_ma1)
        self.ma2 = self.I(talib.SMA, self.data.Close, self.i_ma2)
    def next(self):            
        pass


data = pd.read_csv('CleanData2.csv', parse_dates=True, index_col='Date')

#set data input here taken 1 lac values
data = data.iloc[1:10000]

bt = Backtest(data, MyStrategy)
bt.run()
bt.plot()