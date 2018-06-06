import cPickle as pickle
import pandas as pd
import numpy as np
import os
import gzip
import tarfile

assert os.path.isfile('MBID_dictionary.p'), 'Warning! MBID_dictionary.p must be in current directory!'
assert os.path.isfile('demographics.p'), 'Warning! demographics.p must be in current directory!'

demographics = pd.read_pickle('demographics.p')
MBID_dictionary = pickle.load( open( "MBID_dictionary.p", "rb" ) )

def average_user_age_genre(filename,genres):
    '''
    Looks inside a the .tar file of the MLHD data set. Unzips the folder and 
    looks through the list of folders. It will then check the users for the genres
    specified in the the list 'genres' and identify there age. We do this for all
    the users in the .tar file.
    
    Parameter: filename
    Type: str
    e.g. 'MLHD_000.tar'
    
    Parameter: genres
    Type: list
    e.g. genres = ['pop','hiphop','rock']
    
    Returns: A dictionary containing the genres as the keys, where each key refers
            to a twelve element array containing floating point numbers, each
            containing the average age for the respective month. For example,
            the 0th element in the array refers to the month of January, and so
            on.
            
    e.g.
    >>> average_user_age_genre('MLHD_000.tar',
    ... ['rock','pop','hiphop','jazz','blue','kpop','rap','disco'])
    ...
    {'blue': array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]), 
    'kpop': array([24.63636364, 23.96666667, 23.83870968, 23.6969697 , 24.6       ,
       24.55      , 24.06896552, 23.6969697 , 23.75      , 24.61111111,
       23.57142857, 24.52380952]), 
    'jazz': array([25.61132812, 25.42429577, 25.53379549, 25.54651163, 25.46716698,
       25.675     , 25.45421245, 25.58614865, 25.63979417, 25.86848635,
       26.29166667, 25.70416667]), 
    'pop': array([25.1762963 , 25.01551481, 25.00278164, 25.12087912, 25.15789474,
       25.2828125 , 25.05308465, 25.11618257, 25.10540915, 25.32013201,
       25.33272395, 25.15082956]), 
    'disco': array([25.44642857, 25.36808511, 25.39300412, 25.32251908, 25.35251799,
       25.47239264, 25.32879819, 25.30994152, 25.42284569, 25.85106383,
       25.96818182, 25.49589041]), 
    'hiphop': array([25.15064935, 25.17248908, 25.27659574, 25.15384615, 25.11219512,
       25.18181818, 25.2091954 , 25.21325052, 25.2605042 , 25.10996564,
       25.2008547 , 25.08839779]), 
    'rap': array([24.76923077, 24.58892617, 24.59136213, 24.71612903, 24.69784173,
       24.80345572, 24.62564991, 24.71009772, 24.69306931, 24.81463415,
       24.89766082, 24.65551181]), 
    'rock': array([25.12164074, 25.01775956, 25.00681199, 25.10675676, 25.04888268,
       25.2       , 25.02209945, 25.10176391, 25.10326087, 25.30414747,
       25.36893204, 25.08189655])}
    
    First, it looks for the file in the current directoy. Then once it finds it
    it opens it in a new directory that's inside the current directory. Each file
    in the new directory refers to a user's data. Where the name of the file
    is the user's id in the MLHD data set. We iterate over each user in that directory.
    First we load it into a pandas dataframe and we process it. We remove keep
    the non-empty rows and extract the year 2011. Then we create sub-dataframes
    for each month in the year 2011. If a user listens to a certain genre during
    a given month, we append there age in the list which is contained under
    the key for that month in the genre's dictionary. After we have gone through
    the entire folder, we get the average by adding up all the ages over the number
    of users for that genre for that given month. We then return a dictionary containing
    a 12-element array for the year 2011, saved under the key representing that genre.
    Where each element in the array represents a month from the year 2011.
    
    Assertions:
        - filename must be str
        - genres must be a list of strings.
        - filename must refer to MLHD data set and be .tar file.
        - Specified file must be in the current directory.
        
    '''
    assert isinstance(filename,str), 'Warning! Filename must be a string!'
    assert isinstance(genres, list), 'Warning! genres must be a list of strings!'
    assert filename[0:4] == 'MLHD', 'Warning! Specified file must be from the MLHD dataset!'
    assert filename[-4:] == '.tar', 'Warning! Must be a .tar file from the MLHD dataset!'
    
    assert os.path.isfile(filename), 'Warning! Specified .tar file must be in current directory.'
    for genre in genres:
        assert isinstance(genre,str), 'Warning! genres list must contain strings only!'
        
    genres_lower_case = [x.lower() for x in genres]
    genres = genres_lower_case    
    
    main = os.getcwd()
    
    path = os.getcwd() + '\\' + filename[:-4]
    
    if not os.path.exists(path):
        os.makedirs(path)
        
    f = tarfile.open(filename)
    f.extractall(path)
    f.close()
    
    os.chdir(path)
    
    tags_age = {}
    month_str = ['jan','feb','march','april','may','june','july',
                 'august','september','october','november','december']
    for genre in genres:
        tags_age[genre] = {'jan' : [],
                        'feb' : [],
                        'march' : [],
                        'april' : [],
                        'may':[],
                        'june':[],
                        'july':[],
                        'august':[],
                        'september': [],
                        'october': [],
                        'november': [],
                        'december': [],
                        } #Array of ages.
    
    for file_i in os.listdir(path):
        user_uuid = file_i[:-7]
        
        with gzip.open(file_i) as f:
            history = pd.read_csv(f, delimiter = '\t', header = None)  
            
        history_relevant = history.drop([2,3], axis = 1)
        new_history = history_relevant.dropna()
        
        #Setting UTC Time Stamp to be the row index.
        new_history = new_history.set_index(0)
        
        user_2011 = new_history.loc[1293840000:1325376000]
