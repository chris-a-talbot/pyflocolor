# All the imports from the sklearn module are statistical tools to help perform K-Means Clustering
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans

import numpy as np
import cv2
import pandas as pd


# write a utlity function to determine if a number is in a range. This makes the code less cumbersome later
def is_between(lower, num, upper):
    return lower <= num <= upper


# While averages are used as the default, some utility functions were returned to help with other, more advanced
# summary statistics which may help in some situations the above_nth() and below_nth() functions in particular return
# an array above or below a percentile. This may be helpful when trying to isolate a relatively dark or light part of
# a flower or other feature of interest
# These functions are strictly optional, but may be useful

# A utlity function that returns an array above a pre-defined percentile
# ie, returns all values above the nth percentile, inclusive
def above_nth(np_array, n):
    result = np_array >= np.percentile(np_array, n)

    return np_array[result]


# A utlity function that returns an array above a pre-defined percentile
# ie, returns all values below the nth percentile, inclusive
def below_nth(np_array, n):
    result = np_array <= np.percentile(np_array, n)

    return np_array[result]


# Write a function to return the percent of returned pixels
# The first argument is meant to be an array of pixels within a cluster
# The second and third arguments are the width and height of the image
# The area of the cluster is then returned as a percent of the entire area
def percent_pix(np_array, image_dim_1, image_dim_2):
    total_pixels = image_dim_1 * image_dim_2

    return len(np_array) / total_pixels


def hsv_to_rgb(hsv_vals):
    # round the the values
    h = round(hsv_vals[0], 0)
    s = round(hsv_vals[1], 0)
    v = round(hsv_vals[2], 0)

    # To convert with openCV's rules, a simple one pixel "image" is created
    image = [
        [
            [h, s, v]
        ]
    ]

    # convert to BGR colorspace
    image = cv2.cvtColor(np.uint8(image), cv2.COLOR_HSV2BGR)

    # Get the pixel values in an array
    pixel = image[0][0]

    # Because openCV stores it as a BGR, the reverse is stored in a list and returned for the traditional RGB format
    return [pixel[2], pixel[1], pixel[0]]


# A function that receives an image path and number of clusters k and returns a dictionary of clusters and values
def image_summary_visualizer(image_source, k):
    # Load image
    image = cv2.imread(image_source)

    # Convert image to the HSV color space
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # By default, images are stored as 3D objects with a width and height defined by the image resolution
    # In addition, each pixel stores three pieces of information pertaining to color, in this case, H, S, and V
    # Mathematrical operations on this 3D object is cumbersome and inefficient, so the flatten() method
    # turns it into a 2D array for quicker operations.
    # The first three values in the 2D array correspond with the 3 color values in the top-left pixel
    # The next three values correspond with the 3 color values in next pixel to the right, etc.
    # For example, the data structure of an image typically look like this:
    # [[[1,2,3], [4,5,6]],
    # [[7,8,9], [10,11,12]]
    # The flatten argument transforms it to this:
    # [1,2,3,4,5,6,7,8,9,10,11,12]
    image_flat = image_hsv.flatten()

    # Because of how the image is flatten, we know that the H, S, and V values reoccur at every third pixel
    # at a slight different index i.e. All H values are at the 0th place, 3rd place, 6th place, 9th place and so on
    # We take advantage of this to collect all the H, S, and V values into single variables

    # The h-channel. Takes every 3rd value from flatten image starting at 0th place
    h = image_flat[0::3]
    # The s-channel. Takes every 3rd value from flatten image starting at 1st place
    s = image_flat[1::3]
    # The v-channel. Takes every 3rd value from flatten image starting at 2nd place
    v = image_flat[2::3]

    # Create a dataframe from the pixel values
    df = pd.DataFrame(data=h, columns=["h"])
    df['s'] = s
    df['v'] = v

    # H, S, and V values are at different scales. H values vary from 0-179 and S and V vary from 0-255
    # Consequently, any clustering based on a geometric distance will be skewed
    # To remedy this, the StandScaler() function brings everything onto a standard scale

    # initialize scaler
    scaler = StandardScaler()

    # Scaled features
    scaler.fit(df)
    df_scaled = scaler.transform(df)

    # These two lines actually perform the K-Means clustering. Note that k is the same k passed in the initial argument
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(df_scaled)

    # Create a new column in the dataframe for the labels
    # The labels themselves are simple numeric values that denote which pixels go into which cluster
    # (ie, all pixels labeled as 1 are in the same cluster)
    df["cluster"] = kmeans.labels_

    # create an empty dictionary to store summary values
    colors = {}

    # Iterate through the clusters, calculates the summary stats, and saves a masked image
    for i in range(k):
        # filter the dataframe by cluster
        df_filter = df[df["cluster"] == i]

        # Calculates the summary stats. By default, the average is taken. If these need to change, this is the
        # place to do it. Note that using the numpy library for calulations generally yield faster results
        # The summary states are then stored in the dictionary.
        colors["cluster " + str(i)] = [
            np.mean(df_filter["h"]),
            np.mean(df_filter["s"]),
            np.mean(df_filter["v"])
        ]

        # create a "mask" based on the labels. This is basically the array that will dictate whether or not a pixel
        # will be displayed in the image
        detect = np.array([1 if x == i else 0 for x in kmeans.labels_], dtype='uint8')

        # reshape the mask into the dimensions of the picture
        dims = image_hsv.shape
        detect = detect.reshape(dims[0], dims[1])

        # Create a copy of the image
        image_copy = image_hsv

        # create the masked image
        output = cv2.bitwise_and(image_copy, image_copy, mask=detect)

        # Convert back to rgb for better visualization
        output = cv2.cvtColor(output, cv2.COLOR_HSV2BGR)

        # save the image locally
        cv2.imwrite("image_cluster_" + str(i) + ".jpg", output)

    # Finally return the colors dictionary
    return colors


