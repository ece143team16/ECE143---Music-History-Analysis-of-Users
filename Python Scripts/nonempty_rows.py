import os
import pandas as pd
#os.getcwd() returns a string for the current directory.
#os.lisdir() returns a list of all the current items in that directory.
#print os.getcwd()
main = os.getcwd()
path = os.getcwd() + '\User History'
#print os.listdir(path)
new_path = os.getcwd() + '\UserHisNonEmptyRows'
os.chdir(path)

assert os.path.exists(path), "Warning! Directory must contain 'User History' folder!' 

if not os.path.exists(new_path):
    os.makedirs(new_path)

for filename in os.listdir(path):
    history = pd.read_csv(filename, delimiter = '\t', header = None)
    history_relevant = history.drop([2,3], axis = 1)
    new_history = history_relevant.dropna()
    new_filename = filename[:-4] + '.csv'
    new_history.to_csv(new_path + '\\'+ new_filename, sep = '\t', index = False)
    
os.chdir(main)
