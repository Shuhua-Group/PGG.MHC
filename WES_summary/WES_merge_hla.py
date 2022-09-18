#!/usr/bin/env python
# @coding: utf-8 --
# @Time : 12/29/20
# @Author  :masen
# @Contact :masen2019@sibs.ac.cn
import numpy as np
from collections import Counter
from random import choice
import os 
work_file_dir=os.path.dirname(__file__) 
type_to_call=["A","B","C","DQA1","DQB1","DRB1","DPA1","DPB1"]


def make_a_list(change_list):
    c=[]
    for i in change_list:
        if isinstance(i,list):
            c.extend(i)
        else:
            c.append(i)
    return c
    #None results mean no type
def check_none(alist):
    for i in alist:
        if i :
            return True
    return False
def count_final_list(final_part):
    if not check_none(final_part):
        return ()
    c=Counter(final_part).most_common(2)[0][1]
    try :
        d=Counter(final_part).most_common(2)[1][1]
    except:
        d=0
    if c !=d:
        fina=Counter(final_part).most_common(1)[0][0]
    else:
        fina=choice([item[0] for item in Counter(final_part).items() if item[1]==Counter(final_part).most_common(1)[0][1]])
    return fina


def sort_list_str(w):
    for i in w:
        if isinstance(i,list):
            return i[0]
        else:
            return i

#get dict_answer
dict_answers_to_match={}#resules_dict
part_dict_answers_to_match=[]
with open(work_file_dir+"/hlahd_summary.txt")as f:
    for i in f.readlines():
        id=i.rstrip().split("\t")[0]
        part_dict_answers_to_match.append(id)
with open(work_file_dir+"/optitype_summary.txt")as f:
    for i in f.readlines():
        id=i.rstrip().split("\t")[0]
        part_dict_answers_to_match.append(id)
part_dict_answers_to_match=list(set(part_dict_answers_to_match))

#####
def retcy_to_2(str):
    if str and len(str.split(":")[:]) > 2:
        str_2 = ":".join(str.split(":")[:2])
        return "".join(str_2.split("*")[1:])
    else:
        return "".join(str.split("*")[1:])
def get_hla(file, str_type):
    dict_type = {}
    with open(file)as f:
        for i in f.readlines():
            id, *args = i.rstrip().split("\t")[:]
            if id and args:
                alist = []
                for j in args:
                    if j.startswith("%s*" % str_type):
                        if not ";" in j and not "/" in j:
                            alist.append(retcy_to_2(j))
                        elif ";" in j:
                            part_c=j.split(";")
                            c=[retcy_to_2(i) for i in part_c]
                            if len(c)>1:
                                alist.append(sorted(set(c)))
                        elif "/" in j:
                            part_c=j.split("/")
                            c=[retcy_to_2(i) for i in part_c]
                            alist.append(sorted(set(c)))
            elif id and not args:
                alist=([],[])
            if len (alist)>1 and alist !=([],[]):
                dict_type[id] = sorted(alist,key=lambda x:sort_list_str(x))
            else:
                dict_type[id] =([],[])
    return dict_type
#####
fina1={}
fina2={}
for type in type_to_call:
    dict_1 = get_hla(work_file_dir+"/optitype_summary.txt",type)
    dict_2 = get_hla(work_file_dir+"/polysolver_summary.txt",type)
    dict_3 = get_hla(work_file_dir+"/phlat_summary.txt",type)
    dict_4 = get_hla(work_file_dir+"/hlahd_summary.txt",type)
    dict_6 = get_hla(work_file_dir+"/hla_genotype_summary.txt",type)
    for sample in part_dict_answers_to_match:
        result1 = [dict_1[sample][0],dict_2[sample][0],dict_4[sample][0]]
        result2 = [dict_1[sample][1],dict_2[sample][1],dict_4[sample][1]]
        result_dict1=[count_final_list(make_a_list(result1)),count_final_list(make_a_list(result2))]
        fina1[sample,type]=[type+"*"+i for i in result_dict1 if i]
    for sample in part_dict_answers_to_match:
        result3 = [dict_3[sample][0],dict_4[sample][0],dict_6[sample][0]]
        result4 = [dict_3[sample][1],dict_4[sample][1],dict_6[sample][1]]
        result_dict2=[count_final_list(make_a_list(result3)),count_final_list(make_a_list(result4))]
        fina2[sample,type]=[type+"*"+i for i in result_dict2 if i]
def turn_none_to_kong(alsit):
    if not alsit:
        final =["None","None"]
    else:
        final=["None" if not i else i  for i  in alsit]
    return final
out=open(work_file_dir+"/V2_merge_results.txt","wt")
#out.write("ID\tHLA-A_1\tHLA-A_2\tHLA-B_1\tHLA-B_2\tHLA-C_1\tHLA-C_2\tHLA-DQA1_1\tHLA-DQA1_2\tHLA-DQB1_1\tHLA-DQB1_2\tHLA-DRB1_1\tHLA-DRB1_2\tHLA-DPA1_1\tHLA-DPA1_2\tHLA-DPB1_1\tHLA-DPB1_2\n")
for k in sorted(part_dict_answers_to_match):
    samplesa=k
    try :
        print(k, "\t".join(turn_none_to_kong(fina1[samplesa, "A"])), "\t".join(turn_none_to_kong(fina1[samplesa, "B"])), "\t".join(turn_none_to_kong(fina1[samplesa, "C"])),"\t".join(turn_none_to_kong(fina2[samplesa,"DQA1"])), "\t".join(turn_none_to_kong(fina2[samplesa,"DQB1"])), "\t".join(turn_none_to_kong(fina2[samplesa,"DRB1"])),"\t".join(turn_none_to_kong(fina2[samplesa,"DPA1"])), "\t".join(turn_none_to_kong(fina2[samplesa,"DPB1"])), sep="\t", file=out)
    except:
        print(k)

out.close()

