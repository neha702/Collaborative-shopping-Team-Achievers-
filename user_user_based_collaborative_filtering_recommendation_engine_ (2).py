# -*- coding: utf-8 -*-
"""User- user based Collaborative filtering recommendation engine .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GVA2lC4DZ7ZyvhwEJMM4__XwktKsBHIJ

**User-user based collaborative filtering recommendation system**

For this challenge,we have prepared a user-user based collaborative filtering recommendation system for shopping that will provide us the top similar users to a particular user and the recommended items to that user other than what he/she has liked which will help in promortion of more and more items that it has not chosen before but may like now.

**Data preprocessing**
"""

#Importing the libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Data outlook
data =pd.read_csv('/content/Users_likes_Dislikes_list.csv')
data.head(15)

#Timestamp column is of no use to us, so we will drop it
data.drop(['Timestamp'],inplace=True,axis=1)

#Renaming the columns
data.columns=['Users','Gender','Formal Shirts','Jackets','Casual shirts','Jeans','Skirts','Kurtis',
               'Trousers','Tops']

#Check for missing data in items columns and fill it with 0.
data.isnull().sum()
data=data.fillna(0)
data.isnull().sum()

#Data overlook after preprocessing
data.head(15)

#Function to find relationship(similarity) between two users using pearson correlation coefficient.
def weight_factor(x, y): 
    t1, t2, t3 = 0, 0, 0 
    for i, j in zip(x, y):
        t1+=i*j
        t2+=i*i
        t3+=j*j
    return t1/(np.sqrt(t2) * np.sqrt(t3))

#First one is active user (Neha Das),we find similarity with other users
import numpy as np
x = data.iloc[0,2:]
similarity = np.array([(data.iloc[i,0],weight_factor(x,data.iloc[i, 2:])) for i in range(1,data.shape[0],1)])
similarity

"""**Sorting neighbours based on similarity weights**"""

ind = np.argsort( similarity[:,1] )
similarity = similarity[ind]
similarity

"""**Neigbours based on threshold(Similarity matrix)**"""

#Sorting the weights in descending order giving us the top neighbours first.
index= np.argsort( similarity[:,1] )
index=index[::-1]
similarity=similarity[index]

#We will be taking neighbours having similarity value(weights) more than 0.5
neighbours = similarity[similarity[:,1].astype(float) > 0.5]

#Printing the top 10 neighbours of any user( taking here Neha Das)


#Function to find top users and similar items
def model(user):
    recommended_list=[]
    top_list=[]
    x = data.iloc[data.loc[data.Users == user].index[0],2:]
    similar = np.array([(data.iloc[i,0],weight_factor(x,data.iloc[i, 2:])) for i in range(0,data.shape[0],1)])
    index= np.argsort( similar[:,1] )
    index=index[::-1]
    similar=similar[index] 
    neighbours = similar[similar[:,1].astype(float) > 0.6]  #Taking threshold as 0.6
    for i in range(0,len(neighbours),1):
        for j in range(2,len(data.columns),1):
            if data.iloc[data.loc[data.Users == neighbours[i][0]].index[0],j]==1 and data.iloc[data.loc[data.Users == user].index[0],j]==0:
               recommended_list.append(data.columns[j])
    if (len(neighbours)>10):
       for i in range(0,10,1):  #Top 10 neighbours
           top_list.append(neighbours[i][0])
    else:
       for i in range(len(neighbours)):
            top_list.append(neighbours[i][0])
    if user in top_list: #Remove the user of which we are asked to find neighbours,each user is always strongly correlated with itself and its of no use to us.
       top_list.remove(user) #
    
    recommended_array=np.unique(np.array(recommended_list))#
    return top_list,recommended_array

#Displaying the model result.


"""**Pickling the model**"""

import pickle

#pickling the model
pickle.dump(model,open("model.pkl", 'wb'))


"""**Deploying model**

**Finding requirements.txt**

**NOTE:** This is only feasible for user names in database.
"""
