# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 22:34:52 2018

The following is an elementary manual implementation of a classifier
using only a single neuron and gradient descent optimization. 
The code hass been based on tutorials by giant_neural_network 
on youtube, and further modified so it speaks along the process, reports some stats, 
outputs more visualizations and also has more comments. 
The original data was also extended to a 100 "random" observations such that 
a classification line is clear enough. 

@author: Hair Parra
@Copyright: Attribution-NonCommercial-NoDerivatives 4.0 International
            https://creativecommons.org/licenses/by-nc-nd/4.0/

"""

##THIS FUCKING MAKES THE COMPUTER SPEAK LMFAO
from win32com.client import Dispatch
speak = Dispatch("SAPI.SpVoice")

from matplotlib import pyplot as plt 
import numpy as np
import pandas as pd
from pandas import DataFrame
import random

speak.speak("Welcome to the classification program")
print("Welcome to the classification program")

speak.speak("Preprocessing data")
print("Preprocessing data...")

# Please chage PATH to where you have downloaded the dataset
flower_table = pd.read_excel(r'C:\Users\jairp\Desktop\BackUP\AI and Machine Learning\Flower_Table.xlsx')
flowersdf = DataFrame(flower_table,columns = ['length','width','color'])
print(flowersdf, "\n")


flowers = [] # List of flowers: each entry has the format [color,length,width]

# transform the dataframe into a list 
for index, row in flowersdf.iterrows(): 
    flowers.append([row["length"],row["width"],row["color"]]) # Here needed to append the new sublist

mystery_flower = np.array(flowers[8:9]).tolist()
mystery_flower = mystery_flower[0][:]
del flowers[8:9]
print('Printing flowers\n',flowers)
print('\nMystery flower: ', mystery_flower)
print()

#   we can assign random values to the weights at the beginning
w1 = np.random.randn() 
w2 = np.random.randn()
b = np.random.randn()

# sigmoid function (activation function)
def sigmoid(x): 
    return 1 / (1 + np.exp(-x))

# derivative of sigmoid
def dsigmoid_dx(x): 
    return sigmoid(x)* (1-sigmoid(x))


## Basic graph plot
#X = np.linspace(-20,20,100) # domain
#Y = sigmoid(X) # results
#plt.plot(X,Y) 
    


plt.figure(1)
# Graph both the sigmoid and derivative
X = np.linspace(-6,6,100) # domain 
plt.plot(X,sigmoid(X), c='r') # (axis,Y)
plt.plot(X,dsigmoid_dx(X), c='b') # (axis,Y)
plt.title('Sigmoid function')
plt.ylabel('Y')
plt.xlabel('Values')


# scatter data
plt.figure(2)
plt.axis([0,6,0,3])
plt.grid()
plt.title('Flowers data')
plt.xlabel('Width')
plt.ylabel('Length')
for i in range(len(flowers)): 
    point = flowers[i]
    color = "r"
    if point[2] == 0:
        color = "b"
    plt.scatter(point[0],point[1], c=color)
    
# More advanced function
def vis_data(data):
    
    plt.grid()

    for i in range(len(data)):
        c = 'r'
        if data[i][2] == 0:
            c = 'b'
        plt.scatter([data[i][0]], [data[i][1]], c=c)

    plt.scatter([mystery_flower[0]], [mystery_flower[1]], c='gray')



# Training loop 
    
learning_rate = .2 # learning rate
costs = []
iterations = 100000

speak.speak("Learning rate has been set to {} percent".format(learning_rate*100))
print("Learning rate = {}%".format(str(learning_rate*100)))


speak.speak("Running {} iterations of the algorithm".format(iterations))
print("Running {} iterations of the algorithm".format(iterations))
    
# train

def train(iterations = 10000, learning_rate = 0.1):
    #random init of weights
    w1 = np.random.randn()
    w2 = np.random.randn()
    b = np.random.randn()
    
    costs = [] # keep costs during training, see if they go down
    
    for i in range(iterations):
        # get a random point
        ri = np.random.randint(len(flowers))
        point = flowers[ri]
        
        z = point[0] * w1 + point[1] * w2 + b
        pred = sigmoid(z) # networks prediction
        
        target = point[2] # get the target 
        
        # cost for current random point
        cost = np.square(pred - target)
        
        # print the cost over all data points every 1k iters
        if i % 100 == 0:
            c = 0
            for j in range(len(flowers)):
                p = flowers[j]
                p_pred = sigmoid(w1 * p[0] + w2 * p[1] + b)
                c += np.square(p_pred - p[2])
            costs.append(c)
        
        dcost_dpred = 2 * (pred - target)
        dpred_dz = dsigmoid_dx(z)
        
        dz_dw1 = point[0]
        dz_dw2 = point[1]
        dz_db = 1
        
        dcost_dz = dcost_dpred * dpred_dz
        
        dcost_dw1 = dcost_dz * dz_dw1
        dcost_dw2 = dcost_dz * dz_dw2
        dcost_db = dcost_dz * dz_db
        
        w1 = w1 - learning_rate * dcost_dw1
        w2 = w2 - learning_rate * dcost_dw2
        b = b - learning_rate * dcost_db
        
        final_cost = cost
        
        completed = round((i*100)/iterations, 2)
        print("{}% completed".format(completed))
        
    return costs, w1, w2, b, final_cost

costs, w1, w2, b, final_cost = train(50000,learning_rate)

speak.speak("Iterations finished")
print("Iterations finished")

accuracy = round(100*(1 - final_cost),2)
print("Model accuracy: {}%".format(accuracy))
speak.speak("The model fits the data with {}% accuracy".format(accuracy))

plt.figure(3)
plt.plot(costs)
plt.title('Gradient descend')
plt.xlabel('Iterations')
plt.ylabel('Error')

# seeing model predictions 

for i in range(len(flowers)): 
    point = flowers[i]
    print(point)
    z = point[0]*w1 + point[1]*w2 + b
    pred = sigmoid(z) # activation function
    print("pred: {}".format(pred))
    

# Now let's make the computer speak again
def which_flower(length, width): 
    
    print("(Length,width) = (" + str(length) + "," + str(width) + ")")
    z = length*w1 + width*w2 + b
    pred = sigmoid(z)
    if pred < .5: 
        print("Kind of flower: blue")
        speak.Speak("I think it's a blue flower!")
        return "blue"
    else: 
        print("Kind of flower: red")
        speak.Speak("I think it's a red flower!")
        return "red"
    
# checking the random flower
    
speak.speak("Testing a specific new flower")
print("Testing a specific new flower")
z = mystery_flower[0]*w1 + mystery_flower[1]*w2 + b
pred = sigmoid(z) # activation function

which_flower(mystery_flower[0],mystery_flower[1])
speak.speak("Testing for five randomly measured flowers")
print("Testing...")
    
for i in range(5): 
    print("Iteration:" + str(i))
    rand_length = random.randint(1,4)
    rand_width = random.randint(1,4)
    which_flower(rand_length,rand_width)
# test 
# predict some random flower

# check out the networks predictions in the x,y plane
plt.figure(4)
for x in np.linspace(0, 8, 20):
    for y in np.linspace(0, 3, 20):
        pred = sigmoid(w1 * x + w2 * y + b)
        c = 'b'
        if pred > .5:
            c = 'r'
        plt.scatter([x],[y],c=c, alpha=.2)
        
# plot points over network predictions
# you should see a split, with half the predictions blue
# and the other half red.. nicely predicting each data point!

vis_data(flowers)

speak.speak("Outputting visualizations")
speak.speak("End of the program")

print("\nResults:\n")

print("Number of data = {}".format(len(flowers)))
print("# Iterations = {}".format(iterations))
print("Learning rate = {}".format(learning_rate))
print("Accuracy = {}%".format(accuracy))


"""
Created on Fri Dec 21 22:34:52 2018

The following is an elementary manual implementation of a classifier
using only a single neuron and gradient descent optimization. 
The code hass been based on tutorials by giant_neural_network 
on youtube, and further modified so it speaks along the process, reports some stats, 
outputs more visualizations and also has more comments. 
The original data was also extended to a 100 "random" observations such that 
a classification line is clear enough. 

@author: Hair Parra
@Copyright: Attribution-NonCommercial-NoDerivatives 4.0 International
            https://creativecommons.org/licenses/by-nc-nd/4.0/

"""

