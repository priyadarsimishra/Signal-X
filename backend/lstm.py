import yfinance as yf
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import datetime
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.losses import MeanSquaredError, MeanSquaredLogarithmicError
from tensorflow.keras.metrics import MeanAbsoluteError
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from sklearn.metrics import mean_absolute_error

company = "AAPL"

# Define your date range
past = "2004-08-19"
today = datetime.datetime.now().strftime("%Y-%m-%d")

historical_data = yf.download(company, start=past, end=today)

df = pd.DataFrame(historical_data)
df.drop(["High", "Low", "Close"], axis=1, inplace=True)

def str_to_datetime(s):
  split = s.split('-')
  year, month, day = int(split[0]), int(split[1]), int(split[2])
  return datetime.datetime(year=year, month=month, day=day)

# Define your data windowing function
def df_to_windowed_df(dataframe, first_date_str, last_date_str, n=3):
    # Your windowing logic here
    first_date = str_to_datetime(first_date_str)
    last_date  = str_to_datetime(last_date_str)

    target_date = first_date

    dates = []
    X, Y = [], []

    last_time = False
    while True:
        df_subset = dataframe.loc[: target_date].tail(n+1)
        print('subset:', df_subset)

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
    ret_df = pd.DataFrame({})
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

# Modify the target date calculation to ensure that it's within the date range
modified_today = datetime.datetime.now() - datetime.timedelta(days=2)
modified_past = datetime.datetime.strptime(past, "%Y-%m-%d") + datetime.timedelta(days=5)

# Call the df_to_windowed_df function
windowed_df = df_to_windowed_df(df, modified_past.strftime("%Y-%m-%d"), modified_today.strftime("%Y-%m-%d"), n=3)

# Standardize the data
# scaler = StandardScaler()
# windowed_df = scaler.fit_transform(windowed_df)
windowed_df.drop("Target Date", axis=1, inplace=True)
windowed_df.insert(loc=0, column='Volume', value=df["Volume"])
windowed_df.insert(loc=0, column='Adj Close', value=df["Adj Close"])

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
print(x1.shape, y1.shape)
train_part = int(len(x1) * 0.70) # this is trying to get 70/18/12 split
val_part = int(len(x1) * 0.88)
# test_part = len(x1) - val_part - train_part

X_train1, y_train1 = x1[:train_part], y1[:train_part]
X_val1, y_val1 = x1[train_part:val_part], y1[train_part:val_part]
X_test1, y_test1 = x1[val_part:], y1[val_part:]
print(X_train1.shape, y_train1.shape, X_val1.shape, y_val1.shape, X_test1.shape, y_test1.shape)

# Define the modified model
model = Sequential()
model.add(InputLayer((4, 6)))
model.add(Dense(16, 'relu'))
model.add(LSTM(64))
model.add(Dense(32, 'tanh'))
model.add(Dense(1, 'linear'))
model.summary()

# Add learning rate scheduler
# reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.001)
cp1 = ModelCheckpoint('model/', save_best_only=True)
model.compile(loss=MeanSquaredError(), optimizer=Adam(learning_rate=0.0001), metrics=[MeanAbsoluteError()])
model.fit(X_train1, y_train1, validation_data=(X_val1, y_val1), epochs=15, callbacks=[cp1])

model_load = load_model('model/')
train_predictions = model.predict(X_test1).flatten()

train_results = pd.DataFrame(data={'Train Predictions':train_predictions, 'Actuals':y_test1})
plt.plot(train_results['Train Predictions'])
plt.plot(train_results['Actuals'])
plt.show()

# Make predictions
# train_predictions = model.predict(X_test1).flatten()

# Inverse transform the predictions
# train_predictions = scalar.inverse_transform(train_predictions.reshape(-1, 1))

# Calculate MAE
# mae = mean_absolute_error(y_test1, train_predictions)
# print("Mean Absolute Error:", mae)

# Plot the predictions
# plt.plot(train_predictions["Predictions"], label='Predictions')
# plt.plot(y_test1, label='Actuals')
# plt.legend()
# plt.show()