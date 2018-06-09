# ECE 143 Music History Analysis of Users

The goal of this project is to help predict which music genres are becoming more popular to help artists and producers understand what resonates the most with listeners. We can even understand how these musical trends relate to important demographics such as age and country of origin.  

## Getting Started

The project contains the necessary Python source files and .csv files. However, since most of our files are very large, Github does not support uploads of these dataset files. Instead, we host them on our Google Drive link below.

### Datasets

We used the Music Listening History Dataset (MLHD) and the MusicBrainz dataset. The MLHD dataset contains ~570k files per user with one log per line in each file. Each log is a quadruple <timestamp, artist-MBID, release-MBID, recording-MBID>.

The MLHD .tar files can be found in http://bit.ly/MLHD-Dataset.

The MusicBrainz dataset can be found in http://ftp.musicbrainz.org/pub/musicbrainz/data/fullexport/. Navigate to the most recent updated folder and download mbdump.tar.bz2 and extract. Be advised that this list is updated weekly so the folder name changes frequently.

### Structure of source files 

#### Clearing Datasets
artist_scraping.ipynb,  
ArtistTagMerge.ipynb,  
ECE 143 artist_tag.ipynb,  
tag table cleanup.ipynb,  
refine_demographics_with_scrobble.ipynb,  
Clear Data.ipynb.  
These notebooks in Notebooks folder extract useful information from original dataset 

For your convenience, Clear Data.ipynb conclude all the codes about clearing datasets and you just need to see it.

#### Doing statistics and plotting graphs
nonempty_rows.py,  
get_year_2011.py,  
genre_listener_country.py, 
genre_listener_age.py,  
Demographics.ipynb,  
plot_genre_listener_country.ipynb,  
plot_artists_vs_time_for_genres.ipynb,  
plot_listeners_vs_age_for_genres.ipynb,  
plot_artists_vs_time_for_genres.ipynb.  
These python notebooks and scripts do statistics and plot corresponding images, which are stored in Images folder.

### How to run the code

To run all the scripts, download zip file of this repository, and uncompress and upload all folder and files to Jupyter Notebook. Jupyter notebook will look like this:

![alt text](https://github.com/ece143team16/ECE143---Music-History-Analysis-of-Users/blob/master/Images/Jupyter%20Setup2.png)

Next clear datasets. Run Clear Data.ipynb in Notebooks folder to clear datasets.

Finally, do statistics and plot graphs. Run all the the source files for doing statistics and plotting graphs



### Google Drive Link

https://drive.google.com/drive/u/2/folders/0AH5Rly84R7TjUk9PVA

### Presentation Link

https://docs.google.com/presentation/d/1NjPvdh9WsMKie4uyfzyCRKIFnBmXPsUZzOVHSUxUaYI/edit#slide=id.g3bb1548e77_0_5

## Authors

* **Erik Seetao** 
* **Humberto Hernandez** 
* **Yihan Hu** 
* **Ruting Yin** 
