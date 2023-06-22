import os
import random
import csv
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


def generate_set_data(images_path):
    #generate a list of set for exemple : set data = [1,1,2,4,8,16,32,....] based on power of 2
    number_of_images = len(os.listdir(images_path))
    result = []
    power = 0
    num = 2 ** power
    # to set the first element to 1
    result.append(1)
    while num < number_of_images:
        result.append(num)
        power += 1
        num = 2 ** power
    return result



# create  folders based on the nomber of set len(Set_data())

def Creation_of_folders(image_path,output_folder,Set_data):
    folder_index = 0
    start_index = 0
    
    folder_image_dic = []   # Will contain a tuple of (image, folder_index)
    os.makedirs(output_folder, exist_ok=True)
    image_files = os.listdir(image_path)
    random.shuffle(image_files)
    
    for count in range (len(Set_data) -1) :
        image_f = os.path.join(output_folder, f'img_set_{folder_index+1}')
        os.makedirs(image_f, exist_ok=True)
        label_f = os.path.join(output_folder, f'msk_set_{folder_index+1}')
        os.makedirs(label_f, exist_ok=True)
        end_index = start_index + Set_data[count]
        selected_elements = image_files[start_index:end_index]
        folder_image_dic.extend([(image, folder_index+1) for image in selected_elements])
        start_index = end_index
        folder_index += 1

    return folder_image_dic



def generate_csv_file(folder_image_dic, nom_du_csv_file ,Set_data):
    csv_file = nom_du_csv_file +'.csv'
    with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Image', 'Folder'])
            writer.writerows(folder_image_dic)

    df4 = pd.read_csv(csv_file)
    folder_x= []

    for i in range(0, len(Set_data)-1):
            
            folder_name = 'folder_' + str(i) 
            folder = np.array(df4[df4['Folder'] <= i+1].iloc[:, 0]).tolist()
            globals()[folder_name] = folder
            folder_x.append(folder)
    return folder_x
           

def copy_file_to_set(folder_x,image_path, label_path,output_folder):
    folder_index = 0
    for folder in folder_x:
        for i in range(len(folder)):
            file_name = folder[i]
            source_path = os.path.join(image_path, file_name)
            destination_path.
             = os.path.join(output_folder, f'img_set_{folder_index+1}', file_name)
            shutil.copy(source_path, destination_path)
            label_source_path = os.path.join(label_path, file_name)
            if os.path.isfile(label_source_path):
                    label_destination_path = output_folder + f'msk_set_{folder_index+1}' 
                    shutil.copy(label_source_path, label_destination_path)
                    #print(f"Image '{file_name}' copied successfully.")
            else:
                    print(f"Image '{file_name}' not found in the source folder.")
        folder_index += 1


def Generate_fold_csv(image_path,label_path,output_folder):
    Set_data = generate_set_data(image_path)
    #print(Set_data )
    folder_image_dic=Creation_of_folders(image_path,output_folder,Set_data)
    folder_x = generate_csv_file(folder_image_dic, 'NEW_csv_file' ,Set_data)
    copy_file_to_set(folder_x,image_path, label_path,output_folder)
    print("CSV file was generated successfully , files are copied to folders ......")


if __name__=='__main__':
    parser = argparse.ArgumentParser(description="csv_generate.")
    parser.add_argument("-i", "--image_path", type=str, default=None,
        help="The path to the raw data (images)")
    parser.add_argument("-l", "--labels_path", type=str,
        help="The path to the raw data (labels)")
    parser.add_argument("-o", "--output_path", type=str,
        help="The path to output folder " )

    args = parser.parse_args()
  
    Generate_fold_csv(args.image_path,args.labels_path,args.output_path)
   
   

















 
