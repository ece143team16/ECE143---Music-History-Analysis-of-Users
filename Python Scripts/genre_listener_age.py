import cPickle as pickle
import pandas as pd
import numpy as np
import os
import gzip
import tarfile

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
    
    assert os.path.isfile('MLHD_00.tar'), 'Warning! Specified .tar file must be in current directory.'
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
            array[month_counter] += summation/length
            month_counter += 1
            
        tag_average[tag] = array
    
    return tag_average
            
print average_user_age_genre('MLHD_000.tar',['rock','pop','hiphop','jazz'])

        
    
