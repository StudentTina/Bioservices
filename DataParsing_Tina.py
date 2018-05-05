# -*- coding: utf-8 -*-
"""
Created on Thu May 01 20:57:44 2018

@author: Tina Lai
"""
"""
TARGETS Quiz Instrutions
Based on the KEGG  id ("br:br08329") generate a list of target genes and their 
pathways. 
"""
from bioservices import KEGG
from bioservices import easyXML
import numpy as np
import re


def Get_Drug_IDs(Brite_ID):
    k=KEGG(verbose="False")
    k_id = k.get(Brite_ID)
    e=easyXML(k_id, 'utf=8')
    results = e.soup.findChildren("a")
    all_drug_ids= re.findall(r"(D\d{5})", str(results))
    array = np.array(all_drug_ids)
    unique_drug_ids = np.unique(array)
    return unique_drug_ids

def TargetGene_and_TargetPathway(Unique_Drug_ID):
    with open("Report.txt","w") as Report:
        Report.write('Drug ID'+'\t'+'Target Gene'+'\t'+'Drug Pathway'+'\t')
        for x in Unique_Drug_ID:
            Report.write('\n'+x+'\t')
            a = k.get(x)
            dic = k.parse(a)
            if 'TARGET' in dic.keys():
                Target_and_Pathway = dic['TARGET']
                Target = re.findall('\S.*]$',Target_and_Pathway, flags=re.M)
                Report.write(str(Target)+'\t')
                Pathway = re.findall('hsa.*',Target_and_Pathway) 
                Report.write(str(Pathway)+'\t')
            else: 
                Report.write('NONE'+'\t'+'NONE'+'\t')
    return print('DONE!')
                


TargetGene_and_TargetPathway(Get_Drug_IDs("br:br08329"))
            
