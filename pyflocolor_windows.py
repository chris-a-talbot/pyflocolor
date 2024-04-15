from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtCore import (Qt, Signal)
from PySide6.QtGui import QIcon
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
import pyflocolor_functions as pfc_func
import pyflocolor_utils as pfc_utils
import os
import random
from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget, QMessageBox, QLineEdit, QCheckBox, QApplication
import csv
import pandas as pd

# Main Window
class MainInterface(QWidget):
    def __init__(self):
        # Initialize the main window
        super().__init__()
        self.setWindowTitle('PyFlower Cluster Kit')
        self.resize(800, 400)
        layout = QVBoxLayout(self)

        # Sub-window preparation
        self.get_occurrences_window = GetOccurrencesWindow()
        self.get_images_window = GetImagesWindow()
        self.train_window = GetTrainWindow()
        self.collect_data_window = CollectDataWindow()
        self.process_data_window = ProcessDataWindow()

        # Set up the "Get Occurrences" button
        btn_get_occurrences = QPushButton('Get Occurrences (Not Ready)')
        btn_get_occurrences.clicked.connect(self.open_get_occurrences_window)
        layout.addWidget(btn_get_occurrences)

        # Set up the "Get Images" button
        btn_get_images = QPushButton('Get Images')
        btn_get_images.clicked.connect(self.open_get_images_window)
        layout.addWidget(btn_get_images)

        # Set up the "Train" button
        btn_train = QPushButton('Train')
        btn_train.clicked.connect(self.open_train_window)
        layout.addWidget(btn_train)

        # Set up the "Collect Data" button
        btn_collect_data = QPushButton('Collect Data')
        btn_collect_data.clicked.connect(self.open_collect_data_window)
        layout.addWidget(btn_collect_data)

        # Set up the "Process Data" button
        btn_process = QPushButton('Process Data (Not Ready)')
        btn_process.clicked.connect(self.open_process_data_window)
        layout.addWidget(btn_process)

    # Define what to do when "Get Occurrences" is clicked
    def open_get_occurrences_window(self):
        self.get_occurrences_window.show()

    # Define what to do when "Get Images" is clicked
    def open_get_images_window(self):
        self.get_images_window.show()

    # Define what to do when "Train" is clicked
    def open_train_window(self):
        self.train_window.show()

    # Define what to do when "Collect Data" is clicked
    def open_collect_data_window(self):
        self.collect_data_window.show()

    # Define what to do when "Process Data" is clicked
    def open_process_data_window(self):
        self.process_data_window.show()


# "Get Occurrences" Window
class GetOccurrencesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Get Occurrences (Work in Progress)')
        self.resize(800, 400)
        self.layout = QVBoxLayout(self)

        back_button = QPushButton('Back')
        back_button.clicked.connect(self.close)
        self.layout.addWidget(back_button, alignment=Qt.AlignTop | Qt.AlignRight)


