"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2021/8/12 10:07
# @Author  : DuXin
# @FileName: IdentifyKeyClass.py
# @Software: PyCharm
# @content:
===========================
"""
import csv
import pandas as pd
import numpy as np
import os
import natsort

class COSPA:
    def __init__(self,DataSetFile):
        self.DataSetFile = DataSetFile
    def Preprocess_DatasetFile(self,configfile):
        """
        :return: The Direction of all Systems
        """
        Folder_DataSetFile = os.path.join('data', self.DataSetFile)
        conf_file = open(configfile)
        lines = conf_file.readlines()
        AllFileDirection = []
        for each_line in lines:
            records = each_line.strip('\n').split(",")
            for filename in records:
                FileDirection = os.path.join(Folder_DataSetFile, filename)
                AllFileDirection.append(FileDirection)
        return AllFileDirection

    def Normalize(self,AllFileDirection: list,datafilename):
        '''
        :param
        :return: The value of the method under six different systems
                ClassId_a_index_list[1] expresses a-index's value when it applied in argouml system
        '''
        ClassId_Name_list = list()
        ClassName_Key_list = list()
        ClassId_a_index_list = list()
        ClassId_inDeg_list = list()
        ClassId_outDeg_list = list()
        ClassId_allDeg_list = list()
        ClassId_ForwardBackPageRank_Sora_list = list()
        ClassId_g_core_list = list()
        ClassId_g_core_Right_list = list()
        ClassId_h_index_list = list()
        ClassId_k_core_list = list()
        ClassId_OSE_list = list()

        for EachFileDirection in AllFileDirection:
            FileDirection = os.path.join(EachFileDirection, datafilename)
            ClassId_Name = dict()
            ClassName_Key_dict = dict()
            ClassId_a_index_dict = dict()
            ClassId_inDeg_dict = dict()
            ClassId_outDeg_dict = dict()
            ClassId_allDeg_dict = dict()
            ClassId_ForwardBackPageRank_Sora_dict = dict()
            ClassId_g_core_dict = dict()
            ClassId_g_core_Right_dict = dict()
            ClassId_h_index_dict = dict()
            ClassId_k_core_dict = dict()
            ClassId_OSE_dict = dict()

            with open(FileDirection, 'r') as f:
                lines = f.readlines()[1:]
                for line in lines:
                    ClassId_Name[line.split(',')[0]] = line.split(',')[1]
                    ClassName_Key_dict[line.split(',')[1]] = line.split(',')[-4]
                    ClassId_a_index_dict[line.split(',')[0]] = float(line.split(',')[2])
                    ClassId_inDeg_dict[line.split(',')[0]] = float(line.split(',')[3])
                    ClassId_outDeg_dict[line.split(',')[0]] = float(line.split(',')[4])
                    ClassId_allDeg_dict[line.split(',')[0]] = float(line.split(',')[5])
                    ClassId_ForwardBackPageRank_Sora_dict[line.split(',')[0]] = float(line.split(',')[9])
                    ClassId_g_core_dict[line.split(',')[0]] = float(line.split(',')[13])
                    ClassId_g_core_Right_dict[line.split(',')[0]] = float(line.split(',')[14])
                    ClassId_h_index_dict[line.split(',')[0]] = float(line.split(',')[15])
                    ClassId_k_core_dict[line.split(',')[0]] = float(line.split(',')[16])
                    ClassId_OSE_dict[line.split(',')[0]] = float(line.strip().split(',')[23])

                for key in ClassName_Key_dict.keys():
                    if ClassName_Key_dict[key] != '1':
                        ClassName_Key_dict[key] = str(0)
                ClassId_Name_list.append(ClassId_Name)
                ClassName_Key_list.append(ClassName_Key_dict)
                ClassId_a_index_list.append(ClassId_a_index_dict)
                ClassId_inDeg_list.append(ClassId_inDeg_dict)
                ClassId_outDeg_list.append(ClassId_outDeg_dict)
                ClassId_allDeg_list.append(ClassId_allDeg_dict)
                ClassId_ForwardBackPageRank_Sora_list.append(ClassId_ForwardBackPageRank_Sora_dict)
                ClassId_g_core_list.append(ClassId_g_core_dict)
                ClassId_g_core_Right_list.append(ClassId_g_core_Right_dict)
                ClassId_h_index_list.append(ClassId_h_index_dict)
                ClassId_k_core_list.append(ClassId_k_core_dict)
                ClassId_OSE_list.append(ClassId_OSE_dict)
        return ClassId_Name_list, ClassName_Key_list, ClassId_a_index_list, ClassId_inDeg_list, ClassId_outDeg_list, ClassId_allDeg_list, \
               ClassId_ForwardBackPageRank_Sora_list, ClassId_g_core_list, ClassId_h_index_list, ClassId_k_core_list, \
               ClassId_OSE_list, ClassId_g_core_Right_list

    def FolderDatalist(self,configfile):
        folder_datalist = list()
        DataSetFile = [self.DataSetFile]
        conf_file = open(configfile)
        lines = conf_file.readlines()
        for datasetfile in DataSetFile:
            for line in lines:
                for package in line.split(','):
                    folder_datalist.append(datasetfile + '/' + package)
        return folder_datalist

    def ReadIndex(self, AllFileDirection: list, num: int) -> dict:
        """

        :param AllFileDirection:
        :param num:
        :return: n-layer structure：
                         1. Systems under different weighting methods
                         2. Serial number of the a-index, InDeg and OSE permutations
                         3. Various methods
        """
        print("AllFileDirection", AllFileDirection)
        Methods = ['a_index_list', 'inDeg_list', 'outDeg_list', 'allDeg_list', 'ForwardBackPageRank_Sora_list',
                   'g_core_list', 'h_index_list', 'k_core_list', 'OSE_list']
        ChooseCombine = [('a_index_list', 'inDeg_list', 'OSE_list')]
        ClassInfo = list()
        AllFileDict = dict()
        for File in range(len(AllFileDirection)):
            CombineTimes = dict()
            AllFileDict.setdefault(AllFileDirection[File][5:], {})
            ProcessedFile = os.path.join(AllFileDirection[File], 'AllMethodsDataSet.csv')
            if 'csv' == ProcessedFile.split('.')[-1]:
                classId_list = np.loadtxt(ProcessedFile, dtype=str, delimiter=',', skiprows=1, usecols=0)
                className_list = np.loadtxt(ProcessedFile, dtype=str, delimiter=',', skiprows=1, usecols=1)
                a_index_list = np.loadtxt(ProcessedFile, dtype=float, delimiter=',', skiprows=1, usecols=2)
                inDeg_list = np.loadtxt(ProcessedFile, dtype=float, delimiter=',', skiprows=1, usecols=3)
                outDeg_list = np.loadtxt(ProcessedFile, dtype=float, delimiter=',', skiprows=1, usecols=4)
                allDeg_list = np.loadtxt(ProcessedFile, dtype=float, delimiter=',', skiprows=1, usecols=5)
                ForwardBackPageRank_Sora_list = np.loadtxt(ProcessedFile, dtype=float, delimiter=',', skiprows=1,
                                                           usecols=9)
                g_core_list = np.loadtxt(ProcessedFile, dtype=float, delimiter=',', skiprows=1, usecols=13)
                h_index_list = np.loadtxt(ProcessedFile, dtype=float, delimiter=',', skiprows=1, usecols=15)
                k_core_list = np.loadtxt(ProcessedFile, dtype=float, delimiter=',', skiprows=1, usecols=16)
                OSE_list = np.loadtxt(ProcessedFile, dtype=float, delimiter=',', skiprows=1, usecols=23)

            for CombineNum in range(len(ChooseCombine)):
                CombineTimes.setdefault(CombineNum + 1, {})
                total_list = dict()
                total_list['classId_list'] = classId_list
                total_list['className_list'] = className_list
                for index in ChooseCombine[CombineNum]:
                    total_list[index] = eval(index)
                CombineTimes[CombineNum + 1] = total_list
                AllFileDict[AllFileDirection[File][5:]] = CombineTimes
        return AllFileDict

    def OrderIndex(self, folder_datalist: list, total_list: dict, count: int) -> list:
        """

        :param
        :param
        :return: AllIndexOrder: is a dict where the key is the element in folder_datalist, and the value is the result of sorting by various methods
                 total_list_name: 返回含有方法名
        """
        id_key = dict()
        # ClassId_Name_list[0-35]：是一个列表，存放着类id和类名
        # Name_Key_list[0-35]:是一个列表，存放着类名和是否关键类的标志
        for ClassId_Name_list_key, ClassId_Name_list_value in ClassId_Name_list[count].items():
            id_key[(int(ClassId_Name_list_key))] = int(Name_Key_list[count][ClassId_Name_list_value])
        '''
            下面对类和方法的值进行排序,给定一个序列，当出现相同值的时候根据序列的先后顺序比大小
        '''
        # Sora下5%时各种方法的排名
        index_dict = [(0, 'ClassId_inDeg_list'), (1, 'ClassId_allDeg_list'), (2, 'ClassId_h_index_list'),
                      (3, 'ClassId_OSE_list'), (4, 'ClassId_g_core_list'), (5, 'ClassId_g_core_Right_list'),
                      (6, 'ClassId_allWDeg_list'), (7, 'ClassId_LiuPageRank_list'), (8, 'ClassId_inWDeg_list'),
                      (9, 'ClassId_k_core_list'), (10, 'ClassId_ForwardBackPageRank_Sora_list'),
                      (11, 'ClassId_ForwardPageRank_Sora_list'), (12, 'ClassId_outWDeg_list'),
                      (13, 'ClassId_outDeg_list'), (14, 'ClassId_HITS_auth_list'), (15, 'ClassId_a_index_list')]
        res = [x[1] for x in
               index_dict]  # 所有的方法的相对顺序：['ClassId_inDeg_list', 'ClassId_allDeg_list', 'ClassId_OSE_list', ... ]
        method = list()  # 方法的组合，比如：['ClassId_a_index_list', 'ClassId_inDeg_list']
        for k in list(total_list.keys())[2:]:
            method.append('ClassId' + '_' + k)
        method_order = list()  # method_order表示被选取的方法的序号，以及方法的值
        method_order_list = list()  # method_order_list表示15选n时，被选取的方法的列表，比如15选2时的['inWDeg_list', 'ForwardPageRank_Sora_list']
        for r in range(len(res)):
            if res[r] in method:
                if res[r] == 'ClassId_g_core_list':
                    method_order_list.append(res[r][8:])
                    method_order_list.append(res[r + 1][8:])
                    method_order.append((r, eval(res[r])[count]))
                    method_order.append((r + 1, eval(res[r + 1])[count]))
                else:
                    method_order_list.append(res[r][8:])
                    method_order.append((r, eval(res[r])[count]))
        EachIndexOrder = list()
        total_list_name = list()
        temp_order_dict = dict()
        for key, value in total_list.items():  # key是classId_list等,value是对应的值
            total_list_name.append(key)
            dict_variable_name = key[0:-4] + 'dict'
            dict_variable_name = dict()
            if key == 'classId_list' or key == 'className_list':
                continue
            else:
                for tmp_length in range(len(total_list[key])):
                    dict_variable_name[total_list['classId_list'][tmp_length]] = total_list[key][tmp_length]
                order_variable_name = key[0:-4] + 'order'
                if key == 'g_core_list':
                    order_variable_name = sorted(dict_variable_name.items(), key=lambda item: (
                    float(item[1]), ClassId_g_core_Right_list[count][str(item[0])],
                    [x[1][str(item[0])] for x in method_order]), reverse=True)
                else:
                    order_variable_name = sorted(dict_variable_name.items(), key=lambda item: (
                    float(item[1]), [x[1][str(item[0])] for x in method_order]), reverse=True)
                temp_order_dict[key] = order_variable_name

        # The next part is to eliminate too many classes from the system
        AllIndexOrder = dict()
        del_dict = dict()
        dir = 0
        for order in method_order_list[0:1]:
            if order in list(temp_order_dict.keys()):
                # print(temp_order_dict.keys())
                all_length = len(temp_order_dict[order])
                if all_length > 1000:
                    for del_num in range(all_length - 1000):
                        end_index = len(temp_order_dict[order]) - 1
                        while (id_key[int(temp_order_dict[order][end_index][0])] == 1):
                            end_index -= 1
                        for k, v in temp_order_dict.items():
                            if k != order:
                                for it in v:
                                    if it[0] == temp_order_dict[order][end_index][0]:
                                        temp_order_dict[k].remove(it)
                                        break
                        temp_order_dict[order].pop(end_index)
                break
        if 'g_core_Right_list' in method_order_list:
            method_order_list.remove('g_core_Right_list')
        AllIndexOrder[folder_datalist[count]] = [temp_order_dict[i] for i in method_order_list]
        return AllIndexOrder, method_order_list

    def WriteRank(self, AllIndexOrder: dict, method_order_list: list, iterator_times: list, Combine: int) -> bool:
        value = 0
        root_path = 'OutputResult/'
        for k, v in AllIndexOrder.items():
            print(k)
            # with open(os.path.join(root_path + k.split('/')[1] + '_Result'+'/' + '/'  + 'KeyClasses_Consequence'.format(
            #         iterator_times=iterator_times) + '.txt'), 'w') as f:
            #     for indexname in method_order_list:
            #         f.write(indexname[0:-5])
            #         f.write(": ")
            #         for i in v[value]:
            #             f.write(i[0])
            #             f.write(" ")
            #         f.write("\n")
            #         value += 1

    def KY_Rank(self, combine, RootDirection, choosemethod, Kemeny_Young_Dir):
        if len(combine.split('_')) == 2:
            GoalFile = RootDirection +  '/'  + choosemethod + '/' + combine
            ResultFile = GoalFile[:-4] + '_KY_result.txt'
            Cmd_Statement = '{method} 100 < {inputfile} > {outputfile}'.format(
                method=Kemeny_Young_Dir, inputfile=GoalFile, outputfile=ResultFile)
            os.system(Cmd_Statement)

if __name__ == "__main__":
    RootDirection = 'OutputResult'
    Direction = ['CCN_MethodsValue']
    System = ['ant_main', 'argouml', 'jedit', 'jhotdraw', 'jmeter_core', 'wro4j']
    co = COSPA('CCN_MethodsValue')
    AllFileDirection = co.Preprocess_DatasetFile('data/Subject.conf')
    ClassId_Name_list, Name_Key_list, ClassId_a_index_list, ClassId_inDeg_list, ClassId_outDeg_list, ClassId_allDeg_list, \
    ClassId_ForwardBackPageRank_Sora_list, ClassId_g_core_list, ClassId_h_index_list, ClassId_k_core_list, \
    ClassId_OSE_list, ClassId_g_core_Right_list = co.Normalize(AllFileDirection,'AllMethodsDataSet.csv')
    folder_datalist = co.FolderDatalist('data/Subject.conf')
    Combine = 3
    AllFileDict = co.ReadIndex(AllFileDirection, Combine)
    count = 0
    for weight_mechanism in list(AllFileDict.keys()):
        for iterator_times, methods_value in AllFileDict[weight_mechanism].items():
            AllIndexOrder, method_order_list = co.OrderIndex(folder_datalist, methods_value, count)
            co.WriteRank(AllIndexOrder, method_order_list, iterator_times, Combine)
        count += 1
    print("The following aggregation is performed using the Kemeny-Young method:")
    Kemeny_Young_Dir = 'Kemeny-Young'
    for dir in Direction:
        for choosemethod in natsort.natsorted(os.listdir('OutputResult')):
            for combine in natsort.natsorted(os.listdir(os.path.join(RootDirection,choosemethod))):
                co.KY_Rank(combine,RootDirection,choosemethod,Kemeny_Young_Dir)