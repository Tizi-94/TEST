import os
import random
import csv
import shutil
import argparse
import pandas as pd
from os.path import join
import numpy as np
import matplotlib.pyplot as plt
from shutil import copyfile


parser = argparse.ArgumentParser(description="csv_generate.")
parser.add_argument("-i", "--images_path", type=str, default="single",
    help="The path to the raw data (images)")
parser.add_argument("-l", "--labels_path", type=str,
    help="The path to the raw data (labels)")
parser.add_argument("-o", "--output_path", type=str,
    help="The path to output folder " )

args = parser.parse_args()
args = vars(args)





# path des dossier qui contient les images
#image_path = '/home/tabde/notebooks/nucleus/train/img/'
#label_path = '/home/tabde/notebooks/nucleus/train/msk/'
# dossier de destination ou on va créee les dossier pour chaque set 
#output_folder = '/home/tabde/notebooks/TEST_CSV/'

image_files = os.listdir(image_path)
random.shuffle(image_files)

#liste des set des images 
Set_data = [1, 1, 2, 4, 8, 16, 33]

os.makedirs(output_folder, exist_ok=True)

folder_image_dic = []
folder_index = 0
images_folder = []
label_folder = []
for count in Set_data:
    #création des dossiers
    image_f = os.path.join(output_folder, f'img_set_{folder_index+1}')
    os.makedirs(image_f, exist_ok=True)
    label_f = os.path.join(output_folder, f'msk_set_{folder_index+1}')
    os.makedirs(label_f, exist_ok=True)

    #Selection aléatoires des images pour chaque set 
    selected_images = random.sample(image_files, count)

    images_folder.extend(selected_images)
    #liste pour génerer le csv file 
    folder_image_dic.extend([(image, folder_index+1) for image in selected_images])

    for file_name in images_folder:
        img_source_path = image_path + file_name
        img_destination_path = output_folder + f'img_set_{folder_index+1}' +'/'+ file_name
        shutil.copy(img_source_path, img_destination_path)

        label_source_path = os.path.join(label_path, file_name)

        if os.path.isfile(label_source_path):
            label_destination_path = output_folder + f'msk_set_{folder_index+1}' 
            shutil.copy2(label_source_path, label_destination_path)
            print(f"Image '{file_name}' copied successfully.")
        else:
            print(f"Image '{file_name}' not found in the source folder.")

    folder_index += 1

csv_file = 'image_id.csv'

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Image', 'Folder'])
    writer.writerows(folder_image_dic)




