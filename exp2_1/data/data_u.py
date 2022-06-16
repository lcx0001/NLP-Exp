import codecs
from sklearn.model_selection import train_test_split
import pickle

INPUT_DATA = "RMRB_NER_CORPUS.txt"
SAVE_PATH = "./datasave.pkl"
id2tag = []  
tag2id = {}
word2id = {}
id2word = []


def getMaps(input_list):
    '''
    构造map
    :param input_list: 给定list
    :return: 对应map
    '''
    maps = {}
    for list_ in input_list:
        for e in list_:
            if e not in maps:
                maps[e] = len(maps)
    return maps

def getList(input_list,input_map):
    '''
    获取每行文本列表对应的id列表
    :param input_list: 输入列表
    :param input__map:输入map
    :return: id_list
    '''
    id_list = []
    for i in range(len(input_list)):
        id_list.append(input_map[input_list[i]])
    return id_list

def handle_data():
    '''
    处理数据，并保存至savepath
    :return:
    '''
    x_data = []
    y_data = []
    with open(INPUT_DATA, 'r', encoding="utf-8") as ifp:
        x_word = []
        y_tag = []
        words = []
        tags = []
        for line in ifp:
            if line != '\n':
                word, tag = line.strip('\n').split()
                words.append(word)
                tags.append(tag)
            else:
                x_word.append(words)
                y_tag.append(tags)
                words = []
                tags = []
        word2id = getMaps(x_word)
        tag2id = getMaps(y_tag)
        id2word = list(word2id)
        id2tag = list(tag2id)
        for i in range(len(x_word)):
            x_data.append(getList(x_word[i],word2id))
            y_data.append(getList(y_tag[i],tag2id))


    # print(word2id)
    # print(tag2id)
    # print(id2tag)
    # print(id2word)
    # print(x_data[0])
    # print(y_data[0])
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.1, random_state=43)
    with open(SAVE_PATH, 'wb') as outp:
        pickle.dump(word2id, outp)
        pickle.dump(id2word, outp)
        pickle.dump(tag2id, outp)
        pickle.dump(id2tag, outp)
        pickle.dump(x_train, outp)
        pickle.dump(y_train, outp)
        pickle.dump(x_test, outp)
        pickle.dump(y_test, outp)


if __name__ == "__main__":
    handle_data()
