# 生成式对话seq2seq:从rnn到transformer
** https://mp.weixin.qq.com/s/qUxPgsgP-4XFmVMMzLH5Ow **

---

## 1.工业上的做法: 
普遍是基础模板(例如aiml) + IR闲聊库(例如小黄鸡语料QA) + 爬虫 (百度，搜狗) + 知识图谱(wiki百科) + 对话生成模型  
** aiml: **  网上很多，效果很智障。  
** IR闲聊库: ** 方法有BM25，TFIDF， 编辑距离等等.  
** 爬虫: ** QA-Snake(https://github.com/SnakeHacker/QA-Snake)  
** 图谱: **  
- NER，获取需要的实体词，具体可以分为非监督的实现（模板，词典），监督的实现（lstm+crf，crf）。
- 将得到的实体词，送入图谱检索到可能三元组集合。
- 将三元组集合的属性和问句进行打分（其实就是做一个2分类），选出合适的三元组。
