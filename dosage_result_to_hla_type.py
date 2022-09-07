#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@time        :2021/10/22 15:58:25
@Author      :masen
@Mail        :masen2019@sibs.ac.cn   
'''
import os 
import pandas as pd
import argparse
from collections import Counter
parser = argparse.ArgumentParser()

parser.add_argument('-d','--dosage', required=True, help='dosage results\n\n')
parser.add_argument('-o','--out', required=True, help='output dir\n\n')
parser.add_argument('-f','--fam',required=True ,help='fam file\n\n')
args = parser.parse_args()

out_file_dir=args.out
dosage_file=args.dosage
fam=args.fam
df =pd.read_csv(dosage_file,sep="\t")
list_id=[]
with open(fam)as f:
    for i in f.readlines():
        id=i.rstrip().split(" ")[0]
        list_id.append(id)
#####
def remove_file(file):
    if os.path.getsize(file) <1:
        os.remove(file)

###
def change_2nd_type(str):# HLA_C_03, HLA_C_0304
    hla_type=str.split("_")[1]
    sub_type=str.split("_")[2]
    if len(sub_type)==2:
        return
        #return hla_type+'*'+sub_type
    elif len(sub_type)>=4:
        return hla_type+'*'+sub_type[:2]+":"+sub_type[2:]
def change_1st_type(str):# HLA_C_03, HLA_C_0304
    hla_type=str.split("_")[1]
    sub_type=str.split("_")[2]
    if len(sub_type)==2:
        return hla_type+'*'+sub_type
    """
    elif len(sub_type)>=4:
        return hla_type+'*'+sub_type[:2]+":"+sub_type[2:]
    """
def return_original_dosage_results(num_count,id,df):
    dict={}
    for k in num_count:
        dict[k]=df.loc[df['type']==k,id].values
    return dict
def return_remove_list(counter_dict):
    remove =[]
    for k,n in dict(counter_dict).items():
            if n >2:
                remove.append(k)
    return remove
col1=["type","P","A"]+list_id
df.columns=col1
df1=df[df["type"].str.startswith("HLA_")].round(0)
df1=df1.set_index("type")
out_1field=open(out_file_dir+"/hla_type_results_1_field.txt","wt")
out_2field=open(out_file_dir+"/hla_type_results_2_field.txt","wt")
out_1field_need_to_check_by_self=open(out_file_dir+"/need_to_check_by_yourself_hla_type_results_1_field.txt","wt")
out_2field_need_to_check_by_self=open(out_file_dir+"/need_to_check_by_yourself_hla_type_results_2_field.txt","wt")
for id in list_id:
    type_1=df1[df1[id]==1][id].index.tolist()
    type_2=df1[df1[id]==2][id].index.tolist()
    one_field_type1_and_2=[i for i in type_1 if len(i.split("_")[2])==2]+[i for i in type_2 if len(i.split("_")[2])==2]*2
    two_field_type1_and_2=[i for i in type_1 if len(i.split("_")[2])==4]+[i for i in type_2 if len(i.split("_")[2])==4]*2

    one_field_num_count=Counter([i.split("_")[1] for i in one_field_type1_and_2 ])
    one_field_more_than_one_results=[i for i in one_field_num_count if one_field_num_count.most_common()[0][1]>2]
    two_field_num_count=Counter([i.split("_")[1] for i in two_field_type1_and_2 ])
    two_field_more_than_one_results=[i for i in two_field_num_count if two_field_num_count.most_common()[0][1]>2]

    one_field_results=sorted([change_1st_type(i) for i in one_field_type1_and_2 if i])
    two_field_results=sorted([change_2nd_type(i) for i in two_field_type1_and_2 if i])
    if not one_field_num_count.most_common()[0][1]>2:
        print(id,"\t".join(one_field_results),sep="\t",file=out_1field)
    elif one_field_num_count.most_common()[0][1]>2:
        print(id,"\t".join([i for i in one_field_results if i.split("*")[0] not in return_remove_list(one_field_num_count)]),sep="\t",file=out_1field)
        print(id,"\t".join(one_field_results),sep="\t",file=out_1field_need_to_check_by_self)
        print(id,return_original_dosage_results(one_field_type1_and_2,id,df),sep="\t",file=out_1field_need_to_check_by_self)
    if not two_field_num_count.most_common()[0][1]>2:
        print(id,"\t".join(two_field_results),sep="\t",file=out_2field)
    elif two_field_num_count.most_common()[0][1]>2:
        print(id,"\t".join([i for i in two_field_results if i.split("*")[0] not in return_remove_list(two_field_num_count)]),sep="\t",file=out_2field)
        print(id,"\t".join(two_field_results),sep="\t",file=out_2field_need_to_check_by_self)
        print(id,return_original_dosage_results(two_field_type1_and_2,id,df),sep="\t",file=out_2field_need_to_check_by_self)
out_1field.close()
out_2field.close()
out_1field_need_to_check_by_self.close()
out_2field_need_to_check_by_self.close()
remove_file(out_file_dir+"/need_to_check_by_yourself_hla_type_results_1_field.txt")
remove_file(out_file_dir+"/need_to_check_by_yourself_hla_type_results_2_field.txt")