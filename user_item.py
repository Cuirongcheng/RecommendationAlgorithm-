#coding:utf-8
#基于内容的协同过滤算法：根据用户的观看记录向用户进行相关推荐
import numpy as np
import pandas as pd
#相识度矩阵的计算
def similarity(data):
	"""计算矩阵中任意两行之间的相似度
	imput:data(mat) :任意矩阵
	output:w(mat)  :任意两行之间的相似度"""
	m=np.shape(data)[0]   #用户的数量
	#初始化相似度矩阵
	w=np.mat(np.zeros((m,m)))
	for i in xrange(m):
		for j in xrange(i,m):
			if j!=i:
				#计算任意两行之间的相似度
				w[i,j]=cos_sim(data[i,],data[j,])
				w[j,i]=w[i,j]
			else:
				w[i,j]=0
	return w

#导入用户-商品数据
def load_data(file_path):
	"""导入用户-商品数据
	   input: file_path: 数据文件的路径
	   output: data(mat):用户商品数据"""
	f=open(file_path)
	data=[]
	
	for line in f.readlines():
		lines=line.strip().split(",")
		tmp=[]
		for x in lines:
			if x!="\t":
				tmp.append(float(x))  #直接存储用户对商品的打分
			else:
				tmp.append(0)
		data.append(tmp)
	f.close()
	return np.mat(data)

			
def item_based_recommend(data, w, user):
    '''基于商品相似度为用户user推荐商品
    input:  data(mat):商品用户矩阵
            w(mat):商品与商品之间的相似性
            user(int):用户的编号
    output: predict(list):推荐列表
    '''
    m, n = np.shape(data) # m:商品数量 n:用户数量
    interaction = data[:,user].T # 用户user的互动商品信息
    
    # 1、找到用户user没有互动的商品
    not_inter = []
    for i in xrange(n):
        if interaction[0, i] == 0: # 用户user未打分项
            not_inter.append(i)
            
    # 2、对没有互动过的商品进行预测
    predict = {}
    for x in not_inter:
        item = np.copy(interaction) # 获取用户user对商品的互动信息
        for j in xrange(m): # 对每一个商品
            if item[0, j] != 0: # 利用互动过的商品预测
                if x not in predict:
                    predict[x] = w[x, j] * item[0, j]
                else:
                    predict[x] = predict[x] + w[x, j] * item[0, j]
    # 按照预测的大小从大到小排序
    return sorted(predict.items(), key=lambda d:d[1], reverse=True)

def top_k(predict, k):
    '''为用户推荐前k个商品
    input:  predict(list):排好序的商品列表
            k(int):推荐的商品个数
    output: top_recom(list):top_k个商品
    '''
    top_recom = []
    len_result = len(predict)
    if k >= len_result:
        top_recom = predict
    else:
        for i in xrange(k):
            top_recom.append(predict[i])
    return top_recom
def cos_sim(x, y):
    '''余弦相似性
    input:  x(mat):以行向量的形式存储，可以是用户或者商品
            y(mat):以行向量的形式存储，可以是用户或者商品
    output: x和y之间的余弦相似度
    '''
    numerator = x * y.T  # x和y之间的额内积
    denominator = np.sqrt(x * x.T) * np.sqrt(y * y.T) 
    return (numerator / denominator)[0, 0]

if __name__ == "__main__":
    # 1、导入用户商品数据
    print "------------ 1. load data ------------"
    file_path="data1/user_item_values.txt"
    data = load_data(file_path)
    # 将用户商品矩阵转置成商品用户矩阵
    data = data.T

    # 2、计算商品之间的相似性
    print "------------ 2. calculate similarity between items -------------"    
    w = similarity(data)
    # 3、利用用户之间的相似性进行预测评分
    print "------------ 3. predict ------------" 
    lenth=data.shape[0]
    num=input("请输入产品编号(0-"+str(lenth)+"):")
    predict = item_based_recommend(data, w, num)
    print predict
    # 4、进行Top-K推荐
    print "------------ 4. top_k recommendation ------------"
    item_num=input("请输入推荐产品的个数:")
    top_recom = top_k(predict, item_num)
    print top_recom
