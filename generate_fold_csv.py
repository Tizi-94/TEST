"""
---------------------------------------------------------------------------------------------
the script enables the generation of a CSV file based on image data and creation of folders 
to store the image and label data to provide an organized representation of the images for 
training .
----------------------------------------------------------------------------------------------
"""


import os
import random
import shutil
import os
import argparse
import pandas as pd
from os.path import join
import numpy as np
from skimage.io import imread
import SimpleITK as sitk
import matplotlib.pyplot as plt
from shutil import copyfile
import pydoc




def generate_set_data(image_path):
    """function to generate a list of set data based in a number of images in image_path 

    Parameters:

    - image_path (str): The path for training images .
    
    Returns:

    - list : list of set data .
    """
    # Get the number of images in the specified directory
    number_of_images = len(os.listdir(image_path))
    
    # Create an empty list to store the set data
    set_data = []
    
    # Loop until the number of images is greater than or equal to 1
    while number_of_images >= 1:
        # Append the current number of images to the set data list
        set_data.append(number_of_images)
        
        # Divide the number of images by 2 and update the value of number_of_images
        number_of_images = number_of_images // 2
    
    # Return the set data list
    return set_data







def creation_of_folders(image_path, output_path,set_data):
    """function to create folders under the name (img_set_x et msk_set_x ) in output_path 

    Parameters:

    - image_path (str): the path for training images .

    - output_path ( str ): the path to output folder where the folders will be creat

    - set_data (list ) : list of set data 

    Return: returns nothing
    """
    folder_index = 0
    start_index = 0

    # Create the output path if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    # # Generate set data by calling the generate_set_data function 
    # set_data = generate_set_data(image_path)

    # Iterate over the set data
    for count in range(len(set_data)):
        # Create a folder for images
        image_f = os.path.join(output_path, f'img_set_{folder_index+1}')
        os.makedirs(image_f, exist_ok=True)

        # Create a folder for labels
        label_f = os.path.join(output_path, f'msk_set_{folder_index+1}')
        os.makedirs(label_f, exist_ok=True)

        # Increment the folder index
        folder_index += 1
    return







def generate_csv_file(image_path, set_data):
    """function to generate csv file with pandas 

    Parameters:

    - image_path (str): the path for training images .

    Returns:

    - path_to_csv (str): the path where csv file was saved .

    """
    # Name of the CSV file to be generated
    csv_file = 'image_msk_csv_file.csv'

  

    # Reverse the order of set_data elements
    set_data = set_data[::-1]  

    folder_index = 0  
    start_index = 0

    # List to store tuples of (image, folder_index)
    image_folder_index = []  

    # Get the list of image files in the given image path
    image_files = os.listdir(image_path)  

    # Shuffle the image files randomly
    random.shuffle(image_files)  

    # Iterate over the set_data
    for count in set_data:
        # Calculate the end index for selecting elements from image_files
        end_index = start_index + count  

        # Select elements from image_files based on the end index
        selected_elements = image_files[0:end_index]  

        # Add tuples of (image, folder_index) to image_folder_index
        image_folder_index.extend([(image, folder_index+1) for image in selected_elements])  
        folder_index += 1  

    # Create the CSV file with pandas 
    df = pd.DataFrame(image_folder_index, columns=['Image', 'Folder'])
    df.to_csv(csv_file, index=False)

    # Get the current working directory
    current_directory = os.getcwd()  

    # Construct the full path to the CSV file
    path_to_csv = os.path.join(current_directory, csv_file)  
    print(f"The csv file has been successfully generated under the name '{csv_file}'")
    print(f"Your file is saved in the directory: '{path_to_csv}'")

    # Return the path to the generated CSV file
    return path_to_csv  







def copy_files_to_folders(image_path, label_path, output_path, path_to_csv_file,):
    """Copy files (images and labels) from (image_path, label_path) to output_path

    Parameters:

    - image_path (str) : the path to training images .

    - path_to_csv (str) : the path where csv file was saved .

    - label_path (str) : the path to labels .

    - output_path (str): the path to output folder .
    """
    folder_index = 0
    # Read the CSV file using pandas
    df = pd.read_csv(path_to_csv_file)

    # Extract the 'Folder' and 'Image' columns as lists
    liste_of_set = df['Folder'].tolist()
    liste_of_filename = df['Image'].tolist()

    # Determine the number of folders
    number_of_folders = set(liste_of_set)

    # Iterate over the unique folders
    for folder in number_of_folders:
        # Iterate over the elements in the 'liste_of_set'
        for f in range(len(liste_of_set)):
            # Check if the current element matches the folder
            if liste_of_set[f] == folder:
                # Get the filename
                file_name = liste_of_filename[f]  

                # Construct the image source path
                image_source_path = os.path.join(image_path, file_name)  

                # Construct the image destination path
                destination_path = os.path.join(output_path, f'img_set_{folder_index+1}', file_name)  

                # Copy the file from source to destination
                shutil.copy(image_source_path, destination_path)  

                # Construct the label source path
                label_source_path = os.path.join(label_path, file_name)  

                # Check if the label file exists
                if os.path.isfile(label_source_path): 
                    # Construct the label destination path
                    label_destination_path = os.path.join(output_path, f'msk_set_{folder_index+1}')  
                    # Copy the label file to the destination
                    shutil.copy(label_source_path, label_destination_path)  

                else:
                    print(f"Image '{file_name}' not found in the source folder.")
        # Increment the folder index
        folder_index += 1  
    return






if __name__=='__main__':
    parser = argparse.ArgumentParser(description="csv_generate.")
    parser.add_argument("-i", "--image_path", type=str, default=None,
        help="The path to the raw data (images)")
    parser.add_argument("-l", "--label_path", type=str,
        help="The path to the raw data (labels)")
    parser.add_argument("-o", "--output_path", type=str,
        help="The path to output folder " )

    args = parser.parse_args()

    # Create folders based on the provided image and output paths
    creation_of_folders(args.image_path, args.output_path,generate_set_data(args.image_path) )  

    # Copy files to the folders based on the provided paths
    copy_files_to_folders(args.image_path , args.label_path, args.output_path, generate_csv_file(args.image_path, generate_set_data(args.image_path)))     

    #print(generate_csv_file.__doc__)
















 
