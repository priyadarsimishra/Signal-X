import yfinance as yf
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import datetime
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.losses import MeanSquaredError, MeanSquaredLogarithmicError
from tensorflow.keras.metrics import RootMeanSquaredError, Accuracy
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from sklearn.metrics import accuracy_score

class LSTMModel:
    def get_prediction(self, company):
        date_today = datetime.datetime.now()
        year = date_today.strftime("%Y")
        month = date_today.strftime("%m") 
        day = date_today.strftime("%d")

        past = "2004-08-19"

        today = year+"-"+month+"-"+day
        # yf.pdr_override()
        # data = yf.Ticker("")
        # df = pdr.get_data_yahoo(company, past, today)
        historical_data = yf.download(company, end=today,
                        group_by="column")

        timestamp = ((historical_data.index.values[0] - np.datetime64('1970-01-01T00:00:00'))
                        / np.timedelta64(1, 's'))
        date_past = datetime.datetime.utcfromtimestamp(timestamp)

        year = date_past.strftime("%Y")
        month = date_past.strftime("%m")
        day = date_past.strftime("%d")

        past = year+"-"+month+"-"+day
        # print("PAST:", past)

        # print(df)
        # historical_data = historical_data['Date'].apply(str_to_datetime)
        # print(historical_data.index.values)
        # historical_data['Date'] = historical_data.index.values
        df = pd.DataFrame(historical_data)
        # df.drop("Open", axis=1, inplace=True)
        df.drop("High", axis=1, inplace=True)
        df.drop("Low", axis=1, inplace=True)
        # df.drop("Adj Close", axis=1, inplace=True)
        df.drop("Close", axis=1, inplace=True)
        # df.drop("Volume", axis=1, inplace=True)

        # print(df.index.values)

        # df = df[::-1]
        # print("part:", df.head(7))
        # print("shape:", df.shape)
        # print("-------------")

        def str_to_datetime(s):
            split = s.split('-')
            year, month, day = int(split[0]), int(split[1]), int(split[2])
            return datetime.datetime(year=year, month=month, day=day)

        def df_to_windowed_df(dataframe, first_date_str, last_date_str, n=3):
            first_date = str_to_datetime(first_date_str)
            last_date  = str_to_datetime(last_date_str)

            target_date = first_date

            dates = []
            X, Y = [], []

            last_time = False
            while True:
                df_subset = dataframe.loc[: target_date].tail(n+1)
                # print('subset:', df_subset)

                if len(df_subset) != n+1:
                    print(f'Error: Window of size {n} is too large for date {target_date}')
                    return

                close = df_subset['Adj Close'].to_numpy()
                volume = df_subset['Volume'].to_numpy()
                x, y = close[:-1], close[-1]

                dates.append(target_date)
                X.append(x)
                Y.append(y)

                next_week = dataframe.loc[target_date:target_date+datetime.timedelta(days=7)]
                next_datetime_str = str(next_week.head(2).tail(1).index.values[0])
                next_date_str = next_datetime_str.split('T')[0]
                year_month_day = next_date_str.split('-')
                year, month, day = year_month_day
                next_date = datetime.datetime(day=int(day), month=int(month), year=int(year))

                if last_time:
                    break

                target_date = next_date

                if target_date == last_date:
                    last_time = True

            #   dataframe.drop("Close", axis=1, inplace=True)
            ret_df = dataframe[3:]
            ret_df.insert(loc=0, column='Target Date', value=dates)
            # ret_df.drop("Adj Close", axis=1, inplace=True)
            #   ret_df['Volume'] = dataframe[3:]

            print("X:", ret_df.shape)

            X = np.array(X)
            for i in range(0, n):
                X[:, i]
                ret_df[f'Target-{n-i}'] = X[:, i]

            ret_df['Target'] = Y
            return ret_df

        modified_today = datetime.datetime.now()
        modified_today -= datetime.timedelta(days=2) # TODO: tomorrow before DEMO change to -= 1 for days cause days change
        modified_past = str_to_datetime(past)
        modified_past += datetime.timedelta(days=5)

        year = modified_today.strftime("%Y")
        month = modified_today.strftime("%m")
        day = modified_today.strftime("%d")
        modified_today = year+"-"+month+"-"+day

        year = modified_past.strftime("%Y")
        month = modified_past.strftime("%m")
        day = modified_past.strftime("%d")
        modified_past = year+"-"+month+"-"+day
        # print)


        windowed_df = df_to_windowed_df(df, 
                                        modified_past, 
                                        modified_today, 
                                        n=3)

        windowed_df.drop("Target Date", axis=1, inplace=True)
        # print(windowed_df)

        scalar = StandardScaler()
        scalar = scalar.fit(windowed_df)
        windowed_df = scalar.transform(windowed_df)

        def df_to_X_y(df, window_size=4):
            df_as_np = df
            X = []
            y = []
            for i in range(len(df_as_np)-window_size):
                row = [r for r in df_as_np[i:i+window_size]]
                X.append(row)
                label = df_as_np[i+window_size][0]
                y.append(label)
            return np.array(X), np.array(y)

        WINDOW_SIZE = 4
        x1, y1 = df_to_X_y(windowed_df, WINDOW_SIZE)
        # print(x1.shape, y1.shape)
        train_part = int(len(x1) * 0.70) # this is trying to get 70/18/12 split
        val_part = int(len(x1) * 0.88)
        # test_part = len(x1) - val_part - train_part

        X_train1, y_train1 = x1[:train_part], y1[:train_part]
        X_val1, y_val1 = x1[train_part:val_part], y1[train_part:val_part]
        X_test1, y_test1 = x1[val_part:], y1[val_part:]
        # print(X_train1.shape, y_train1.shape, X_val1.shape, y_val1.shape, X_test1.shape, y_test1.shape)

        model = Sequential()
        model.add(InputLayer((4, 7)))
        model.add(Dense(16, 'relu'))
        model.add(LSTM(64))
        model.add(Dense(32, 'tanh'))
        model.add(Dense(1, 'linear'))

        model.summary()

        cp1 = ModelCheckpoint('model/', save_best_only=True)
        model.compile(loss=MeanSquaredError(), optimizer=Adam(learning_rate=0.0001), metrics=[RootMeanSquaredError()])
        model.fit(X_train1, y_train1, validation_data=(X_val1, y_val1), epochs=8, callbacks=[cp1])

        model_load = load_model('model/')
        train_predictions = model.predict(X_test1).flatten()

        train_results = pd.DataFrame(data={'Train Predictions':train_predictions, 'Actuals':y_test1})
        return [train_predictions[-3:], y_test1[-3:]]
        # plt.plot(train_results['Train Predictions'])
        # plt.plot(train_results['Actuals'])
        # plt.show()