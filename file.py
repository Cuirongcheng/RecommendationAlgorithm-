#coding:utf-8

import pandas as pd

file_path="Bdata/附件1：用户收视信息.xlsx"
data1_1=pd.read_excel(file_path,u"用户收视信息",encoding='gbk')
data1_2=pd.read_excel(file_path,u"用户回看信息")
data1_3=pd.read_excel(file_path,u"用户点播信息")
data1_4=pd.read_excel(file_path,u"用户单片点播信息")

data_2=pd.read_csv("Bdata/附件2：电视产品信息.csv",encoding='gbk')
data_3=pd.read_csv("Bdata/附件3：用户基本信息.csv",encoding='gbk')

