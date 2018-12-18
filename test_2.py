# -*- coding: utf-8 -*-
from gensim import corpora, models, similarities
import logging
from collections import defaultdict
import xlrd
from xlrd.sheet import ctype_text
import unicodedata
import sys
import json
question = sys.argv[1]
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

workbook = xlrd.open_workbook('mashup.xlsx')                 #查看所有sheet
booksheet = workbook.sheet_by_index(0)

#booksheet = workbook.sheet_by_name('Sheet 1')  #或用名称取sheet
#读单元格数据
cell_11 = booksheet.cell_value(0,0)
cell_21 = booksheet.cell_value(1,0)
#读一行数据
row_3 = booksheet.cell_value(2,3)
#unicodedata.normalize('NFKD', title).encode('ascii','ignore')
print(row_3)

num_cols = booksheet.ncols
num_rows = booksheet.nrows
print num_cols,num_rows
documents = []
apis = []
for i in range(1,num_rows):
	documents.append(booksheet.cell_value(i,6))
	apis.append(booksheet.cell_value(i,3))

#1.分词，去除停用词
stoplist=set('for a of the and to in'.split())
texts=[[word for word in document.lower().split() if word not in stoplist] for document in documents]
#print('-----------1----------')

#2.计算词频
frequency = defaultdict(int) #构建一个字典对象
#遍历分词后的结果集，计算每个词出现的频率
for text in texts:
	for token in text:
		frequency[token]+=1
#选择频率大于1的词
texts=[[token for token in text if frequency[token]>1] for text in texts]
#print('-----------2----------')

#3.创建字典（单词与编号之间的映射）
dictionary=corpora.Dictionary(texts)

#print('-----------3----------')

#4.将要比较的文档转换为向量（词袋表示方法）
#要比较的文档
#new_doc = "I want to go travel in America, need to check the weather and map. And I need some music when travel"
new_doc = question
#将文档分词并使用doc2bow方法对每个不同单词的词频进行了统计，并将单词转换为其编号，然后以稀疏向量的形式返回结果
new_vec = dictionary.doc2bow(new_doc.lower().split())
print('-----------4----------')

#5.建立语料库
#将每一篇文档转换为向量
corpus = [dictionary.doc2bow(text) for text in texts]
print('-----------5----------')

#6.初始化模型
# 初始化一个tfidf模型,可以用它来转换向量（词袋整数计数）表示方法为新的表示方法（Tfidf 实数权重）
tfidf = models.TfidfModel(corpus)
#测试
tfidf.save('mymodel')
tfidf = models.TfidfModel.load('mymodel')
#test_doc_bow = [(0, 1), (1, 1)]
#print('-----------6----------')
#print(tfidf[test_doc_bow])

#print('-----------7----------')
#将整个语料库转为tfidf表示方法
corpus_tfidf = tfidf[corpus]


#7.创建索引
index = similarities.MatrixSimilarity(corpus_tfidf)

#print('-----------8----------')
#8.相似度计算
new_vec_tfidf=tfidf[new_vec]#将要比较文档转换为tfidf表示方法
#print(new_vec_tfidf)
#print('-----------9----------')
#计算要比较的文档与语料库中每篇文档的相似度
sims = index[new_vec_tfidf]
#print(sims)
service = {}
for i in range(len(sims)):
	if sims[i]>0.2:
		line = apis[i].split(", ")
		for s in line:
			if len(s) == 0:
				continue
			if service.has_key(s):
				service[s]+=1
			else:
				service[s] = 1
for key, value in service.items():
	print key, value
result = sorted(service.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
print result

ind = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r"]
#ind = ["1","2","3","4","5","6","7","8","9","10","11","12","13"]
dict = {}
index = 0
for i in result:
	dict[ind[index]] = i[0]
	print i[0]
	index+=1

with open('test.json','w') as f:
    json.dump(dict, f)
f.close()
