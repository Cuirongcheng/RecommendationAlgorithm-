#encoding:utf-8
from user_item import load_data,similarity,top_k
import numpy as np
def user_based_recommend(data,w,user):
	"""基于用户相似性为用户use进行推荐
	input:data(mat)  用户商品矩阵
	      w(mat)  用户之间的相似度
	      user(int)  用户的编号
	output:predict(list)  推荐列表
	"""
	m,n=np.shape(data)
	interction=data[user,]  #用户user与商品信息
	#找到用户user没有互动过的商品
	not_inter=[]
	for i in xrange(n):
		if interction[0,i]==0 : #没有互动的商品
			not_inter.append(i)

	#对没有互动过的商品进行预测
	predict={}
	for x in not_inter:
		item=np.copy(data[:,x])  #找到所有用户对商品x的互动信息
		for i in xrange(m):  #对每一个用户
			if x not in predict:
				predict[x]=w[user,i]*item[i,0]
			else: 
				predict[x]=predict[x]+w[user,i]*item[i,0]
	#排序
	return sorted(predict.items(),key=lambda d:d[1],reverse=True)

if __name__ == "__main__":
    # 1、导入用户商品数据
    print "------------ 1. load data ------------"
    file_path="data1/user_item_values.txt"
    data = load_data(file_path)


    # 2、计算商品之间的相似性
    print "------------ 2. calculate similarity between items -------------"    
    w = similarity(data)
    # 3、利用用户之间的相似性进行预测评分
    print "------------ 3. predict ------------" 
    lenth=data.shape[0]
    num=input("请输入用户编号(0-"+str(lenth)+"):")
    predict = user_based_recommend(data, w, num)
    print (predict,"\n")
    # 4、进行Top-K推荐
    print "------------ 4. top_k recommendation ------------"
    item_num=input("请输入推荐相似用户的人数:")
    top_recom = top_k(predict, item_num)
    print top_recom
