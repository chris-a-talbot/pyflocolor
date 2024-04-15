from bs4 import BeautifulSoup

# imports the URL library, which helps download images from websites
import urllib.request

# imports the pandas library, which stores data into spreadsheet-like objects
import pandas as pd

# imports the os library, which is used to work with directories
import os

import pyflocolor_utils as pfc_utils


def setup_directories():
    directories = ['AppData/Images', 'AppData/Occurrences', 'AppData/Values', 'AppData/Output', 'AppData/Summary']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def download_images(occurrence_lists, image_num=100, re_download=False):
    if not occurrence_lists:
        return None
    else:
        file_num = 0
        for occurrences in occurrence_lists:
            occurrence_df = pd.read_csv(rf"AppData/Occurrences/{occurrences}")
            species_name = os.path.splitext(occurrences)[0]
            os.makedirs(r"AppData/Images/" + species_name, exist_ok=True)
            dest = rf"AppData/Images/{species_name}/"
            # This for loop iterates through every image url in the dataframe and downloads it locally to the destination
            if len(occurrence_df.index) >= image_num:
                length = image_num
            else:
                length = len(occurrence_df.index)

            for i in range(0, length):
                # The "try" tells the program to attempt the below code. If it fails for whatever reason, it moves to the
                # "except"
                if os.path.exists(dest + str(occurrence_df['id'][i]) + '.jpg') and not re_download:
                    continue
                try:
                    # A single line to invisibly visit the image url and download it to the preselected destination
                    # Note 1: that it is assumed that the dataframe as a column labeled "image_url" and "id"
                    # Note 2: Images are saved under their id as a jpg
                    urllib.request.urlretrieve(occurrence_df['image_url'][i], dest + str(occurrence_df['id'][i]) + '.jpg')
                # If the code fails, "continue" is called so that the program continues to run. This means if there is an error,
                # (e.g. url is no longer available, incorrect url, bad internet connection, etc.) the loop moves to the next
                # item and the image is not downloaded
                except:
                    continue

                # This is a really rough progress bar. Essentially, whenever an image downloads, a line will print telling how
                # many images have been downloaded so far out of the total. For example, if 20 images download out of 40 total,
                # the line will read "20/40"
                print("File " + str(file_num+1) + "/" + str(len(occurrence_lists)) + ": image " + str(i + 1) + "/" + str(length))
            file_num += 1


# takes a path and number of clusters k and creates an html file with the summary statistics and sample color
# Note that a html file is the basic bare-bones component to a static website. This provides a useful frame work
# for displaying data and information in an organized way. If running this on Jupyter Notebooks, the web browswer
# will be open anyway and will open a new tab to render the html file
def get_summary_visual(path, k):
    # Get the photo data
    summary = pfc_utils.image_summary_visualizer(path, k)

    path = path.replace("\\", "/")

    # write the start of the html file
    start = """
<!DOCTYPE html>

<html>

    <body>
    """

    # start the body of the html as a blank
    body = f"""
    <div><b>Instructions</b>: <br/>
    Please review <b>all groups</b> before selecting the best ones! <br/>
    Select the groups which most fully represent the <b>flower petals</b> without background imagery. <br/>
    Enter the best groups as a <b>comma separated list</b>, e.g.: 1,5,9</div> <br/>
    <div><b>Alternative commands</b>: <br/>
    <b>X</b>: If the original image has <b>no flowers</b>, <b>has over- or under-saturated</b> flowers, or has <b>very 
    small flowers</b>, enter "X". <br/>
    <b>+</b>: If the flowers are <b>not separating from the background</b> into a group, increase the group number by 
    entering "+". <br/>
    <b>-</b>: If the flowers are <b>separating into too many groups</b>, try to decrease the group number by entering 
    "-", or enter all relevant groups. <br/>
    <b>E</b>: If you're seeing the <b>same images repeatedly</b> and believe this species is complete, enter "E" 
    to move on.</div> <br/>
    <div><b>Original Image</b></div>
    <img src = "file:///{path}">
    <br>
    """

    # For each entry in the summary (ie, that colors dictionary from the image_summary() function),
    # add the details to the html file
    for key in summary:
        # The hsv values stored in a nice variable
        hsv_cluster = summary[key]

        # Convert the hsv values into RGB values
        rgb_cluster = pfc_utils.hsv_to_rgb(hsv_cluster)

        # Concat the body of the html and use f-strings to "fill in blanks" for key summary statistics
        body = body + rf"""      
        <p>{key}</P>
        <p>Average H: {hsv_cluster[0]}</p>
        <p>Average S: {hsv_cluster[1]}</P>
        <p>Average V: {hsv_cluster[2]}</p>
        <div style ="background-color:rgb({rgb_cluster[0]},{rgb_cluster[1]},{rgb_cluster[2]});height: 
        50px;width: 50px;" ></div>
        <img src = "file:///image_cluster_{key[8:]}.jpg">
        <br>
        """

    # Write a closing
    end = """
    </body>
</html>
    """

    # Right now, all the components to the HTML file are in separate varaibles
    # Concat all the elements together into a single, cohesive html document
    html = start + body + end

    # write the html locally
    with open("image_summary.html", 'w') as file:
        file.write(html)

    # Get the working directory, so the user doesn't have to manually configure the path to the file
    cwd = os.getcwd()

    # Get the absolute path
    path = cwd + "\\" + "image_summary.html"

    return path


def get_cluster_info(cluster_id, k):
    output = [None for _ in range(7)]

    with open('image_summary.html', 'r') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    cluster_section = soup.find_all('p', string=lambda text: f'cluster {cluster_id}' in text.lower())

    if cluster_section:
        siblings = cluster_section[0].find_next_siblings('p')
        average_h = average_s = average_v = "N/A"  # Default values

        for sibling in siblings:
            text = sibling.get_text()
            if text.lower().startswith('cluster'):
                break
            if text.startswith('Average H:'):
                average_h = float(text.split(': ')[1])
                if not output[0]:
                    output[0] = average_h
                else:
                    output[0] = min(output[0], average_h)
                if not output[3]:
                    output[3] = average_h
                else:
                    output[3] = max(output[3], average_h)
            elif text.startswith('Average S:'):
                average_s = float(text.split(': ')[1])
                if not output[1]:
                    output[1] = average_s
                else:
                    output[1] = min(output[1], average_s)
                if not output[4]:
                    output[4] = average_s
                else:
                    output[4] = max(output[4], average_s)
            elif text.startswith('Average V:'):
                average_v = float(text.split(': ')[1])
                if not output[2]:
                    output[2] = average_v
                else:
                    output[2] = min(output[2], average_v)
                if not output[5]:
                    output[5] = average_v
                else:
                    output[5] = max(output[5], average_v)

    output[6] = k
    return output
