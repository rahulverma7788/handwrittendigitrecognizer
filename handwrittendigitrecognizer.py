# -*- coding: utf-8 -*-
"""handwrittendigitrecognizer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1f_7VEoie9RI_unFk-8idrOyvpxvX7xFD
"""

# Commented out IPython magic to ensure Python compatibility.
import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline

plt.rcParams["figure.figsize"] = 10,7
warnings.filterwarnings('ignore') 
np.random.seed(0)

test = pd.read_csv('test1.csv')
train = pd.read_csv('train1.csv')

train.head()

test.head()

range_class = np.arange(10)
y = np.asfarray(train.iloc[:,0])
train_x = train.iloc[:,1:].values
train_y = np.array([(range_class==label).astype(np.int) for label in y])
print(train_y)

test_x = test.values
print(test)

y = train.iloc[:,0].value_counts()
x = range(len(y))
plt.bar(x, y, color='rgbymc')
plt.xticks(x, x)
plt.ylabel('no. of images w.r.t labels')
plt.xlabel('Lables between 0-9')
plt.grid()

figure = plt.figure()


figure.set_size_inches(20.5, 8.5)

for itr in range(1, 10):
    plt.subplot(1, 10, itr)
    label = train.loc[itr,'label']
    pixels = train.iloc[itr,1:].values.reshape((28,28))
    plt.title('Label is {label}'.format(label=label))
    plt.imshow(pixels)

plt.show()

train_x = train_x / 255.
test_x  = test_x  / 255.

shape_x = train_x.shape
shape_y = train_y.shape
m = train_y.shape[0]
print('the shape of X is' + str(shape_x))
print('the shape of Y is' + str(shape_y))
print('I have m = %d training examples!' % (m))

def layer_size(X, Y):
  n_x = X.shape[1]
  n_h = 4
  n_y = Y.shape[1]
  return (n_x, n_h, n_y)

def initialise_parameter(n_x, n_h, n_y):
    
    np.random.seed(0)
    
    W1 = np.random.randn(n_h[0], n_x) * 0.1
    b1 = np.zeros(shape=(n_h[0], 1))
    
    W2 = np.random.randn(n_h[1], n_h[0]) * 0.1
    b2 = np.zeros(shape=(n_h[1], 1))
    
    W3 = np.random.randn(n_y, n_h[1]) * 0.1
    b3 = np.zeros(shape=(n_y, 1))
    
    assert(W1.shape == (n_h[0], n_x))
    assert(b1.shape == (n_h[0], 1))

    assert(W2.shape == (n_h[1], n_h[0]))
    assert(b2.shape == (n_h[1], 1))
    
    assert(W3.shape == (n_y, n_h[1]))
    assert(b3.shape == (n_y, 1))
    
    parameters = {"W1": W1, 
                  "b1": b1, 
                  "W2": W2, 
                  "b2": b2, 
                  "W3": W3, 
                  "b3": b3
                 }
    
    return parameters

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

_x = np.linspace(-5, 5, 40)

plt.plot(sigmoid(_x))
plt.plot(sigmoid_derivative(sigmoid(_x)))

plt.grid()

def forward_propagation(X, parameters):
    
    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]
    W3 = parameters["W3"]
    b3 = parameters["b3"]
    
    Z1 = (np.dot(W1, X.T) + b1).T
    A1 = sigmoid(Z1)
    Z2 = (np.dot(W2, A1.T) + b2).T
    A2 = sigmoid(Z2)
    Z3 = (np.dot(W3, A2.T) + b3).T
    A3 = sigmoid(Z3)
    
    assert(A3.shape == (X.shape[0], 10))
    
    cache = {
        "Z1" : Z1,
        "A1" : A1,
        "Z2" : Z2,
        "A2" : A2,
        "Z3" : Z3,
        "A3" : A3
    }

    return A3, cache

def compute_cost(A3, Y):
    
    m = Y.shape[0] 
    
    logprobs = np.multiply(Y, np.log(A3)) + np.multiply((1 - Y), np.log(1 - A3))
    cost = - np.sum(logprobs) / m
    
    cost = float(np.squeeze(cost))
    
    assert(isinstance(cost, float))
    
    return cost

