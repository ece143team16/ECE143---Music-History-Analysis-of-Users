import cPickle as pickle
import pandas as pd
import numpy as np
import os
import gzip
import tarfile

demographics = pd.read_pickle('demographics.p')
MBID_dictionary = pickle.load( open( "MBID_dictionary.p", "rb" ) )

def user_country_genre(filename,genres):
    '''
    Looks inside a the .tar file of the MLHD data set. Unzips the folder and 
    looks through the list of folders. It will then check the users for the genres
    specified in the the list 'genres' and identify the country. We do this for all
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
    
    country = ['US', 'UK', 'BR', 'NL', 'DE']
    
    country_dic = {}
    for c in country:
        country_dic[c] = {}
        for genre in genres:
            country_dic[c][genre] = 0
              
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

        user_country = demographics.loc[user_uuid,'country']
        
        if not(user_country in country):
            continue
           
        seen = {}
        for tag in genres:
            seen[tag] = False

        if not(user_2011.empty):
            rows = user_2011.shape[0]
            row_counter = 0
            while row_counter < rows:
                MBID = user_2011.iloc[row_counter,0]
                if (MBID in MBID_dictionary):
                    MBID_tags = MBID_dictionary[MBID]
                    MBID_tags_lower = [x.lower() for x in MBID_tags]
                    for tag in genres:
                        if (tag in MBID_tags_lower):
                            seen[tag] = True 
                        
                row_counter += 1
            for key in genres:
                if(seen[key]):
                    country_dic[user_country][key] += 1
                
    os.chdir(main)
    
    return country_dic
