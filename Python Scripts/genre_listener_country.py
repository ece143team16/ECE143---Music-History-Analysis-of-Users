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

def user_country_genre(filename,genres):
    '''
    Looks inside a the .tar file of the MLHD data set. Unzips the folder and 
    looks through the list of folders. It will then check the users for the genres
    specified in the the list 'genres' and identify the country. We do this for all
    the users in the .tar file. Does so for the year 2011.
    
    Parameter: filename
    Type: str
    e.g. 'MLHD_000.tar'
    
    Parameter: genres
    Type: list
    e.g. genres = ['pop','hiphop','rock']
    
    Returns: dictionary containing sub-dictionaries for each country, where each
            item in this sub dictionary contains the data for 
    
    e.g.
    >>> user_country_genre('MLHD_000.tar',['rock','pop','hiphop','jazz','blue','kpop','rap','disco','edm'])
    {'BR': {'blue': 0, 'kpop': 2, 'jazz': 46, 'pop': 68, 'disco': 45, 
            'hiphop': 25, 'rap': 53, 'rock': 72, 'edm': 0}, 
    'DE': {'blue': 0, 'kpop': 4, 'jazz': 57, 'pop': 73, 'disco': 45, 
           'hiphop': 47, 'rap': 64, 'rock': 75, 'edm': 14},
    'NL': {'blue': 0, 'kpop': 0, 'jazz': 18, 'pop': 20, 'disco': 17, 
           'hiphop': 18, 'rap': 20, 'rock': 20, 'edm': 6},
    'UK': {'blue': 0, 'kpop': 2, 'jazz': 64, 'pop': 70, 'disco': 58,
           'hiphop': 53, 'rap': 59, 'rock': 71, 'edm': 6},
    'US': {'blue': 0, 'kpop': 8, 'jazz': 145, 'pop': 165, 'disco': 128,
           'hiphop': 129, 'rap': 147, 'rock': 168, 'edm': 11}}
    
    First it looks for the file in the current directory. Then it opens it into
    a new directory in the current directory. It then goes inside that directory
    and we iterate through all the files in the new directory. We open a user's
    data and we first process it. First it removes empty rows, which are sometimes
    created when there is user activity, but there are no songs, or artists. Then,
    we take only the data that is specific to the year 2011. Before, we proceed,
    we make sure that the user is found in the demopraphics pandas table. If they are
    not found in that table, then we cannot analyze them for demographics data
    and we skip them. If they are found, then proceed to check their data, line
    by line for the genres we are looking for. After we have gone through all their
    data, we include them in the counting for how many users listened to certain
    genres for a given country.
    
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
