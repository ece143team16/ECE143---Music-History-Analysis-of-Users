# ECE 143 Music History Analysis of Users

The goal of this project is to help predict which music genres are becoming more popular to help artists and producers understand what resonates the most with listeners. We can even understand how these musical trends relate to important demographics in a population such as age and country of origin.  

## Getting Started

The project contains the necessary jupyter notebooks and csv files. However, since most of our files are very large, Github does not support uploads of these dataset files. Instead, we host them on our Google Drive link below.

### Datasets

We used the Music Listening History Dataset (MLHD) and the MusicBrainz dataset. The MLHD dataset contains ~570k files per user with one log per line in each file. Each log is a quadruple <timestamp, artist-MBID, release-MBID, recording-MBID>.

The MLHD .tar files can be found in http://bit.ly/MLHD-Dataset.

The MusicBrainz dataset can be found in http://ftp.musicbrainz.org/pub/musicbrainz/data/fullexport/. Navigate to the most recent updated folder and download mbdump.tar.bz2 and extract. Be advised that this list is updated weekly so the folder name changes frequently.

### Clearing Datasets
artist_scraping.ipynb,  
ArtistTagMerge.ipynb,  
ECE 143 artist_tag.ipynb,  
tag table cleanup.ipynb,  
refine_demographics_with_scrobble.ipynb.   
These notebooks in Notebooks folder extract useful information from original dataset 

For your convenience, Clear Data.ipynb conclude all the codes about clearing datasets and you just need to see it.

### Do statistics and plot
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

### Jupyter Notebook Setup

To run all the scripts, set up the Jupyter notebook similar to this:

![alt text](https://github.com/ece143team16/ECE143---Music-History-Analysis-of-Users/blob/master/Images/Jupyter%20Setup.png)






### Google Drive Link

https://drive.google.com/drive/u/2/folders/0AH5Rly84R7TjUk9PVA

### Presentation Link

https://docs.google.com/presentation/d/1NjPvdh9WsMKie4uyfzyCRKIFnBmXPsUZzOVHSUxUaYI/edit#slide=id.g3bb1548e77_0_5

## Authors

* **Erik Seetao** 
* **Humberto Hernandez** 
* **Yihan Hu** 
* **Ruting Yin** 
