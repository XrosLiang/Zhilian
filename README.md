# Zhilian

通过爬取智联招聘网站获取有关python职位的信息。(基于python3.5)

# Spider

爬虫文件，运行后会生成`demand.txt`,`location.txt`,`treatment.txt`,`salary.txt`四个文件用于之后的分析，在运行过程中也会保存到Mongo数据库。

# wordscount

对保存的txt文件分词并统计出现次数。

# wordyun

根据词频统计生成词云。

# 依赖的库有：

- pymongo
- requests
- pyquery
- matplotlib
- wordcloud
- jieba

## 安装依赖

```
pip3 install -r requirements.txt
```