def backward_propagation(parameters, cache, X, Y):
    
    m = Y.shape[0]
    
    A1 = cache["A1"]
    A2 = cache["A2"]
    A3 = cache["A3"]
    
    W1 = parameters["W1"]
    W2 = parameters["W2"]
    W3 = parameters["W3"]
    
    dZ3 = (A3 - Y)
    dW3 = (1 / m) * np.dot(dZ3.T, A2)
    db3 = (1 / m) * np.sum(dZ3, keepdims=True)

    dZ2 = np.multiply(np.dot(dZ3, W3), sigmoid_derivative(A2))
    dW2 = (1 / m) * np.dot(dZ2.T, A1)
    db2 = (1 / m) * np.sum(dZ2, keepdims=True)
    
    dZ1 = np.multiply(np.dot(dZ2, W2), sigmoid_derivative(A1))
    dW1 = (1 / m) * np.dot(dZ1.T, X)
    db1 = (1 / m) * np.sum(dZ1, keepdims=True)
    
    grads = {"dW1": dW1, 
             "db1": db1, 
             "dW2": dW2, 
             "db2": db2, 
             "dW3": dW3, 
             "db3": db3
            }
    
    return grads

def update_parameters(parameters, grads, learning_rate):
    
    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]
    W3 = parameters["W3"]
    b3 = parameters["b3"]
    
    dW1 = grads["dW1"]
    db1 = grads["db1"]
    dW2 = grads["dW2"]
    db2 = grads["db2"]
    dW3 = grads["dW3"]
    db3 = grads["db3"]
    
    W1 = W1 - (learning_rate * dW1)
    b1 = b1 - (learning_rate * db1)
    W2 = W2 - (learning_rate * dW2)
    b2 = b2 - (learning_rate * db2)
    W3 = W3 - (learning_rate * dW3)
    b3 = b3 - (learning_rate * db3)
    
    parameters = {"W1": W1, 
                  "b1": b1, 
                  "W2": W2, 
                  "b2": b2, 
                  "W3": W3, 
                  "b3": b3
                 }
    
    return parameters

def predict(X, parameters):
    
    m = X.shape[0]
    
    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]
    
    A3, cache = forward_propagation(X, parameters)
    
    return A3

def nn_model(X, Y, n_h, learning_rate, num_iterations, print_cost=False):

    np.random.seed(3)

    cost_per_iter = []
    
    n_x = layer_size(X, Y)[0]
    n_y = layer_size(X, Y)[2]
    
    # Initialize parameters
    parameters = initialise_parameter(n_x, n_h, n_y)
    
    # Loop (gradient descent)
    for i in range(0, num_iterations):

        # Forward propagation. Inputs: "X, parameters". Outputs: "A2, cache".
        A3, cache = forward_propagation(X, parameters)
        
        # Cost function. Inputs: "A2, Y, parameters". Outputs: "cost".
        cost = compute_cost(A3, Y)
 
        cost_per_iter.append(cost)

        # Backpropagation. Inputs: "parameters, cache, X, Y". Outputs: "grads".
        grads = backward_propagation(parameters, cache, X, Y)
 
        # Gradient descent parameter update. Inputs: "parameters, grads". Outputs: "parameters".
        parameters = update_parameters(parameters, grads, learning_rate)
        
        # Print the cost every 1000 iterations
        if print_cost and i % 100 == 0:
            print ("Cost after iteration %i: %f" %(i, cost))
    
    train_prediction = (train.iloc[:,0].values != np.array(predict(train_x, parameters).argmax(axis=1)).T).astype(int)

    test_prediction = np.vstack((np.arange(1, 21832), predict(test_x, parameters).argmax(axis=1).T)).T
    data_to_submit = pd.DataFrame(test_prediction, columns = ['ImageId','Label']) 
    
    print("train accuracy: {} %".format(100 - np.mean(train_prediction) * 100))
    
    output = {
        "cost" : cost_per_iter[-1],
        "parameters" : parameters,
        "cost_per_iter" : cost_per_iter,
        "train_prediction" : train_prediction,
        "test_prediction" : test_prediction,
        "data_to_submit" : data_to_submit
    }
    
    return output

models = {}
learning_rates = [2.1]

for i in learning_rates:
    print ("learning rate is: " + str(i))
    models[str(i)] = nn_model(train_x, train_y, n_h = [400, 40], learning_rate = i, num_iterations = 1500, print_cost=False)
    print ("Cost is: " + str(models[str(i)]["cost"]))
    print ("-------------------------------------------------------" + '\n')

for i in learning_rates:
    plt.plot(np.squeeze(models[str(i)]["cost_per_iter"]), label= str(i))

plt.ylabel('cost')
plt.xlabel('iterations')
legend = plt.legend(loc='upper center', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.grid()
plt.show()

