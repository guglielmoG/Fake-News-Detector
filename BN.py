# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 21:53:24 2018

@author: guglielmo
"""

import numpy as np

debug = lambda x: print(*x)

np.set_printoptions(threshold=np.NaN)

np.random.seed(146654)
 
n_features = 4
n_class = 2

class_prob = np.ones(n_class)/n_class
feature_prob = np.ones((n_features, n_class))*9/10 #prob of true news
correct_pred = np.ones(n_features)

theoretical_prob = np.random.random(n_features)

n_data = 20
train_data = np.zeros((n_data,n_features))
mask = np.random.random((n_data,n_features)) < theoretical_prob
train_data[mask] = 1

#for i in range(n_data):
#    if np.random.random() > 0.01:
#        train_data[i][0] = 1-train_target[i]
#print(sum(train_data[:,0]==train_target))

print('Train data\n',train_data)
print('\nTrue probability of a given source to provide real news\n', theoretical_prob)
            
#debug(('train_data\n',train_data))

#debug(('theoretical_prob\n',theoretical_prob))
#debug(('correct_pred\n',correct_pred))

class bernoulliBN():
    def __init__(self):
        np.random.seed(1234)
        self.n_class = 2
        
    def fit(self, X, prior_source=None, prior_news=None):
        self.n_data, self.n_features = X.shape
        self.X = X
        #is it needed?
        if prior_source is None:
            prior_source = np.ones(n_features)
        else:
            if prior_source.ndim != 1:
                raise(1)
            elif sum(prior_source) != 1:
                raise(2)
        if prior_news is None:
            prior_news = np.repeat(0.5,self.n_class)
        else:
            if not 0 <= prior_news <= 1:
                raise(3)
        
        self.prior_news = prior_news
        self.prior_source = prior_source
        self._fit()
        
    def _fit(self):
        X = self.X
        n_features = self.n_features
        trust = np.zeros((n_features,2))
        trust[:,0] = np.sum(X, axis=0)/self.n_data
        trust[:,1] = 1- trust[:,0]
        
        cases = []
        for k in range(self.n_class):
            prod = 1
            for i in range(n_features):
                prod = prod * trust[i][k] ** X[-1,i] * (1 - trust[i][k]) ** (1-X[-1,i])
            cases.append(prod*self.prior_news[k])
        best = np.argmax(cases)
        self._trust = trust
        self._best = (cases[best], best)
        
    def update(self, X):
        rows, features = X.shape
        tot = rows + self.n_data
        m1 = self._trust[:,0] * self.n_data

                        
        new_count = np.sum(X, axis=0)
        tot_count = m1 + new_count
        assert tot_count[0] < tot
        new_trust = np.zeros((self.n_features,2))
        new_trust[:,0] = tot_count/tot
        new_trust[:,1] = 1-new_trust[:,0]
        self._new_trust = new_trust
        
my_net = bernoulliBN()
my_net.fit(train_data)
print('\nEsrimated Probability\n', my_net._trust[:,0], '\n\nProbability of being a fake news:', my_net._best[0])

#my_net = bernoulliBN()
#source = ['www.quotidiano.net','http://www.ansa.it']
#p_t1 = [0.7, 0.8]
#p_t2 = [0.5, 0.8]
#X_t1 = np.zeros((10,2))
#X_t2 = np.zeros((10,2))
#X_t1[np.random.random((10,2))<p_t1] = 1
#print('Data time t=0\n', X_t1)
#my_net.fit(X_t1)
#trust_t1 = my_net._trust
#print('Data time t=1\n', X_t2)
#X_t2[np.random.random((10,2))<p_t2] = 1
#my_net.update(X_t2)
#trust_t2 = my_net._new_trust
#
#
#
#print('\nmy_net._trust1\n', trust_t1, '\nmy_net._trut2\n', trust_t2)
#     