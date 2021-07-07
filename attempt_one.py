import numpy as np
import pandas as pd
import random
import math
import matplotlib.pyplot as plt

def main():
     data = pd.read_csv('all_stocks_5yr.csv')
     tickers = data.Name.unique()
     #print('tickers:', tickers)
     split = split_by_tickers(data, tickers)
     #print(split)
     ticker_index = 0
     means = []
     largest_mean_open_close_diff_label = ''
     largest_mean_open_close_diff = -float('inf')
     largest_high_low = -float('inf')
     high_low_label = ''
     #for s in split:
         #mean = s.mean()
         #diff = mean['close'] - mean['open']
         #high_low = mean['high'] - mean['low']
         #if high_low > largest_high_low:
         #    largest_high_low = high_low
         #    high_low_label = tickers[ticker_index]
         #if diff > largest_mean_open_close_diff:
          #   largest_mean_open_close_diff = diff
           #  largest_mean_open_close_diff_label = tickers[ticker_index]

         #print(mean['high'], 'close - open')
         #means.append(mean)
         #print(tickers[ticker_index], '\n ', mean)
         #ticker_index += 1

     #print('largest high_low: ', largest_high_low, 'label: ', high_low_label)
     #print('largest one day change:', largest_mean_open_close_diff_label, ' :', largest_mean_open_close_diff)
     #constant_set, error_log, min_error, min_constants, min_month
     model, error_log, min_error, min_constants, min_month = build_model(data, 1, 1)
     print('model: ', model)
     print('min average error:', min_error)
     print('min_constants: ', min_constants)
     print('min_month', min_month)

     meanError, predictions, actualList = testModel(min_constants, data, 10, 'close')
     axis = []
     for i in range(len(predictions)):
         axis.append(i)
     print('mean error: ', meanError)
     print('actual: ', actualList)
     print('predictions: ', predictions)
     plt.plot(axis, predictions)
     plt.plot(axis, actualList)
     plt.show()


     #print('error_log: ', error_log)
def approximationFunction(degree, constants, value):
    sum = 0
    for i in range(degree):
        sum += constants[i] * pow(value, i)
    
    return sum

def testModel(model, testData, trail_length, attribute):
    errorSum = 0
    counter = 0
    predictions = []
    actualList = []
    output = testData[attribute]
    print('test data index: ', output.index)
    for data in range(len(output.index) - 4*trail_length):
        vals = []
        for i in range(trail_length):
            #print('index index ', data + i, 'index: ', testData.index[data + i])
            val = output[output.index[data + i] + 1]
            vals.append(val)
            
        prediction = predict(vals, model)
        actual = output[output.index[data + trail_length + 1]]
        error = calcError(prediction, actual)
        errorSum = errorSum + abs(error)
        counter = counter + 1
        predictions.append(prediction)
        actualList.append(actual)
    meanError = errorSum/counter
    return meanError, predictions, actualList

def getClosingPrices(data, month):
    #how to calc error = what do we want to predict via this function
    #data[pd.to_datetime(data['date'], format='%m/%d/%Y', errors='ignore').month == month]
    data['date'] = pd.to_datetime(data['date'])
    subset = data[data['date'].dt.month == month]
    closing = subset['close']
    return closing
    
    #bad model, might have to do this differently
def build_model(data, iterations, steps):
    #what kind of model do i wanna do tho??
    #heres what im thinking, we plot the close prices and try fitting different degree exponential functions to the curve to minimize error
    #first x^0 , then k_0 * 1 + k_1 * x, then k_0 + k_1 * x + k_2 * x_2
    #for i in range(iterations):
        #get function error across data set
    
    constant_set = []#np.random.random_integers(10, size=(1, 1))
    trail_length = 10
    error_log = []
    min_error = float('inf')
    min_constants = []
    min_month = []
    for i in range(iterations):
        #constants.append(random.randint(-3, 3))
        for month in range(1, 12):
            constants = []
            errorSum = 0
            length = 0
            for t in range(trail_length):
                constants.append(random.random())#1
                closing = getClosingPrices(data, month)

            for step in range(steps):
                size = len(closing) - trail_length
                size = size - 5
                start = closing.index[0] + 1
                for i in range(len(closing.index) - trail_length - 2):
                    vals = []
                    length = length + 1
                    for j in range(trail_length):
                        #go from i to i + j
                        #print('i + j: ',  (start + i + j), ' : ', closing)
                        vals.append(closing[closing.index[i + j]])
                    prediction = predict(vals, constants)
                    #print('start + i + length: ', closing.index[i + trail_length])
                    error = calcError(prediction, closing[closing.index[i + trail_length]])
                    errorSum = errorSum + abs(error)
                    #print('error: ', error)
                    for w in range(len(constants)):
                        w_prime = constants[w] + error/(len(constants)*max(abs(constants[w]), 1))
                        constants[w] = w_prime
            
            errorSum = errorSum/length

            if errorSum < min_error:
                min_error = errorSum
                min_constants = constants
                min_month = month
            constant_set.append(constants)   
                
    #print('error_log:', error_log)
    return constant_set, error_log, min_error, min_constants, min_month

def calcError(pred, actual):
    #print('pred: ', pred, ' actual: ', actual)
    error = math.log(abs(pred)) - math.log(abs(actual))
    error = 2*abs(error)
    if pred > actual:
        return -error
    if pred < actual:
        return error

    
def predict(vals, constants):
    prediction = 0
    for i in range(len(vals)):
        prediction += constants[i]*vals[i]
    return prediction

def adjustWeights(w, error):
    constants = []
    #bad function :(
    #print('w: ', w, 'error: ', error)
    for weight in w:
        w_prime = weight + (error/float(weight*weight))
        constants.append(w_prime)
    return constants

def split_by_tickers(data, tickers):
    split = []
    for t in tickers:
        ticker_set = (data['Name'] == t)
        split.append(data[ticker_set])

    return split 


if __name__ == "__main__":
    main()