# Receives an image path and number of clusters k and returns a dictionary of clusters and values
# This function works very similarly to the function of the same name in the Image Summary Visualizer,
# but there's a key difference in how it aggregates clusters within a defined color range
# The image_source argument is a path to the image
# k is the k for K-Means Clustering
# lower_bound is the lower bound of the HSV values
# upper_bound is the upper bound of the HSV values
def image_summary_processor(image_source, k, lower_bound, upper_bound):
    # Load image
    image = cv2.imread(rf"{image_source}")

    try:
        # Very large images take a lot of time to process, so if it has a width of over 1500, the image is resized to
        # @ 1/4th of its original size
        if image.shape[0] > 1500:
            image = cv2.resize(image, (int(image.shape[0] / 4), int(image.shape[1] / 4)))

        # Convert image to HSV
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # By default, images are stored as 3D objects with a width and height defined by the image resolution
        # In addition, each pixel stores three pieces of information pertaining to color, in this case, H, S, and V
        # Mathematrical operations on this 3D object is cumbersome and inefficient, so the flatten() method
        # turns it into a 2D array for quicker operations.
        # The first three values in the 2D array correspond with the 3 color values in the top-left pixel
        # The next three values correspond with the 3 color values in next pixel to the right, etc.
        # For example, the data structure of an image typically look like this:
        # [[[1,2,3], [4,5,6]],
        # [[7,8,9], [10,11,12]]
        # The flatten argument transforms it to this:
        # [1,2,3,4,5,6,7,8,9,10,11,12]
        # Flatten the image for more efficient processing
        image_flat = image_hsv.flatten()

        # Because of how the image is flatten, we know that the H, S, and V values reoccur at every third pixel
        # at a slight different index i.e. All H values are at the 0th place, 3rd place, 6th place, 9th place and so on
        # We take advantage of this to collect all the H, S, and V values into single variables

        # the h-channel. Takes every 3rd value from flatten image starting at 0th place
        h = image_flat[0::3]
        # the s-channel. Takes every 3rd value from flatten image starting at 1st place
        s = image_flat[1::3]
        # the v-channel. Takes every 3rd value from flatten image starting at 2nd place
        v = image_flat[2::3]

        # Create a dataframe from the pixel values
        df = pd.DataFrame(data=h, columns=["h"])
        df['s'] = s
        df['v'] = v

        # H, S, and V values are at different scales. H values vary from 0-179 and S and V vary from 0-255
        # Consequently, any clustering based on a geometric distance will be skewed
        # To remedy this, the StandScaler() function brings everything onto a standard scale

        # initialize scaler
        scaler = StandardScaler()

        # Scaled features
        scaler.fit(df)
        df_scaled = scaler.transform(df)

        # These two lines actually perform the K-Means clustering. Note that k is the same k passed in the initial argument
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(df_scaled)

        # Create a new column in the dataframe for the labels
        # The labels themselves are simple numeric values that denote which pixels go into which cluster
        # (ie, all pixels labeled as 1 are in the same cluster)
        df["cluster"] = kmeans.labels_

        # create an empty dictionary to store summary values
        colors = {}

        # Iterates through the clusters, calculates the summary statistics (if they're in the upper and lower bounds)
        for i in range(k):

            # filter the dataframe by cluster
            df_filter = df[df["cluster"] == i]

            # Find the mean of h
            h_mean = np.mean(df_filter["h"])

            # Find out if h_mean is within range. If not, the loop moves to the next iteration
            # If it does it moves to the next item to calculate. This method should speed up the code
            # because it doesn't need to calculate everything every time. The drawback is that more
            # than a handful of calculations make the code cumbersome/hard to read
            if is_between(lower_bound[0], h_mean, upper_bound[0]):

                # Find the mean of s
                s_mean = np.mean(df_filter["s"])

                # Next comparison
                if is_between(lower_bound[1], s_mean, upper_bound[1]):

                    # Find the mean of v
                    v_mean = np.mean(df_filter["v"])

                    # Next comparison
                    if is_between(lower_bound[2], v_mean, upper_bound[2]):
                        # store ONLY the averages that fit in range in the dictionary
                        # If the values are calculated need to be changed, this is point to do it
                        colors[i] = [h_mean, s_mean, v_mean]

        # Once the summary stats for the clusters are calculated, some additional checks need to be made

        # If there's no clusters in range, then return "no flowers"
        if len(colors) == 0:
            return "no flowers"
        # If there are multiple clusters in range, they need to be combined and their summary stats re-calculated
        else:

            # Create a list of dataframes to combine
            df_combine = [df[df["cluster"] == key] for key in colors.keys()]

            # Concatenate the dataframes into one, bigger, dataframe
            df_result = pd.concat(df_combine)

            # return a list of values
            # if you want to change which measure to evaluate, here's the place to choose. Using Numpy's built-in
            # functions are recommended as they're usually quicker
            result = [
                np.mean(df_result["h"]),
                np.mean(df_result["s"]),
                np.mean(df_result["v"])
            ]

            return result

    except:
        return "An error occured"