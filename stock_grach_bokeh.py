import pandas as pd
import pandas_datareader.data as web

from bokeh.plotting import figure  ,output_notebook , save
from bokeh.layouts import column
from math import pi

from pyti.bollinger_bands import upper_bollinger_band as bb_up
from pyti.bollinger_bands import middle_bollinger_band as bb_mid
from pyti.bollinger_bands import lower_bollinger_band as bb_low

stockdata=web.DataReader("9531.JP", "stooq").dropna()
stockdatarange=stockdata[:'2015-1-1']

inc = stockdatarange.Close > stockdatarange.Open
dec = stockdatarange.Open > stockdatarange.Close
w = 12*60*60*1000 # half day in ms

p = figure(x_axis_type="datetime", plot_width=800, title = "9531 日足")
p.xaxis.major_label_orientation = pi/4
p.grid.grid_line_alpha=0.1

p.segment(stockdatarange.index, stockdatarange.High, stockdatarange.index, stockdatarange.Low, color="black")
p.vbar(stockdatarange.index[inc], w, stockdatarange.Open[inc], stockdatarange.Close[inc], fill_color="snow", line_color="black")
p.vbar(stockdatarange.index[dec], w, stockdatarange.Open[dec], stockdatarange.Close[dec], fill_color="black", line_color="black")
p.line(stockdatarange.index,stockdatarange["Close"].rolling(25, min_periods=1).mean() ,color = 'olive',legend = '25日移動平均')
p.line(stockdatarange.index,bb_up(stockdatarange["Close"],25) ,color = 'orange',legend = 'ボリンジャー')
p.line(stockdatarange.index,bb_low(stockdatarange["Close"],25) ,color = 'orange',legend = 'ボリンジャー')

# 移動平均乖離率のグラフ化
p1 = figure (width = 800 , height = 150,x_axis_type = 'datetime' ,x_range = p.x_range)
df1 = pd.DataFrame((stockdatarange["Close"] - stockdatarange["Close"].rolling(25, min_periods=1).mean()) * 100/stockdatarange["Close"].rolling(25, min_periods=1).mean())
p1.line(stockdatarange.index,df1["Close"],color = 'blue' ,legend = '移動平均乖離率')
p1.line(stockdatarange.index,0,color = 'red',line_width = 2)

# 判例ラベルの位置設定
p.legend.location = 'top_left'
p1.legend.location = 'top_left'

output_notebook()

save(column(p,p1))
