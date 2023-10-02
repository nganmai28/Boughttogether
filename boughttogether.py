#Load in the essential libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations,combinations
from collections import Counter

#create a function that finds pairs and list them in a column. Using A and B as a stand in
def find_pairs(x):
    pairs = pd.DataFrame(list(permutations(x.values,2)),columns=["A","B"])
    return pairs

#Load in the dataset and check the head of the data
dataset=pd.read_csv('14 days.csv')
#dataset.head()

#Group the Seller SKU by Buyer Username then apply the function 
dataset_combo =dataset.groupby('Buyer Username')['Seller SKU'].apply(find_pairs).reset_index(drop=True)
#dataset_combo.head()

#  Calculate how often each item item_a occurs with the items in item_b
dataset_combo2 =dataset_combo.groupby(['A','B']).size()

#create a sorted dataframe by the most frequent combinations.
dataset =dataset_combo2.reset_index()
dataset.columns = ['A','B',"Size"]
dataset.sort_values(by='Size',ascending =False, inplace =True)

#Create a combination of groups so that can be used as an alternative to pairing
df2=pd.read_csv('14 days.csv')
df2= df2.dropna()
df2 =df2[df2['Buyer Username'].duplicated(keep=False)]
df2['Group'] = df2.groupby('Buyer Username')['Seller SKU'].transform(lambda x:','.join(x))
df2 =df2[['Buyer Username', 'Group']].drop_duplicates()

#Count each row combination by the the pairing of the two
count = Counter()
for row in df2['Group']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list,2)))

#check out the most common combination. 
for key, value in count.most_common(10):
    print(key,value)