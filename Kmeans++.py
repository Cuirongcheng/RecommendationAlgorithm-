#!/usr/bin/python
#encoding:utf-8


import numpy as np
import pandas as pd

from file import data1_3,data1_4,data_2,data_3 

column_names=[u"正题名",u"导演",u"演员",u"出品年代",u"分类名称",u"连续剧分类"]
l=len(column_names)

data=data_2[column_names]
data=data.replace(to_replace='无',value=np.nan)
data=data.dropna(how='any')

#导入train_test_split对数据进行分割
from sklearn.cross_validation import train_test_split
x_train,x_test,y_train,y_test=train_test_split(data[column_names[1:l-1]],data[column_names[l-1]],test_size=0.25,random_state=33)
print "训练样本的类别和数量"
print y_train.value_counts()

print "测试样本的类别和数量"
print y_test.value_counts()


#导入KMeans模型
from sklearn.cluster import KMeans
#初始化，设置聚类中心数量为10
kmeans=KMeans(10, init='k-means++', algorithm='auto' )#full, elkan
kmeans.fit(x_train)
#逐条判断每条数据所属的聚类中心
y_predict=kmeans.predict(x_test)

label_pred = kmeans.labels_ #获取聚类标签
print "聚类标签\n",label_pred
print "聚类标签长度:",len(label_pred)
centroids = kmeans.cluster_centers_ #获取聚类中心
print "聚类中心\n",centroids
inertia = kmeans.inertia_ # 获取聚类准则的总和
print "聚类准则的总和\n",inertia

#使用ARI进行算法的聚类性能评估
from sklearn import metrics
print "ARI进行算法的聚类性能评估:",metrics.adjusted_rand_score(y_test, y_predict)

#模型保存
from sklearn.externals import joblib
joblib.dump(kmeans,  'data1/doc_cluster.pkl')
kmeans = joblib.load('data1/doc_cluster.pkl')
clusters = kmeans.labels_.tolist()



