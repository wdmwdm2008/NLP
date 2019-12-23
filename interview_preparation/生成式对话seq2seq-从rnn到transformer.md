# 生成式对话seq2seq:从rnn到transformer
**https://mp.weixin.qq.com/s/qUxPgsgP-4XFmVMMzLH5Ow**

---

## 1.工业上的做法: 
普遍是基础模板(例如aiml) + IR闲聊库(例如小黄鸡语料QA) + 爬虫 (百度，搜狗) + 知识图谱(wiki百科) + 对话生成模型  
**aiml:**  网上很多，效果很智障。  
**IR闲聊库:** 方法有BM25，TFIDF， 编辑距离等等.  
**爬虫:** QA-Snake(https://github.com/SnakeHacker/QA-Snake)  
**图谱:**
- NER，获取需要的实体词，具体可以分为非监督的实现（模板，词典），监督的实现（lstm+crf，crf）。
- 将得到的实体词，送入图谱检索到可能三元组集合。
- 将三元组集合的属性和问句进行打分（其实就是做一个2分类），选出合适的三元组。

## 2.Seq2seq:
Tips:
- Attention被引入到seq2seq模型，从而解决原来rnn长序列的long-term问题  
- 使用拥有gate的lstm能避免RNN的梯度消失问题  
- GRU因为使用更少的门，所以模型参数更少，因此效率比lstm好  
## 3.Attention
- Self-attention里面的每个词都要和该句子中的所有词进行attention计算，目的是学习句子内部的词依赖关系，从而捕获句子的内部结构。  
- Multi-head attention中每个head在不同的表示子空间里学习到相关的信息，即feature。  
- scaled dot-product attention中的scaled目的是使内积不至于太大，有利于训练的收敛。  
- self-attention的特点在于无视词之间的距离直接计算依赖关系，能够学习一个句子的内部结构，实现也较为简单并行可以并行计算。  
## 4.Transformer
- 结构上transformer 由decoder和encoder组成，decoder比encoder多了一个multi-head attention.这个multi-head attention 的k，v来自encoder 的输出，q来自前一级的decoder层的输出。  
-- Self-attention计算了词与句子中每个词的关系，但是没有位置关系。所以添加了positional encoding在embedding上。  
-- ADD代表了residual connection,为了解决网络退化问题将前几层的信息传递到这里。  
-- Norm代表了layer normalization,通过对层的归一化，可以加速模型的训练过程，使其更快的收敛。  
-- Multi-head 后面加一个ffn，能增加模型的非线性变换能力。  
## 5.Bert and gpt之后的seq2seq
#### 5.1 Bert的优点和缺点
- Bert的出现使nlp界开始关注预训练+少量数据下游任务调优的开发模型。  
- Bert使用的是transformer的encoder部分。  
- Bert 的embedding由三种embedding求和而成。其中positional encoding 不是由transformer中的三角函数学习而来，而是一个大小为(512, 768)的lookup表  
- Bert比transformer多了segment embedding,因为句子不光做LM任务还要做以两个句子为输入的分类任务。  
- 预训练使用mask LM，就是在训练过程中作者随机mask 15%的token，最终的损失函数只计算被mask掉那个token。  
#### 5.2 Bert的压缩提速和bert and gpt的seq2seq
- 压缩方向：pruning, distill, quantization  
- 主要模型: distillBert (论文：arxiv.org/abs/1910.01108), ALBERT, 和TinyBERT  
    - DistillBert (模型大小减小了40%（66M），推断速度提升了60%，但性能只降低了约3%。)
    - ALBERT(论文：arxiv.org/abs/1909.11942v2 代码：github.com/brightmart/albert_zh)
    - TinyBERT(论文：arxiv.org/abs/1909.10351  代码地址：github.com/brightmart/albert_zh) 
    TinyBERT提出了针对Transformer结构的知识蒸馏和针对pre-training和fine-tuning两阶段的知识蒸馏.
- 微软提出了一个通用预训练模型MASS(代码：论文：arxiv.org/abs/1905.02450，github.com/microsoft/MASS)，采用了联合encoder-attention-decoder的训练框架。
- **Encoder:** 输入为一个被mask掉连续部分token的句子，使用双向transformer对其进行编码。这样处理的目的是更好的捕获没有被mask掉词语信息用于后续decoder的预测。
- **Decoder：** 输入为与encoder同样的句子，但是mask掉的正好和encoder相反（后面试验直接将masked tokens删去保留unmasked tokens position embedding），使用attention机制去训练，但只预测encoder端被mask掉的词。该操作可以迫使decoder预测的时候更依赖于source端的输入而不是前面预测出的token，同时减缓了传统seq2seq结构的exposure bias问题。
## Reference
zhuanlan.zhihu.com/p/53796189

zhuanlan.zhihu.com/p/65062025

blog.csdn.net/qq_32241189/article/details/81591456

fancyerii.github.io/2019/02/14/chatbot/

cnblogs.com/robert-dlut/p/8638283.html

sohu.com/a/42214491_164987

cnblogs.com/hellojamest/p/11128799.html

zhuanlan.zhihu.com/p/85221503

zhuanlan.zhihu.com/p/77307258

blog.csdn.net/qq_38343151/article/details/102993202

zhuanlan.zhihu.com/p/47063917

zhuanlan.zhihu.com/p/47282410

cnblogs.com/jiangxinyang/p/11715678.html

zhuanlan.zhihu.com/p/86900556

blog.csdn.net/u012526436/article/details/101924049

zhuanlan.zhihu.com/p/65346812

zhihu.com/question/324019899/answer/709577373

kexue.fm/archives/6933

zhuanlan.zhihu.com/p/68327602

zhuanlan.zhihu.com/p/70663422

jiqizhixin.com/articles/2019-09-03-14

jiqizhixin.com/articles/2019-08-26-12

zhuanlan.zhihu.com/p/92842331
