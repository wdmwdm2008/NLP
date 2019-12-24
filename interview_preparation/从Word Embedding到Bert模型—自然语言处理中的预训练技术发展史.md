**https://mp.weixin.qq.com/s?__biz=MjM5ODkzMzMwMQ==&mid=2650408679&idx=1&sn=1e10bf19e59729bedd7407b7e1aa4db1&chksm=becd80bd89ba09ab748973b10ee30c4b0a87b7649de37394abc02de3b061a5853753ae7374c4&scene=21#wechat_redirect**
## 图像领域的预训练
- 为什么预训练是可行的?  
    在CNN中不同层级的神经元学习到不同类型的图像特征，由底向上特征形成层级结构。最底层学习到的是线段等特征，第二层学习到人脸五官的轮廓，第三层学习到的
    是人脸的轮廓。越往上抽取出特征越与手头上的人物相关。尤其是底层的网络参数抽取出特征跟具体任务越无关，越具备任务的通用性，所以这是为何一般用底层
    预训练好的参数初始化新任务网络参数的原因。
- 怎么进行预训练?  
    我们有两种方法：一是frozen。即冻结底层参数，只用少数数据训练顶层网络的参数。二是fine-tuning: 用少数数据训练所有的参数，预训练的参数作为初始化参数。
- 预训练的好处:  
    - 能使用少量数据来训练model
    - 即使手头任务训练数据也不少，加个预训练过程也能极大加快任务训练的收敛速度，

## 语言模型和word2vec
$$ \begin{equation} \begin{split} P(w_1,...,w_t) = \prod_{i=1}^{t}P(w_i|w_1,...,w_{i-1}) = \prod_{i=1}^{t}P(w_i|Context) \ P(w_1, w_2, …, w_t) 
= P(w_1) \times P(w_2 | w_1) \times P(w_3 | w_1, w_2) \times … \times P(w_t | w_1, w_2, …, w_{t-1}) \end{split} \end{equation} $$$

- NNLM(Neural Network Language Model)和word2vec的区别 (Glove也被用于word embedding训练)：
    - NNLM训练方法是输入一个单词的上文来预测这个单词。
    - word2vec训练方法是CBOW和SKIP-GRAM
- 为什么他们训练方法不同？  
    因为NNLM主要任务是学习一个解决语言模型任务网络结构，而word embedding是其的一个副产品。而word2vec主要任务就是word embedding。所以可以随意训练。

- wordEmbedding为什么效果不是特别好？  
    - wordEmbedding能找出语义相近的其他词汇。（相似词）  但是不能解决多义词问题。比如Bank(有河岸，银行两种意思), word2vec对bank进行编码时是不能区
    分这个含义的。因为尽管他们的上下文环境中的单词不同，但是上下文句子经过word2vec编码，都是预测相同的单词bank，而同一个单词占用同一行的参数空间，所
    以其不能区分多义词。
    
## From Word2vec to ELMO(Embedding From Language Model)
提出ELMO的论文题目：“Deep contextualized word representation”更能体现其精髓。   
word2vec训练好的word embedding是静态方式。  
ELMO的本质思想是：我事先用语言模型学好一个单词的Word Embedding，此时多义词无法区分，不过这没关系。在我实际使用Word Embedding的时候，单词已经具备了特
定的上下文了，这个时候我可以根据上下文单词的语义去调整单词的Word Embedding表示，这样经过调整后的Word Embedding更能表达在这个上下文中的具体含义，自然
也就解决了多义词的问题了。所以ELMO本身是个根据当前上下文对Word Embedding动态调整的思路。  
     
   
   
    
    
    
    
    
    
    
    
    
    