# "Get Images" Window
class GetImagesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Get Images')
        self.resize(800, 400)
        self.layout = QHBoxLayout(self)

        self.list_widget = QListWidget()
        self.populate_list('AppData/Occurrences')
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        self.layout.addWidget(self.list_widget)

        self.setup_right_column()

        # Implement a back button
        back_button = QPushButton('Back')
        back_button.clicked.connect(self.close)
        self.layout.addWidget(back_button, alignment=Qt.AlignTop | Qt.AlignRight)

    def populate_list(self, directory):
        try:
            for file_name in os.listdir(directory):
                self.list_widget.addItem(file_name)
        except FileNotFoundError:
            QMessageBox.warning(self, "Directory Not Found", f"Could not find directory: {directory}")

    def setup_right_column(self):
        right_column = QVBoxLayout()

        refresh_button = QPushButton("Refresh List")
        refresh_button.clicked.connect(self.refresh_list)  # Connect to a new method
        right_column.addWidget(refresh_button)

        self.num_images_input = QLineEdit()
        self.num_images_input.setPlaceholderText("# of images to download (default=100)")
        right_column.addWidget(self.num_images_input)

        self.collect_all_checkbox = QCheckBox("Do all species in list?")
        right_column.addWidget(self.collect_all_checkbox)

        self.redownload = QCheckBox("Re-download images if they already exist?")
        right_column.addWidget(self.redownload)

        start_button = QPushButton("Start")
        start_button.clicked.connect(self.start_download)
        right_column.addWidget(start_button)

        self.status_label = QLabel("Ready")
        self.status_label.setWordWrap(True)  # Enable word-wrapping
        self.status_label.setTextFormat(Qt.RichText)  # Set the text format to rich text
        right_column.addWidget(self.status_label)

        self.layout.addLayout(right_column)

    def refresh_list(self):
        self.list_widget.clear()  # Clear the existing list
        self.populate_list('AppData/Occurrences')  # Repopulate the list

    def start_download(self):
        if self.num_images_input.text():
            num_images = int(self.num_images_input.text())
        else:
            num_images = 100
        collect_all = self.collect_all_checkbox.isChecked()
        re_download = self.redownload.isChecked()

        if collect_all:
            selected_files = os.listdir('AppData/Occurrences')  # Get all files in the directory
        else:
            selected_files = [item.text() for item in self.list_widget.selectedItems()]  # Collect all selected items

        current_text = self.status_label.text()
        new_text = f"<br>Downloading {len(selected_files)} images - this may take a while!"
        self.status_label.setText(current_text + new_text)

        pfc_func.download_images(selected_files, num_images, re_download)

        current_text = self.status_label.text()
        new_text = f"<br>Image downloads complete!"
        self.status_label.setText(current_text + new_text)


