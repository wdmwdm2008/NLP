from gensim.models import Word2Vec
import jieba
import numpy as np
import os
import pandas as pd
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser
from pyltp import NamedEntityRecognizer


class Extraction():

    def __init__(self, cws_model_path: str,
                 pos_model_path: str,
                 ner_model_path: str,
                 parser_model_path: str,
                 spoken_words: str,
                 word2vec):
        self.spoken_words = spoken_words
        self.truncate_index = 8

        self.segmentor = Segmentor()
        self.postagger = Postagger()
        self.ner = NamedEntityRecognizer()
        self.parser = Parser()

        self.segmentor.load(str(cws_model_path))
        self.postagger.load(str(pos_model_path))
        self.ner.load(str(ner_model_path))
        self.parser.load(str(parser_model_path))
        self.word2vec = Word2Vec.load(word2vec)

    def release(self):
        self.segmentor.release()
        self.postagger.release()
        self.ner.release()
        self.parser.release()


    def get_next_sentence(self, news, index):
        stop1 = news[index + 1:].find("。")
        stop2 = news[index + 1:].find("!")
        stop3 = news[index + 1:].find("?")
        stop_list = [stop for stop in [stop1, stop2, stop3] if stop != -1]
        if stop_list is None:
            False

        stop = min(stop_list)
        return news[index:index + stop + 2], index + stop + 2


    def cut(self, string):
        return " ".join(jieba.cut(string))


    def sentence_distance(self, sentence1, sentence2):
        word_list1 = self.cut(sentence1)
        word_list2 = self.cut(sentence2)

        vec_1 = 0
        vec_2 = 0
        ### get representation of sentence 1
        for i in range(len(word_list1)):
            if word_list1[i] in self.word2vec.wv.vocab:
                vec_1 += self.word2vec.wv[word_list1[i]]

        ### get representation of sentence 2
        for i in range(len(word_list2)):
            if word_list2[i] in self.word2vec.wv.vocab:
                vec_2 += self.word2vec.wv[word_list2[i]]

        return np.dot(vec_1, vec_2) / (np.linalg.norm(vec_1) * np.linalg.norm(vec_2))


    def get_sentence(self, news, word_list, idx, postag_list, sub_id):
        # 取得 说的内容 及SBV的宾语成分
        # idx 为表示说的词在新闻中的位置信息
        index = len("".join(word_list[:idx + 1]))
        sub_index = len("".join(word_list[:sub_id]))

        if news[index] == "。" or news[index] == "!" or news[index] == "?":
            stop1 = news[:index].rfind("。")
            stop2 = news[:index].rfind("!")
            stop3 = news[:index].rfind("?")
            # 检查是不是后面没有句子了
            stop_list = [stop for stop in [stop1, stop2, stop3] if stop != -1]
            if len(stop_list) == 0:
                stop = 0
            else:
                stop = max(stop_list) + 1

            begin = float("inf")
            end = float("inf")
            if "“" in news[:index] and "”" in news[:index]:
                begin = news[:index].rfind("“")
                end = news[:index].rfind("”")
            # 第一种情况 双引号在stop前面，表示说词后面跟的是双引号的句子 则双引号里的内容即为说的内容
            if sub_index - end < self.truncate_index:
                result = news[begin + 1:end]
            else:
                result = news[stop:sub_index]
            # print(result)
        else:
            stop1 = news[index:].find("。")
            stop2 = news[index:].find("!")
            stop3 = news[index:].find("?")
            # 检查是不是后面没有句子了
            stop_list = [stop for stop in [stop1, stop2, stop3] if stop != -1]
            if len(stop_list) == 0:
                return False
            # 返回后面的第一个句子
            stop = min(stop_list)
            sentence = news[index:stop + index + 1]
            if postag_list[idx + 1] == 'wp':
                sentence = sentence[1:]
            if postag_list[idx + 2] == 'wp':
                sentence = sentence[1:]
            result = sentence
            sim = 1
            next_id = stop + index + 2
            # 检查第二个句子是否也是说的内容，通过检查句子相似性来判断 若是相似度大于某个数值则表示 相近 这个句子也是说的内容
            # 如果相似度大于0.7表示 该句话和前一句内容相似 所以这句话 也为说的内容 继续检查下一句话
            while sim > 0.85 and next_id <= len(news):
                next_sentence_id = next_id
                if next_sentence_id <= len(news):
                    next_sentence, next_id = self.get_next_sentence(news, next_sentence_id)
                    sim = self.sentence_distance(sentence, next_sentence)
                if sim > 0.85:
                    result += next_sentence
                    sentence = next_sentence
        return result


    def get_sub_and_view(self, idxs, news, word_list, postag_list):
        sub = []
        speech = []
        for sub_id, spoken_id in idxs:
            sub.append(word_list[sub_id])
            speech.append(self.get_sentence(news, word_list, spoken_id, postag_list, sub_id))
        return sub, speech

    def find_spoken_word_id_and_sub(self, spoken_words,word_list, ner_list, parser_list):
        #取得 新闻中 包含SBV关系 并且V表示的是说的意思 的主语和谓语的位置
        id_list = []
        for sub_id,parse_relation in enumerate(parser_list):
            index,relation = parse_relation
            if  relation == "SBV" and (ner_list[sub_id] == "S-Nh" or ner_list[sub_id] == "S-Ni" or ner_list[sub_id] == "S-Ns"):
                spoken_word = word_list[index-1]
                if spoken_word in spoken_words:
                    word_id = index-1
                    id_list.append((sub_id,word_id))
        return id_list


    def newsExtraction(self, news):
        word_list = list(self.segmentor.segment(news))
        postag_list = list(self.postagger.postag(word_list))
        ner_list = list(self.ner.recognize(word_list, postag_list))
        arcs = self.parser.parse(word_list, postag_list)
        parser_list = [(arc.head, arc.relation) for arc in arcs]

        idx=self.find_spoken_word_id_and_sub(self.spoken_words,word_list, ner_list, parser_list)
        # print(idx)
        sub, speech = self.get_sub_and_view(idx, news, word_list, postag_list)
        # for i in range(len(sub)):
        #     print(sub[i], speech[i])
        return sub, speech


