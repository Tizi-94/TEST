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
#image_path = '/home/tabde/notebooks/nucleus/train/img_out/'
#label_path = '/home/tabde/notebooks/nucleus/train/msk/'
#output_folder = '/home/tabde/notebooks/output_folder/'

image_files = os.listdir(image_path)
random.shuffle(image_files)

#liste des set des images 
Set_data = [1, 1, 2, 4, 8, 16, 33]
os.makedirs(output_folder, exist_ok=True)

csv_file = 'image_label_train.csv'
folder_image_dic = []
folder_index = 0
start_index = 0

for count in Set_data:
    image_f = os.path.join(output_folder, f'img_set_{folder_index+1}')
    os.makedirs(image_f, exist_ok=True)
    label_f = os.path.join(output_folder, f'msk_set_{folder_index+1}')
    os.makedirs(label_f, exist_ok=True)
    end_index = start_index + count
    selected_elements = image_files[start_index:end_index]
    folder_image_dic.extend([(image, folder_index+1) for image in selected_elements])
    start_index = end_index
    folder_index += 1


with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Image', 'Folder'])
        writer.writerows(folder_image_dic)
   
        print(folder_image_dic)


df4 = pd.read_csv('image_label_train.csv')

folder_1 = np.array(df4[df4['Folder']<=1].iloc[:,0]).tolist()
folder_2 = np.array(df4[df4['Folder']<=2].iloc[:,0]).tolist()
folder_3 = np.array(df4[df4['Folder']<=3].iloc[:,0]).tolist()
folder_4 = np.array(df4[df4['Folder']<=4].iloc[:,0]).tolist()
folder_5 = np.array(df4[df4['Folder']<=5].iloc[:,0]).tolist()
folder_6 = np.array(df4[df4['Folder']<=6].iloc[:,0]).tolist()
folder_7 = np.array(df4[df4['Folder']<=7].iloc[:,0]).tolist()
folder_index = 0


folder_x= [folder_1, folder_2, folder_3,folder_4,folder_5,folder_6,folder_7]

for folder in folder_x:
    for i in range(len(folder)):
        file_name = folder[i]
        source_path = os.path.join(image_path, file_name)
        destination_path = os.path.join(output_folder, f'img_set_{folder_index+1}', file_name)
        shutil.copy(source_path, destination_path)
        label_source_path = os.path.join(label_path, file_name)
        if os.path.isfile(label_source_path):
                label_destination_path = output_folder + f'msk_set_{folder_index+1}' 
                shutil.copy(label_source_path, label_destination_path)
                print(f"Image '{file_name}' copied successfully.")
        else:
                print(f"Image '{file_name}' not found in the source folder.")
    folder_index += 1


