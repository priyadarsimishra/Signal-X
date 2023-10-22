import yfinance as yf
import numpy as np
import pandas as pd

apple = yf.Ticker("AAPL")
print(apple.info)
for key, value in apple.info.items():
    print(key+":", value)

# apple_history = apple.history(start="2023-01-01", end="2023-04-30")
# eps = (net income - preferred dividends) / (avg number of outstanding shares)
# # print(type(apple_history))
# # app = np.array(apple_history)
# # print(app)
# # data = pd.DataFrame(app)
# print(apple.actions)
# print(apple_history.info())

# data = yf.download("AAPL", start="2023-01-01", end="2023-04-30",
#                    group_by="column")

# print(data)
# data = yf.download("AAPL", start="2017-01-01", end="2017-04-30",
#                    group_by="ticker")
# apple = yF.get_data_yahoo("AAPL", start="2023-10-01", end="2023-10-31")
# print(apple.isin)