# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 21:53:24 2018

@author: guglielmo
"""

import numpy as np

debug = lambda x: print(*x)

np.set_printoptions(threshold=np.NaN)

np.random.seed(158566)
 
n_features = 3
n_class = 2

class_prob = np.ones(n_class)/n_class
feature_prob = np.ones((n_features, n_class)) #prob of true news
correct_pred = np.ones(n_features)

theoretical_prob = np.random.random(n_features)

n_data = 10
train_data = np.zeros((n_data,n_features))
mask = np.random.random((n_data,n_features)) < theoretical_prob
train_data[mask] = 1
train_target = np.ones(n_data)

#for i in range(n_data):
#    if np.random.random() > 0.01:
#        train_data[i][0] = 1-train_target[i]
#print(sum(train_data[:,0]==train_target))

#print('\n\n\n',train_data,'\n\n\n')
            
debug(('train_data\n',train_data))
debug(('train_target\n',train_target))

debug(('feature_prob\n',feature_prob))
debug(('correct_pred\n',correct_pred))


l = []
for row in range(n_data):
    debug(('**row',train_data[row]),'target',train_target[row])
    m = []
    for k in range(n_class):
        prod = 1
        for i in range(n_features):
            prod = prod * feature_prob[i][k] ** train_data[row,i] * (1 - feature_prob[i][k]) ** (1-train_data[row,i])
            #debug(('prod',prod,'prob[i]',feature_prob[i][k], 'x[i]',train_data[row,i]))
        #debug(('prod_final',prod))
        y = class_prob[k]*prod
        m.append(y)
    debug(('outcomes',m))
    pred = np.argmax(m)
    debug(('prediction',pred))
    #update_prob
    for i in range(n_features):
        if train_data[row,i] == pred:
            correct_pred[i] += 1
    feature_prob[:,0] = correct_pred/(row+2)
    feature_prob[:,1] = 1-feature_prob[:,0]
    debug(('correct_pred\n',correct_pred))
    debug(('feature_prob\n',feature_prob))
print('feature_prob\n',feature_prob)
    