#        user_2011.reset_index(inplace=True) #Resets the row_index into a column again.
        #CHECK IF NAN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        if not(user_uuid in demographics.index):
            continue

        age = demographics.loc[user_uuid,'age']
        
        if not(pd.isnull(age)):
            jan = user_2011.loc[1293840000:1296518400]
            feb = user_2011.loc[1296518400:1298937600]
            march = user_2011.loc[1298937600:1301616000]
            april = user_2011.loc[1301616000:1304208000]
            may = user_2011.loc[130420800:1306886400]
            june = user_2011.loc[1306886400:1309478400]
            july = user_2011.loc[1309478400:1312156800]
            august = user_2011.loc[1312156800:1314835200]
            september = user_2011.loc[1314835200:1317427200]
            october = user_2011.loc[1317427200:1320105600]
            november = user_2011.loc[1320105600:1322697600]
            december = user_2011.loc[1322697600:1325376000]
            
            months_of_2011 = [jan,feb,march,april,may,june,july,
                      august,september,october,november,december]
           
            seen = {}
            for tag in genres:
                seen[tag] = False
            month_counter = 0
            for month in months_of_2011:
#                print month
                if not(month.empty):
                    rows = month.shape[0]
                    row_counter = 0
                    while row_counter < rows:
                        MBID = month.iloc[row_counter,0]
                        if (MBID in MBID_dictionary):
                            MBID_tags = MBID_dictionary[MBID]
                            MBID_tags_lower = [x.lower() for x in MBID_tags]
                            for tag in genres:
                                if (tag in MBID_tags_lower):
                                    seen[tag] = True
                                
                        row_counter += 1
                for key in tags_age:
                    if(seen[key]):
                        tags_age[key][month_str[month_counter]].append(age)
                    
                month_counter += 1
                
    os.chdir(main)
    tag_average =  {}
    for tag in tags_age:
        month_counter = 0
        array = np.zeros(12)
        for month in tags_age[tag]:
            summation = sum(tags_age[tag][month])
            length = len(tags_age[tag][month])
            if not(length == 0):
                array[month_counter] += summation/length
                
            month_counter += 1
            
        tag_average[tag] = array
    
    return tag_average    
