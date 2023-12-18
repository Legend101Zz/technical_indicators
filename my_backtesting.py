from backtesting import Backtest, Strategy
# from backtesting.lib import SMA
import talib
import pandas as pd
import numpy as np



def optim_func(series):
   if series["# Trades"] <50:
      return -1
   return series["Return [%]"]


class MyStrategy(Strategy):

     
    i_ma1 = 200
    i_ma2 = 10
    i_stopPercent = 0.10
    i_lowerClose = False
    prevBuyPrice = None
    # i_startTime = pd.to_datetime("01 Jan 1995 09:00 +0000").time()
    # i_endTime = pd.to_datetime("1 Jan 2099 15:30 +0000").time()

        
    buyPrice = 0



    def init(self):
  
        self.ma1 = self.I(talib.SMA, self.data.Close, self.i_ma1)
        self.ma2 = self.I(talib.SMA, self.data.Close, self.i_ma2)

    def next(self):
       
        # f_dateFilter = (
        #     (self.data.index.time >= self.i_startTime) &
        #     (self.data.index.time <= self.i_endTime)
        # )

    
        buyCondition = (crossover(self.ma1, self.ma2) and (self.position.size == 0)) 
        sellCondition = (crossover(self.ma2, self.ma1) and (self.position.size > 0) and
                        ((not self.i_lowerClose) or (self.data['Close'] < self.data['Low'].shift(1))))

        stopDistance = (
            ((self.prevBuyPrice - self.data.Close) / self.data.Close[-1])
            if self.position.size > 0 and self.prevBuyPrice is not None
            else None
        )

        stopPrice = (
            (self.prevBuyPrice - (self.prevBuyPrice * self.i_stopPercent))
            if self.position.size > 0
            else None
        )

        stopCondition = (
            (self.position.size > 0) and
            (stopDistance is not None) and
            (np.nan_to_num(stopDistance) > self.i_stopPercent)
        )

        
        if buyCondition:

            self.buyPrice = self.data.Open[-1]

  
            self.prevBuyPrice = self.buyPrice

            self.buy()

        
           

      
        if sellCondition or stopCondition:
            self.sell()


data = pd.read_csv('CleanData2.csv', parse_dates=True, index_col='Date')

data = data.iloc[1:100000]

bt = Backtest(data, MyStrategy, cash=10000000, commission=0.005)
stats,heatmap = bt.optimize(
    i_ma1 =range(170,220,5),
    i_ma2 = range(5,25,5),
    maximize = optim_func,
    return_heatmap =True
)



bt.plot()


print(stats)