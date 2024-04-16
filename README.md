# **Pyflocolor** (Python Floral Color)

A graphical user interface and workflow centered around the method introduced by Perez-Udell et al. in [An automated pipeline for supervised classification of petal color from citizen science photographs (2019)](https://doi-org.proxy.lib.umich.edu/10.1002/aps3.11505). Substantial portions of the code associated with k-means clustering and image preparation are borrowed from this paper and associated GitHub repository, [found here](https://github.com/atudell/Color-Cluster-Kit).

This application provides a comprehensive workflow and GUI for downloading iNaturalist occurrences with images of blooming flowers, downloading the associated images of flowers, and identifying the color values of flowers within those images.

Developed by Chris Talbot for work on a senior thesis project at the University of Michigan, 2024.

## Installation
Download the latest release as a .exe from GitHub. Available for OSX and Linux by request.

## Using the program

Upon running `pyflocolor.exe`, several new folders will be created in the directory of the executable file. You will be presented with a menu with five options:

![Main menu](https://github.com/chris-a-talbot/pyflocolor/assets/44279777/21916fcf-92ab-464b-ac6b-bcb4c86025f7)

### Downloading occurrence data

This feature is a work-in-progress (see "Get Occurrences" menu in-app). For now, occurrence data should be downloaded directly from iNaturalist. 

Occurrences should be stored in separate CSV files for each species, with the file name `{species_name}.csv`. On first run of `pyflocolor.exe`, a directory will be created wherever the executable is stored. Occurrence CSVs should be placed directly into the `AppData/Occurrences` directory.

For best results, occurrences should be limited to those whose phenology is identified as blooming.

### Downloading images from occurrences

Images can be downloaded for some or all species in the `AppData/Occurrences` folder from the "Get Images" menu. Images are stored in `AppData/Images`. 

You may select a set of species from the list, or select "Do all species in list". If your files are not showing up, try hitting "Refresh List".

The number of images downloaded per species is set to 100 by default, but may be changed; species with fewer occurrences will download images for all occurrences. 

If "Re-download images" is checked, images will be downloaded from the occurrences even if the image already exists in `AppData/Images`.

**Downloads may take a while - no progress bar is implemented - please do not close the page until the status is updated from "Ready" to "Complete"!**

!["Get Images" menu](https://github.com/chris-a-talbot/pyflocolor/assets/44279777/0d4bc161-09d4-450f-9e71-f358095389de)

### Training on color range

The program must be trained to identify clusters likely containing flower petals. In the "Train" menu, select the species to train for, a number of images to use for training, and a starting k value. Higher k values will create more clusters from the image, which makes it more likely a cluster will fully isolate a flower; however, more clusters means more computation time. Defaults are set to 10 images per species and a starting k of 5, but a starting k of 10 is recommended for most species. 

!["Train" menu](https://github.com/chris-a-talbot/pyflocolor/assets/44279777/554d93ce-e677-4551-ae1c-01622bcb4bcc)

Upon beginning training, a new window will open, which will ask you to select the cluster that best represents the flower from the original image. If the flower is not separated from the background, you may increase the k value and try again. If no flower is present in the image, you may skip that image. If you feel you've trained on sufficiently many images for a species, you may force-complete the process for that species. Note that the clusters are 0-indexed, and the color tile & image for a cluster is displayed *below* the associated cluster number.

![Train](https://github.com/chris-a-talbot/pyflocolor/assets/44279777/772ba49f-dc6b-469b-8e82-4c4484328b00)

### Collecting color data

Once the program is trained to identify flowers for a species, the "Collect Data" menu may be used to identify clusters containing flowers, and their associated HSV values, for all downloaded images.

**This process may take a while - no progress bar is implemented - please do not close the page until the status is updated from "Ready" to "Complete"!**

!["Collect Data" menu](https://github.com/chris-a-talbot/pyflocolor/assets/44279777/e0a156ee-8212-485e-a835-60c19827b709)

### Processing color data

*Work in progress*
