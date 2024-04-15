# **Pyflocolor** (Python Floral Color)

A graphical user interface and workflow centered around the method introduced by Perez-Udell et al. in [An automated pipeline for supervised classification of petal color from citizen science photographs (2019)](https://doi-org.proxy.lib.umich.edu/10.1002/aps3.11505).

This application provides a comprehensive workflow and GUI for downloading iNaturalist occurrences with images of blooming flowers, downloading the associated images of flowers, and identifying the color values of flowers within those images.

Developed by Chris Talbot, 2024.

## Installation
Download the executable for Windows [here](https://drive.google.com/file/d/1iMIJ7X8Quv7RmyOotElQ6DjgQDRfnjiT/view?usp=sharing). Available for OSX and Linux by request.

**Step 1**: Extract files to an empty directory. 

**Step 2**: In the `dist` subfolder, run the executable file `pyflocolor.exe`.

**Step 3**: See instructions below to get started!

## Using the program

### Downloading occurrence data

This feature is a work-in-progress (see "Get Occurrences" menu in-app). For now, occurrence data should be downloaded directly from iNaturalist. 

Occurrences should be stored in separate CSV files for each species, with the file name `{species_name}.csv`. On first run of `pyflocolor.exe`, a directory will be created wherever the executable is stored. Occurrence CSVs should be placed directly into the `AppData/Occurrences` directory.

For best results, occurrences should be limited to those whose phenology is identified as blooming.

### Downloading images from occurrences

Images can be downloaded for some or all species in the `AppData/Occurrences` folder from the "Get Images" menu. The number of images downloaded per species must be specified; species with fewer occurrences will download images for all occurrences.

### Training on color range

The program must be trained to identify clusters likely containing flower petals. In the "Train" menu, select the species to train for, a number of images to use for training, and a starting k value. Higher k values will create more clusters from the image, which makes it more likely a cluster will fully isolate a flower; however, more clusters means more computation time.

Upon beginning training, a new window will open, which will ask you to select the cluster that best represents the flower from the original image. If the flower is not separated from the background, you may increase the k value and try again. If no flower is present in the image, you may skip that image. If you feel you've trained on sufficiently many images for a species, you may force-complete the process for that species.

### Collecting color data

Once the program is trained to identify flowers for a species, the "Collect Data" menu may be used to identify clusters containing flowers, and their associated HSV values, for all downloaded images.

### Processing color data

*Work in progress*