if __name__ =='__main__':

    new_contents = "'原标题：叙利亚被“袭机”事件惹怒俄罗斯 警告将瞄准美战机\r\n海外网6月19日电 当地时间6月19日，俄罗斯国防部对美国军方击落叙利亚飞机一事作出反击，宣布停止执行俄美两国签署的“在叙飞行安全备忘录”，并称以后美国领导的国际联军所有的战机，都是俄罗斯军方监控与瞄准的目标，叙利亚局势进一步复杂化。\r\n据纽约时报消息，由于美国军方今日击落了一架叙利亚军机，俄罗斯国防部发布消息，自6月19日起暂停执行俄美间在叙利亚领空“防止空中事件和保障行动期间飞行安全”的相互谅解备忘录。要求美方指挥部对此事件进行彻查，结果与俄方共享。\r\n公告称：“俄空军在叙利亚领空执行任务的地区里，幼发拉底河西岸发现的任何飞行物，包括美国领导的国际联军的飞机和无人机，都将是俄罗斯军方地面和空中防空武器监控与瞄准的目标。”\r\n据叙利亚军方声明，当地时间6月19日，一架政府军机正前往拉卡（Raqqa）市，准备对盘踞于此的IS武装分子进行打击，却突然遭到美军袭击，飞行员至今失踪。声明称：“这次袭击发生的时机，是在叙利亚政府及其盟国的军队在与IS恐怖分子的战斗中获得优势的情况下发生的，本来这些恐怖分子已经在叙利亚的沙漠中节节败退。”\r\n此次“袭机”事件“惹怒”了俄罗斯，俄罗斯参议院国防委员会副主席弗朗茨·克莱琴谢夫（Frants Klintsevich）称美军的行动是“挑衅行为”，实际上是对叙利亚的“军事侵略”。\r\n该部门认为，美军“故意不履行双方2015年签署的“安全备忘录”中规定的义务，因此宣布暂停与美军在该框架下的合作。据报道，该协议一直是美俄两国军队协调在该地区的军事活动的关键。俄罗斯、美国、叙利亚、土耳其等国家在叙利亚的诉求经常是相冲突的，该协议就在其中起到调和作用。在特朗普四月下令袭击叙利亚空军之后，俄方表示将暂停协议，不过几个星期之后又重启，这次时隔两月后再被中断。\r\n俄罗斯外长拉夫罗夫在回应记者时也表示，“涉及到叙利亚地面所发生的事情，毫无疑问，我们认为有必要尊重叙利亚的主权和领土完整，这是联合国2254号决议和其他文件规定的。因此，任何地面行动，包括实施军事行动的参与方，需得到大马士革的许可。”（编译/海外网 杨佳）\r\n'"
    # new_contents = pd.Series([new_contents])
    # new_contents.fillna("", inplace=True)
    # news = new_contents[89579]
    news = new_contents.replace('\u3000','')
    news = news.replace(' ','')

    with open('../utils/say_words.txt', 'r') as f:
        lines = f.read().splitlines()

    word2vec_path = '../utils/model/newsWithCount5_split5'
    file_path = '../utils/ltp_data_v3.4.0/'
    cws_model_path = os.path.join(file_path + 'cws.model')
    pos_model_path = os.path.join(file_path + 'pos.model')
    par_model_path = os.path.join(file_path + 'parser.model')
    ner_model_path = os.path.join(file_path + 'ner.model')

    ext = Extraction(cws_model_path, pos_model_path, ner_model_path, par_model_path, lines, word2vec_path)
    ext.newsExtraction(news)
