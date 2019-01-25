# -*- coding: utf-8 -*-
"""
@author: raymond.kwok

This converts XMLs output by labelImg to a csv.

The XML contains single instance of the following: 
    folder, filename, path, source, size, segment,
but multiple objects depending on the number of labels.

The produced csv will have one row for each object's 
    xmin,ymin,xmax,ymax,class_name
and the same filename for all rows. 
"""
import xml.etree.ElementTree as ET
import os

def xml2csv(xmlInput, csvOutput):
    colHeader = 'filename,xmin,ymin,xmax,ymax,class_name'
    tree = ET.parse(xmlInput)
    root = tree.getroot()
    
    filename = root.find('filename').text
    particle = [','.join([ filename,
                           obj.find('bndbox').find('xmin').text,
                           obj.find('bndbox').find('ymin').text,
                           obj.find('bndbox').find('xmax').text,
                           obj.find('bndbox').find('ymax').text,
                           obj.find('name').text]) for obj in root.iter('object')]
    
    with open(csvOutput, 'w') as f:
#        f.write(colHeader+'\n')
        f.write('\n'.join(particle))

    return '\n'.join(particle)

def batchxml2csv(xmlInDir, recursive = True, summary_path =''):
    '''
    it converts through all xml files under xmlInDir and its sub-dirctories 
    if recursive is True, otherwise, it only converts those under xmlInDir.
    The csv file are in the same directory as the xml file.
    '''
    tmp = ''
    for root, dirs, files in os.walk(xmlInDir):
        for file in files:
            if file[-4:] == '.xml':
                tmp += xml2csv( os.path.join(root, file), os.path.join(root, os.path.splitext(file)[0] + '.csv')) + '\n'
        if not recursive:
            break
    if summary_path != '':
        with open(summary_path, 'w') as f:
            f.write(tmp)
        
#batchxml2csv('/home/raymondkwok/data/cloudchamber/V_20190114_183508_OC0', recursive = True, summary_path = '/home/raymondkwok/data/cloudchamber/V_20190114_183508_OC0/summary.csv' )
