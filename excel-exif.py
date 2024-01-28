#!/bin/python

#----------------------------------
# excel-exif.py
#
# Loop through all files in a directory and subdirectoies
# - If the file matches the regex then process as an image file
#
# For each image file extract the specified EXIF data
#
# Write the filenames and exif data to an Excel spreadsheet
#
#----------------------------------

import sys
import os
import re
from PIL import Image
from PIL.ExifTags import TAGS
import pandas as pd

# Print the Exif data to the screen
def printExif(exif):
    
    for tag_id in exif:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exif.get(tag_id)
        # decode bytes 
        if isinstance(data, bytes):
            data = data.decode()
        print(f"{tag:25}: {data}")

# Return the Exif Tag data as a list
# - this will return the data in the list in the order the tags are found
#   in the file not the order it is defined in the original list
#
# (might need to handle if one entry is missing as this will return an shorter list)
def returnExifTags(exif,tags):

    results_tags = []
    results_data = []
    
    for tag_id in exif:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exif.get(tag_id)
        # decode bytes 
        if isinstance(data, bytes):
            data = data.decode()

        # If this is a tag we want then append to return list    
        if tag in tags:
            results_data.append(data)
            results_tags.append(tag)

    return results_tags, results_data
    
def main():

    ################ Variables ################
    dataDir = '/run/media/apr/Data/apr/Photos/Family/Scans/'  # Directory to process
    filename_regex = '\.jpg'                              # Regex of file we want to process
    exif_tags = ['DateTime','GPSInfo']   # List of EXIF tags we want to save to excel file
    excel_filename='test.xlsx'
    ############################################
    
    # Loop through all the files in datDir and subdirectories
    # If they match the regular expression filename_regex then process them    
    print('{}'.format(dataDir))

    nFiles = 0
    filenames = []
    for root, subdirs, files in os.walk(dataDir):
        for file in files:
            filepath = os.path.join(root, file)
            
            if re.search(filename_regex, file):
                #print('Found File: {}'.format(filepath))
                filenames.append(filepath)
                nFiles += 1
                               
    if nFiles == 0:
        print('No files match for regex: {}'.format(filename_regex))
        exit()
    else:
        print('Read {} files'.format(nFiles))

        # Now we need to get the exif data for each file
        files_tags = []
        files_data = []

        for f in filenames:
            print("\n")
            print(f)
            exif = Image.open(f).getexif()
            xmp = Image.open(f).getxmp()
            # TO SEE NAMES OF EXIF tags to populate list - uncomment this line
            #printExif(exif)
            # for key, value in xmp.items() :
            #     print (key, value)
            print(xmp['xmpmeta']['RDF']['Description']['subject']['Bag']['li'])
            #print(xmp)

            # Get the data from the tags in our list
            tags, data = returnExifTags(exif,exif_tags)
            print(tags, data)
            # files_tags.append(tags)
            # files_data.append(data)

        # # Now we fill an excel spreadsheet with the data
        # df = pd.DataFrame(filenames, columns=['Filepath'])

        # # Convert to a hyperlink
        # df['Filepath'] = '=HYPERLINK("' + df['Filepath'] + '", "' + df['Filepath'] + '")'
        
        # for i in range(len(files_data[0])):
        #     print([row[i] for row in files_data])
        #     df.insert((i+1),files_tags[0][i],[row[i] for row in files_data])

        # # Write to file
        # df.to_excel(excel_filename,index=False)
    
if __name__ == '__main__':
    sys.exit(main())
