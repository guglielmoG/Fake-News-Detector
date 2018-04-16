# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 21:53:24 2018

@author: guglielmo
"""

import numpy as np

class bernoulliBN():
    '''Assumption: the number of features stays constant from one time
    to the next one. I only set them up once in fit'''
    def __init__(self):
        np.random.seed(1234)
        self.n_class = 2
        self.tot_observation = 0
        
    def _init(self, X, prior_source=None, prior_news=None):
        self.n_data, self.n_features = X.shape
        self.count = np.zeros(self.n_features)
        self._trust = np.zeros((self.n_features,self.n_class))
        self.prev_X = X[-1]
        self.tot_observation += n_data
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
        
    def fit(self, X, prior_source=None, prior_news=None):
        self._init(X, prior_source=None, prior_news=None)
        
        self._fit(X)
        
    def _fit(self, X):
        print(X)
        count= self.count
        count += np.sum(X, axis=0)
        
        self._update_trust()
        
    def compute_prob(self):
        #computes the value P(news=T | vector of sources), without normalization,
        #applying Bayes TH and properties of Bayesian Networks. The computation 
        #is done using as x's the last observation seen by the network.
        #Notice that by itself needs to be normalized, however it can be compared
        #to previous values to see rate of convergence.
        self._update_trust()
        trust = self._trust
        x = self.prev_X
        cases = []
        for k in range(self.n_class):
            prod = 1
            for i in range(self.n_features):
                prod = prod * trust[i][k] ** x[i] * (1 - trust[i][k]) ** (1-x[i])
            cases.append(prod*self.prior_news[k])
        return np.max(cases)
        
    def _update_trust(self):
        count, trust = self.count, self._trust
        trust[:,0] = count/self.tot_observation
        trust[:,1] = 1- trust[:,0]
        
    def fit_next(self, x):
        #one observation is given, BN updates conditional prob (trust). 
        if x.n_dim == 1 and x.shape[0] == self.n_features:
            self.count += x
            self.tot_observation += 1
            self._update_trust()
        else:
            raise(4)
        
    def update(self, X):
        #updates in bulk, more efficient, exploit broadcasting
        self.count += np.sum(X, axis=0)
        self.tot_observation += X.shape[0]
        
        self._update_trust()
        
if __name__ == '__main__':
    np.set_printoptions(threshold=np.NaN)

    np.random.seed(146654)
     
    n_features = 4
    n_class = 2
    n_data = 20
        
    theoretical_prob = np.random.random(n_features)
    train_data = np.zeros((n_data,n_features))
    mask = np.random.random((n_data,n_features)) < theoretical_prob
    train_data[mask] = 1
              
    print('Train data\n',train_data)
    print('\nTrue probability of a given source to provide real news\n', theoretical_prob)
              
    my_net = bernoulliBN()
    my_net.fit(train_data)

    print('\nEsrimated Probability\n', my_net._trust[:,0], '\n\nIndicator of news being true (not a probability):', my_net.compute_prob())