# "Train" Window
class GetTrainWindow(QWidget):
    def __init__(self):
        # Initialize the "Train" window
        super().__init__()
        self.setWindowTitle('Train Model')
        self.resize(800, 600)
        layout = QHBoxLayout(self)

        # Set up the left-side directory window
        self.list_widget = QListWidget()
        self.populate_list('AppData/Images')
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.list_widget)

        # Initialize all the Widgets for the right column
        self.do_all_species_checkbox = QCheckBox("Do all species in list?")
        self.redo_species_checkbox = QCheckBox("Re-train on species if already trained?")
        self.num_species_input = QLineEdit()
        self.start_k_input = QLineEdit()

        self.values = [None for _ in range(7)]

        # Set up the right-side menu
        self.setup_right_column()

        # Implement a back button
        back_button = QPushButton('Back')
        back_button.clicked.connect(self.close)
        layout.addWidget(back_button, alignment=Qt.AlignTop | Qt.AlignRight)

    # Populate the left column with the contents of the directory
    def populate_list(self, directory):
        try:
            for subfolder in os.listdir(directory):
                if os.path.isdir(os.path.join(directory, subfolder)):
                    self.list_widget.addItem(subfolder)
        except FileNotFoundError:
            QMessageBox.warning(self, "Directory Not Found", f"Could not find directory: {directory}")

    # Set up the right column with the menu
    def setup_right_column(self):
        right_column = QVBoxLayout()  # Initialize the right column

        refresh_button = QPushButton("Refresh List")
        refresh_button.clicked.connect(self.refresh_list)  # Connect to a new method
        right_column.addWidget(refresh_button)

        # Add the checkboxes
        right_column.addWidget(self.do_all_species_checkbox)
        right_column.addWidget(self.redo_species_checkbox)

        # Add the input fields
        self.num_species_input.setPlaceholderText("# images to train on (default=10)")
        right_column.addWidget(self.num_species_input)
        self.start_k_input.setPlaceholderText("Starting k value (default=5)")
        right_column.addWidget(self.start_k_input)

        # Add the "Train" button, which will initiate self.start_training
        train_button = QPushButton("Train")
        train_button.clicked.connect(self.start_training)
        right_column.addWidget(train_button)

        self.status_label = QLabel("Ready")
        self.status_label.setWordWrap(True)  # Enable word-wrapping
        self.status_label.setTextFormat(Qt.RichText)  # Set the text format to rich text
        right_column.addWidget(self.status_label)

        # Add the right column to the layout
        self.layout().addLayout(right_column)

    def refresh_list(self):
        self.list_widget.clear()  # Clear the existing list
        self.populate_list('AppData/Images')  # Repopulate the list

    # Start the training process
    def start_training(self):
        # Retrieve the values from the input fields
        self.do_all_species = self.do_all_species_checkbox.isChecked()
        self.redo_species = self.redo_species_checkbox.isChecked()
        if self.num_species_input.text():
            self.num_species = int(self.num_species_input.text())
        else:
            self.num_species = 10
        if self.start_k_input.text():
            self.start_k = int(self.start_k_input.text())
        else:
            self.start_k = 5

        # Retrieve the list of folders to train with
        if self.do_all_species:
            self.selected_folders = [item.text() for item in self.list_widget.findItems("*", Qt.MatchWildcard)]
        else:
            self.selected_folders = [item.text() for item in self.list_widget.selectedItems()]

        # Process the first folder
        self.current_folder_index = 0
        self.process_next_folder()

    # Process the next folder
    def process_next_folder(self):
        # Stop if all folders have been processed
        if self.current_folder_index < len(self.selected_folders):
            folder = self.selected_folders[self.current_folder_index]  # Get the current folder
            # Get the images from the current folder
            self.images = os.listdir(os.path.join('AppData/Images', folder))
            # Randomly select a subset of images
            self.selected_images = random.sample(self.images, min(self.num_species, len(self.images)))
            # Process the first image
            self.current_image_index = 0
            self.process_image()

    # Process the next image
    def process_image(self):
        folder = self.selected_folders[self.current_folder_index]  # Get the current folder
        image = self.selected_images[self.current_image_index]  # Get the current image
        # Get the html summary of the image
        html_summary = pfc_func.get_summary_visual(os.path.join('AppData/Images', folder, image), self.start_k)
        # Open the review window to train on this image
        self.review_window = ReviewWindow(html_summary, folder, image, self.current_image_index + 1,
                                          len(self.selected_images), self.start_k)

        # Connect the "Closed" signal from ReviewWindow to on_review_window_closed
        self.review_window.closed.connect(self.on_review_window_closed)
        # Connect the "Increase k and repeat" signal from ReviewWindow to on_increase_k_and_repeat
        self.review_window.increase_k_and_repeat.connect(self.on_increase_k_and_repeat)
        self.review_window.skip_image_and_add_one.connect(self.on_skip_image_and_add_one)
        self.review_window.force_complete.connect(self.on_force_complete)
        self.review_window.show()  # Show the image

    def on_review_window_closed(self, values):
        self.current_image_index += 1
        if self.current_image_index < len(self.selected_images):
            self.update_values(values)
            self.process_image()
        else:
            self.update_values(values)
            self.store_values()
            current_text = self.status_label.text()
            new_text = f"<br>Species {self.selected_folders[self.current_folder_index]} complete!"
            self.status_label.setText(current_text + new_text)
            self.current_folder_index += 1
            self.process_next_folder()

    def on_increase_k_and_repeat(self, new_start_k):
        self.start_k = new_start_k  # Update the start_k value
        self.process_image()  # Re-open the ReviewWindow with the new start_k

    def on_skip_image_and_add_one(self):
        self.current_image_index += 1
        self.selected_images.append(random.sample(self.images, 1)[0])
        self.process_image()

    def on_force_complete(self):
        self.current_folder_index += 1
        self.store_values(values)
        self.process_next_folder()

    def update_values(self, values):
        if not self.values[0]:
            self.values = values
        else:
            for i in range(3):
                if values[i] < self.values[i]:
                    self.values[i] = values[i]

            # Update the second group of three elements if necessary
            for i in range(3, 6):
                if values[i] > self.values[i]:
                    self.values[i] = values[i]

            self.values[6] = values[6]

        print(self.values)

    def store_values(self):
        species = self.selected_folders[self.current_folder_index]
        csv_filename = rf"AppData/Values/{species}.csv"
        with open(csv_filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Min H', 'Min S', 'Min V', 'Max H', 'Max S', 'Max V', 'K'])
            csvwriter.writerow(self.values)

        input_folder = rf"AppData/Images/{species}"
        output_csv_filename = rf"AppData/Output/{species}.csv"

        # Get a list of file paths within the input folder
        file_paths = os.listdir(input_folder)

        # Write the file paths to a CSV file
        with open(output_csv_filename, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Write the header row
            writer.writerow(['path'])

            # Write file paths to the CSV file
            for path in file_paths:
                full_path = f"AppData/Images/{species}/{path}"
                writer.writerow([full_path])

        print(f"CSV file '{csv_filename}' has been created in the 'Output' and 'Values' folders.")
        self.values = [None for _ in range(7)]


# Sub-window of the "Train" Window
class ReviewWindow(QWidget):
    closed = Signal(list)  # Signal when the window is closed
    increase_k_and_repeat = Signal(int)  # Signal to increase k and repeat the process
    skip_image_and_add_one = Signal()  # Signal to skip the current image and add another to the list
    force_complete = Signal()  # Signal to force complete the process

    def __init__(self, html_summary, folder, image, file_number, total_files, start_k):
        # Initialize the "Review" window
        super().__init__()
        self.setWindowTitle(f"Review - {folder} ({file_number}/{total_files})")
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        self.resize(screen_geometry.width(), screen_geometry.height())
        layout = QHBoxLayout(self)

        # Initialize variables locally
        self.folder = folder
        self.image = image
        self.start_k = start_k
        self.values = [0.0 for _ in range(7)]

        # Initialize the HTML Viewer
        web_view = QWebEngineView()
        web_view.page().settings().setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        web_view.page().settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)

        # Load HTML from a local file path
        if os.path.exists(html_summary):
            file_url = QUrl.fromLocalFile(html_summary)
            web_view.load(file_url)
        else:
            print("File does not exist:", html_summary)  # Additional debug info

        # Add the HTML viewer to the layout
        layout.addWidget(web_view)

        # Add the menu to the layout
        self.setup_right_column()

    # Set up the right column with the menu
    def setup_right_column(self):
        right_column = QVBoxLayout()  # Initialize the layout

        submit_button = QPushButton("Skip")
        submit_button.clicked.connect(lambda: self.skip_image())
        right_column.addWidget(submit_button)

        increase_k_button = QPushButton("Increase k")
        increase_k_button.clicked.connect(lambda: self.handle_increase_k(self.start_k))
        right_column.addWidget(increase_k_button)

        self.best_clusters_input = QLineEdit()
        self.best_clusters_input.setPlaceholderText("Best cluster")
        right_column.addWidget(self.best_clusters_input)
        self.best_clusters_input.returnPressed.connect(
            lambda: self.submit_and_close(self.folder, self.image, self.start_k))

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(lambda: self.submit_and_close(self.folder, self.image, self.start_k))
        right_column.addWidget(submit_button)

        submit_button = QPushButton("Force Complete")
        submit_button.clicked.connect(lambda: self.force())
        right_column.addWidget(submit_button)

        self.layout().addLayout(right_column)

    def handle_increase_k(self, start_k):
        new_start_k = start_k + 1  # Increment k
        self.increase_k_and_repeat.emit(new_start_k)  # Emit the custom signal with the new k value
        self.close()

    def skip_image(self):
        self.skip_image_and_add_one.emit()  # Emit the signal to skip the image and add another
        self.close()

    def force(self):
        self.force_complete.emit()  # Emit the signal to force complete the process
        self.close()

    def submit_and_close(self, folder, image, start_k):
        best_cluster = self.best_clusters_input.text()
        self.values = pfc_func.get_cluster_info(best_cluster, start_k)
        self.closed.emit(self.values)  # Emit the signal when the window is about to close
        self.close()


# "Collect Data" Window
class CollectDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Collect Data')
        self.resize(800, 400)
        self.layout = QHBoxLayout(self)

        self.list_widget = QListWidget()
        self.populate_list('AppData/Values')
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        self.layout.addWidget(self.list_widget)

        self.setup_right_column()

        back_button = QPushButton('Back')
        back_button.clicked.connect(self.close)
        self.layout.addWidget(back_button, alignment=Qt.AlignTop | Qt.AlignRight)

    def setup_right_column(self):
        right_column = QVBoxLayout()

        refresh_button = QPushButton("Refresh List")
        refresh_button.clicked.connect(self.refresh_list)  # Connect to a new method
        right_column.addWidget(refresh_button)

        self.collect_all_checkbox = QCheckBox("Do all species in list?")
        right_column.addWidget(self.collect_all_checkbox)

        collect_data_button = QPushButton("Collect Data")
        collect_data_button.clicked.connect(self.collect_data)
        right_column.addWidget(collect_data_button)

        self.status_label = QLabel("Ready")
        self.status_label.setWordWrap(True)  # Enable word-wrapping
        self.status_label.setTextFormat(Qt.RichText)  # Set the text format to rich text
        right_column.addWidget(self.status_label)

        self.layout.addLayout(right_column)

    def populate_list(self, directory):
        try:
            for file_name in os.listdir(directory):
                self.list_widget.addItem(file_name)
        except FileNotFoundError:
            QMessageBox.warning(self, "Directory Not Found", f"Could not find directory: {directory}")

    def refresh_list(self):
        self.list_widget.clear()  # Clear the existing list
        self.populate_list('AppData/Values')  # Repopulate the list

    def collect_data(self):
        collect_all = self.collect_all_checkbox.isChecked()
        if collect_all:
            selected_files = os.listdir('AppData/Values')  # Get all files in the directory
        else:
            selected_files = [item.text() for item in self.list_widget.selectedItems()]  # Collect all selected items

        current_text = self.status_label.text()
        new_text = f"<br>Processing {len(selected_files)} files - this may take a while!"
        self.status_label.setText(current_text + new_text)

        for file in selected_files:
            csv_file_path = rf'AppData/Values/{file}'

            # Initialize an empty list to store the second row data
            row_data = []

            # Open the CSV file and read its contents
            with open(csv_file_path, mode='r') as csv_file:
                csv_reader = csv.reader(csv_file)
                for row_num, row in enumerate(csv_reader, start=1):
                    if row_num == 2:  # Check if it's the second row
                        row_data = row
                        break

            # Convert the items of the second row into a list of numbers
            values = [float(item) for item in row_data]

            # define upper and lower bounds and k
            lower_bound = list(map(int, values[:3]))
            upper_bound = list(map(int, values[3:6]))
            k = int(values[6])

            # Read data from a CSV file and stores it into a dataframe
            # Like the destination, an "r" should be added in front path
            # This may be either an absolute path (recommended for beginners) or a relative path, depending on how the file is saved
            # Note: most of the time, no further arguments are required. Sometimes, though, there will be encoding issues
            # The most common fix is to add an argument, "encoding", using either:
            # encoding = 'utf-8'
            # encoding = 'latin1',
            # encoding = 'iso-8859-1',
            # encoding = 'cp1252'
            df = pd.read_csv(rf"AppData/Output/{file}")

            # All that code above supports these final lines
            # This creates a new column in the dataframe called "KMeansData"
            # This assumes there is already a column in the dataframe called "path" which has the path to the image
            # In the image_summary() function, the first argument is always x, because in this case, x will take
            # the value of the path to the image
            # The second argument is k for K-Means clustering
            # The third and fourth arguments are the lower and upper bound for HSV values, already defined in other variables
            # NOTE: Depending on the size of the data set and the number k selected, this may take some time to complete
            # In smaller datasets with a low k, this may take 30 minutes to an hour
            # For larger datasets with larger k, this may run overnight or longer
            df["KMeansData"] = df["path"].apply(lambda x: pfc_utils.image_summary_processor(x, k, lower_bound, upper_bound))

            # Finally, the code is saved to a csv file locally
            # Use just a file name to save it in the same directory
            # Use an absolute path to save it to some other location in the system
            df.to_csv(rf"AppData/Output/{file}")

            current_text = self.status_label.text()
            new_text = f"<br>Species {file} complete!"
            self.status_label.setText(current_text + new_text)


# "Process Data" Window
class ProcessDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Process Data (Work in Progress)')
        self.resize(800, 400)
        self.layout = QVBoxLayout(self)

        back_button = QPushButton('Back')
        back_button.clicked.connect(self.close)
        self.layout.addWidget(back_button, alignment=Qt.AlignTop | Qt.AlignRight)
