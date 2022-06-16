import torch
import pickle
import re
from model import CWS
from model import NER

if __name__ == '__main__':
    cws_model = torch.load('model/cws_model.pkl', map_location=torch.device('cpu'))
    ner_model = torch.load('model/ner_model.pkl', map_location=torch.device('cpu'))
    output = open('cws_ner_result.txt', 'w', encoding='utf-8')

    with open('data/cws_datasave.pkl', 'rb') as inp_cws:
        word2id_cws = pickle.load(inp_cws)
        id2word_cws = pickle.load(inp_cws)
        tag2id_cws = pickle.load(inp_cws)
        id2tag_cws = pickle.load(inp_cws)
        x_train_cws = pickle.load(inp_cws)
        y_train_cws = pickle.load(inp_cws)
        x_test_cws = pickle.load(inp_cws)
        y_test_cws = pickle.load(inp_cws)
    
    with open('data/ner_datasave.pkl', 'rb') as inp_ner:
        word2id_ner = pickle.load(inp_ner)
        id2word_ner = pickle.load(inp_ner)
        tag2id_ner = pickle.load(inp_ner)
        id2tag_ner = pickle.load(inp_ner)
        x_train_ner = pickle.load(inp_ner)
        y_train_ner = pickle.load(inp_ner)
        x_test_ner = pickle.load(inp_ner)
        y_test_ner = pickle.load(inp_ner)

    with open('data/test.txt', 'r', encoding='utf-8') as f:
        for test in f:
            flag = False
            test = test.strip()

            x_cws = torch.LongTensor(1, len(test))
            mask_cws = torch.ones_like(x_cws, dtype=torch.uint8)
            length_cws = [len(test)]
            for i in range(len(test)):
                if test[i] in word2id_cws:
                    x_cws[0, i] = word2id_cws[test[i]]
                else:
                    x_cws[0, i] = len(word2id_cws)

            x_ner = torch.LongTensor(1, len(test))
            mask_ner = torch.ones_like(x_ner, dtype=torch.uint8)
            length_ner = [len(test)]
            for i in range(len(test)):
                if test[i] in word2id_ner:
                    x_ner[0, i] = word2id_ner[test[i]]
                else:
                    x_ner[0, i] = len(word2id_ner)

            predict_cws = cws_model.infer(x_cws, mask_cws, length_cws)[0]
            predict_ner = ner_model.infer(x_ner, mask_ner, length_ner)[0]


            for i in range(len(test)):
                print(test[i], end='', file=output)
                if re.match('E',id2tag_ner[predict_ner[i]]) or re.match('S',id2tag_ner[predict_ner[i]]):
                    if id2tag_cws[predict_cws[i]] in ['B', 'M']: 
                        continue
                    print(' ', end='', file=output)
                elif re.match('O',id2tag_ner[predict_ner[i]]):
                    if id2tag_cws[predict_cws[i]] in ['B', 'M']: 
                        continue
                    print(' ', end='', file=output)
            print(file=output)
