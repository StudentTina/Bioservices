# -*- coding: utf-8 -*-
"""
Created on Thu May 01 20:57:44 2018

@author: Tina Lai
"""
#TARGETS Quiz Instrutions
#Based on the KEGG  id ("br:br08329") generate a list of target genes and their pathways.

from bioservices import KEGG
from bioservices import easyXML
import re
import numpy as np
import os

k = KEGG(verbose="False")
k_id = k.get("br:br08329") #This pulls up the KEGG brite id file

#To parse through the file, I will create a easy xml file
e=easyXML(k_id, 'utf=8')
# The drug IDs are tagged with "<a" so I will use e soup find children to parse out lines tagged with "<a"
results = e.soup.findChildren("a")

#This is using the regular expression findall to find the drug IDS, however it pulls all drug ids mentioned in lines tagged with "a", even redundant drug ID tags.
all_drug_ids= re.findall(r"(D\d{5})", str(results))

#I will use numpy to parse out unique drug ids from the list.

#First I need to convert the list into an array
array = np.array(all_drug_ids)
#then using numpy's unique function, find unique genes.
unique_drug_ids = np.unique(array)

#Each drug in brite id file: "br:br08329" has it's own unique drug id, target genes, and target pathways
#This first step is to pull out each drug id file using k.get and write it into a directory for parsing

os.makedirs('/Users/harrison/Desktop/Treenut/Bioservices/DrugIDs',exist_ok=True)
path = '/Users/harrison/Desktop/Treenut/Bioservices/DrugIDs'

for x in unique_drug_ids:
    k_drug_id=k.get(x) #The first step is to pull out each drug id file using k.get
    with open(os.path.join(path,x+".txt"), "w") as file1: # I used the with statement because it automatically closes the files written
        file1.write(k_drug_id) #this writes one Drug ID KEGG file one text file labeled with the DRUG ID into a directory I created called DrugIDs

#I opened a new file to write a report witht the drug ID, target gene, and target pathway
file2 = open("/Users/harrison/Desktop/Treenut/Bioservices/DrugIDs/Report.txt", "w")

#Then I want to read the files using a for loop to parse for the target genes and pathways
for x in unique_drug_ids:
    with open(os.path.join(path,x+".txt"),'r') as file3: # This loop allows us to read each new drug ID file
        file2.write(x+'\t')
        genes = re.findall(r'^(TARGET)      (.*)$', file3.read(), flags=re.M) #using re I pull for the lines that match TARGET, which will give us genes the drug targets
        DrugTarget_genes = dict(genes)
        file2.write(str(DrugTarget_genes)+'\t') #This writes it into the report
        Pathways = re.findall('^(  PATHWAY)   (.*)$', file3.read(), flags=re.M) #using re I pull for the lines that match PATHWAY, which will give us the pathways the drug targets
        #This code only allows the first pathway to be parsed. I couldn't figure out how to get all of them. I think it involves changing the flag to re.S so that the newlines are read as special characters.
        DrugTarget_pathways = dict(Pathways)
        file2.write(str(DrugTarget_pathways) + '\n') # This writes it into the report

file2.close()


"""
file3 = open(os.path.join(path,x+".txt"),'r')
Pathways = (re.findall("[^ ]\(.*\)*$", file3.read(), flags=re.M))
#using re I pull for the lines that match PATHWAY, which will give us the pathways the drug targets
Pathways2 = []
for pw in Pathways:
    file3 = open(os.path.join(path,x+".txt"),'r')
    for line in file3:
        if pw in line:
            Pathways2.append(line)
Pathways2
"""


