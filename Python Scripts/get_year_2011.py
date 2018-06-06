'''
This code was used for extracting the years 2011 from the folder 'UserHisNonEmpty'
folder which was created by the nonempty_rows.py python code file.

It creates a new directory called \UserHistory2011 and looks inside the 'UserHisNonEmpty'
folder. It looks at the UTC time stamp of the codes and gets only the rows that belong
to the year 2011. It then outputs the new tables as .csv files in the folder 
\UserHistory2011. These new files can be found in the teams Google Drive under
the folder 'UserHistory2011'.
'''
import os
import pandas as pd

main = os.getcwd()
path = os.getcwd() + '\UserHisNonEmptyRows'
new_path = os.getcwd() + '\UserHistory2011'

os.chdir(path)

assert os.path.exists(path), "Warning! Directory must contain 'UserHisNonEmpty' folder!' 

if not os.path.exists(new_path):
    os.makedirs(new_path)
#UTC Time
begin_year = 1293840000 #Jan 1, 2011
end_year =   1325376000 #Jan 1, 2012
    
for filename in os.listdir(path):
    user_data = pd.read_csv(filename, delimiter = '\t', index_col = '0')
    user_2011 = user_data.loc[begin_year:end_year]
    user_2011.reset_index(inplace=True) #Resets the row names to integer names again.
    new_filename = filename[:-4] + '_2011.csv'
    user_2011.to_csv(new_path + '\\'+ new_filename, sep = '\t', index = False)
    
os.chdir(main)
