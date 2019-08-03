import re
from langconv import *
import jieba
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from gensim.models.word2vec import PathLineSentences
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt


def simple2tradition(line):
    # 将简体转换成繁体
    line = Converter('zh-hant').convert(line)
    return line


def tsne_plot(model):
    "Creates and TSNE model and plots it"
    labels = []
    tokens = []
    index = 0;
    for word in model.wv.vocab:
        index = index + 1
        if index > 100:
            break
        tokens.append(model[word])
        labels.append(word)

    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)

    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])

    plt.figure(figsize=(16, 16))
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.annotate(labels[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
    plt.show()


def tradition2simple(line):
    # 将繁体转换成简体
    line = Converter('zh-hans').convert(line)
    return line


def cut(string):
    return list(jieba.cut(string))


def clean_data(string):
    string = re.sub(r'\d+', 'NUM', string)
    return re.findall(r'\w+', string)


if __name__ == '__main__':
    # opening file and cleaning data
    file_index = 10
    index = 0
    with open('C:/study/AI Training and Jobs/NLP_CV_Course/week_4\wikiextractor-master/wdm_wiki_extracted\wiki_00', 'r',
              encoding='UTF-8') as f:
        lines = [''.join(clean_data(line)) for line in f.readlines(1024 * 1024 * 400) if
                 not line.startswith("<doc") and not line.startswith("</doc>") and not len(line.strip()) == 0]
        while lines != []:
            print(1)
            with open(
                    'C:/study/AI Training and Jobs/NLP_CV_Course/week_4\wikiextractor-master/wdm_wiki_extracted\cleaned_wiki_' + str(
                            file_index) + '.txt', 'w', encoding='UTF-8') as g:
                for data_list_line in lines:
                    data_list_line = tradition2simple(data_list_line)
                    index += 1
                    if index % 10000 == 0:
                        print(index)
                    g.write(data_list_line + '\n')
                file_index += 1
            print(2)
            lines = [''.join(clean_data(line)) for line in f.readlines(1024 * 1024 * 400) if
                     not line.startswith("<doc") and not line.startswith("</doc>") and not len(line.strip()) == 0]

    # splitting sentences into multiple vocabulary by using jieba
    filepath = 'C:/study/AI Training and Jobs/NLP_CV_Course/week_4/wikiextractor-master/wdm_wiki_extracted/cleaned_wiki_'
    for i in range(3):
        with open(filepath + str(i) + '.txt', 'r', encoding='UTF-8') as f:
            with open(filepath + str('jieba') + i + '.txt', 'w', encoding='UTF-8') as g:
                for line in f.readlines():
                    tempStrs = ' '.join(cut(line))
                    g.write(tempStrs + "\n")

    # using all files to generate word2vec model
    wiki_news = open('C:/study/AI Training and Jobs/NLP_CV_Course/week_4/wikiextractor-master/wdm_wiki_extracted/cleaned_wiki_jieba.txt', 'r', encoding='utf-8')
    sentences = LineSentence(wiki_news);
    model = Word2Vec(sentences, size=100, min_count=5, window=5, workers=8)
    model.save('./modeled_wiki_2')
    model.wv.save_word2vec_format('./modeled_wiki_txt_2.txt', binary=False)

    # Testing similarity
    print(model.wv.similarity("排序", "香港"))
    print(model.wv.similarity("你", "你们"))
    print(model.wv.similarity("你", "我"))

    # Testing distance between two words
    print(model.wv.distance("爱", "喜欢"))
    print(model.wv.distance("你", "我"))

    # Most similarity vocabulary
    print(model.wv.most_similar("苹果"))
    print(model.wv.most_similar("阿里巴巴"))

    # Visualization
    tsne_plot(model)
