import os
import math
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Flatten
from keras.layers.convolutional import Conv1D, MaxPooling1D
import matplotlib.pyplot as plt

### 날짜 입력받아서 기사 출력하기 테스트
# from TestGetNews import simpleScore
# simpleScore("2022-01-15")
### 동작 확인 완료

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

### 주식 history data 읽어오기
stock_df = pd.read_csv('./003490.KS.csv')
### Sample history data 뽑기 (22-01-10 ~ 22-02-10)
sample_df = stock_df.loc[2648:2791,:]

### 날짜 data 뽑기
date_df = stock_df.filter(['Date'])
### Sample 날짜 data 뽑기 (22=01-10 ~ 22-02-10)
sample_date_df = sample_df.filter(['Date'])

## Sample에 대해 수행중 (stock_df -> sample_df)
### 종가 data만 뽑기
close_df = sample_df.filter(['Close'])
### Data frame을 numpy array로 전환하기
close_data = close_df.values

### Data scaling
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(close_data)

seq = 60

### Train set, Test set 생성하기
train_data_len = math.ceil(len(stock_df) * 0.7)
train_data = scaled_data[0:train_data_len, :]
test_data = scaled_data[train_data_len-seq:, :]

## Training data 생성
### Data를 x_train과 y_train으로 나누기
x_train = []
y_train = []

for i in range(seq, len(train_data)):
    x_train.append(train_data[i-seq:i, 0])  # index: 0 ~ (seq -1)
    y_train.append(train_data[i, 0])    # index: seq

### x_train, y_train을 numpy array로 수정
x_train, y_train = np.array(x_train), np.array(y_train)

### LSTM 학습을 위해서 data를 2D->3D로 수정
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

## Test data 생성
x_test = []
y_test = close_data[train_data_len:, :]

for i in range(seq, len(test_data)):
    x_test.append(test_data[i-seq:i, 0])

### x_test를 numpy array로 수정
x_test = np.array(x_test)

### LSTM 테스트를 위해서 data를 2D->3D로 수정
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

'''
LSTM 모델 생성
'''

lstmModel = Sequential()
lstmModel.add(LSTM(64, return_sequences=True, input_shape=(x_train.shape[1],1)))
lstmModel.add(LSTM(64, return_sequences=False))
lstmModel.add(Flatten())
lstmModel.add(Dense(25))
lstmModel.add(Dense(1, activation='sigmoid'))

### LSTM 모델 컴파일
lstmModel.compile(optimizer='adam', loss='mean_squared_error')

### 모델 training
lstmModel.fit(x_train, y_train, batch_size=1, epochs=1)

### LSTM 모델 예측
lstmPredictions = lstmModel.predict(x_test)
lstmPredictions = scaler.inverse_transform(lstmPredictions) # Unscale the value

### LSTM 모델 평가
lstmRmse = np.sqrt(np.mean(lstmPredictions - y_test)**2)
print("LSTM RMSE: ", lstmRmse)

### Plot data
train = close_df[:train_data_len]
valid = close_df[train_data_len:]

### LSTM 예측
valid['Predictions'] = lstmPredictions

### LSTM 시각화
plt.figure(figsize=(16,9))
plt.title('LSTM Model')
plt.xlabel("Date", fontsize=18)
plt.ylabel("Price", fontsize=18)
plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])
plt.legend(['Train','Val','Predictions'], loc='lower right')
plt.show()


'''
CNN 모델 생성
'''

cnnModel = Sequential()
cnnModel.add(Conv1D(filters=128, kernel_size=4, activation='relu', input_shape=(x_train.shape[1],1)))
cnnModel.add(Conv1D(filters=64, kernel_size=4, activation='relu'))
cnnModel.add(Flatten())
cnnModel.add(Dense(25, activation='relu'))
cnnModel.add(Dense(1, activation='sigmoid'))

### CNN 모델 컴파일
cnnModel.compile(optimizer='adam', loss='mean_squared_error')

### 모델 training
cnnModel.fit(x_train, y_train, batch_size=1, epochs=1)

### CNN 모델 예측
cnnPredictions = cnnModel.predict(x_test)
cnnPredictions = scaler.inverse_transform(cnnPredictions) # Unscale the value

### CNN 모델 평가
cnnRmse = np.sqrt(np.mean(cnnPredictions - y_test)**2)
print("CNN RMSE: ", cnnRmse)

### Plot data
train = close_df[:train_data_len]
valid = close_df[train_data_len:]

### CNN 예측
valid['Predictions'] = cnnPredictions

### CNN 시각화
plt.figure(figsize=(16,9))
plt.title('CNN Model')
plt.xlabel("Date", fontsize=18)
plt.ylabel("Price", fontsize=18)
plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])
plt.legend(['Train','Val','Predictions'], loc='lower right')
plt.show()


