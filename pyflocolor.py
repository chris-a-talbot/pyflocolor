import sys
from PySide6.QtWidgets import QApplication
import pyflocolor_functions as pfc_func
import pyflocolor_windows as pfc_win


def create_app():
    app = QApplication(sys.argv)
    pfc_func.setup_directories()
    window = pfc_win.MainInterface()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    create_app()


# /*
#  * Step 1: Make a GUI that can interface with the location of my data
#  * On first run, initialize the data library:
#  * Data
#  * -- Images
#  * -- Output
#  * -- Values
#  * -- Occurrences
#  *
#  * Step 2: Then, the GUI should have four distinct sections:
#  * - Get Occurrences
#  * - Get Images
#  * - Train Model
#  * - Process Images
#  * - Process Data
#  *
#  * Step 3: Get Occurrences should allow for the input of a species name or list of species names
#  *         and then interface with iNaturalist to download the occurrences of those species.
#  *         There must be options to filter the iNaturalist download in accordance with the API.
#  *         Alternatively, the user can upload a CSV file with the list of species.
#  *         Also, alternatively, the user can input a download link.
#  *         The occurrences should be stored in the Data/Occurrences folder in a file {species_name}.csv.
#  *         It may be worth including the ability to get images from other sources?
#  *
#  * Step 4: Get Images should get the images from all occurrences in the Data/Occurrences folder.
#  *         It could also be designed to allow for selecting specific species from the Occurrences folder.
#  *         It needs to filter which have already been downloaded to avoid wasted time,
#  *         but it also needs to be able to re-download images if the user desires.
#  *         It also needs to accept a number which will define how many images, at most, to download per species.
#  *         The images should be stored in the Data/Images folder in a subfolder named {species_name} and with filename {occurrence_id).{filetype}.
#  *
#  * Step 5: Train Model should allow the user to interface with the images of a species to determine min/max HSV and k values.
#  *         The user should be able to select a species from the Data/Images folder or loop through all species without values in Data/Values.
#  *         The user should be able to select a number of images to train on, with a default of 10.
#  *         The user should be able to select the starting k value, with a default of 10.
#  *         The interface will then display images and allow the user to select clusters displaying flowers.
#  *         It will also allow for skipping, going back an image, changing k, or force-completing for the species.
#  *         The output should be stored in Data/Values/{species_name}.csv.
#  *
#  * Step 6: Collect Data should allow the user to select a {species_name}.csv from Data/Values and process the images in Data/Images/{species_name}.
#  *         It should start by creating a CSV consisting of a single column containing the paths to all images of the species.
#  *         It then performs the KMeans process on all the images and selects clusters with flowers based on values from Data/Values.
#  *         It then outputs an updated CSV to Data/Output/{species_name}.csv containing paths to images and the KMeans HSV values.
#  *
#  * Step 7: The Process Data interface could feature a variety of options for each species once output is generated,
#  *         including getting the mean color, color range, classifying images for polymorphic species, etc.
#  */