class Tokenizer(object):
    def __init__(self, words, max_len):
        self.words = words
        self.max_len = max_len

    def fmm_split(self, text):
        '''
        正向最大匹配分词算法
        :param text: 待分词字符串
        :return: 分词结果，以list形式存放，每个元素为分出的词
        '''
        start = 0
        result = []
        while start != len(text):
            end = start + max_len
            if end > len(text):
                end = len(text)
            for i in range(max_len):
                if text[start:end] in words or len(text[start:end]) == 1:
                    result.append(text[start:end])
                    start = end
                    break
                end -= 1
        return result




    def rmm_split(self, text):
        '''
        逆向最大匹配分词算法
        :param text: 待分词字符串
        :return: 分词结果，以list形式存放，每个元素为分出的词
        '''
        start = len(text)
        result = []
        while start != 0:
            end = start - max_len
            if end < 0:
                end = 0
            for i in range(max_len):
                if text[end:start] in words or len(text[end:start]) == 1:
                    result.append(text[end:start])
                    start = end
                    break
                end += 1
        index = len(result)
        final_result = []
        for word in result:
            final_result.append(result[index-1])
            index -= 1
        return final_result

    def bimm_split(self, text):
        '''
        双向最大匹配分词算法
        :param text: 待分词字符串
        :return: 分词结果，以list形式存放，每个元素为分出的词
        '''
        result1 = self.fmm_split(text)
        result2 = self.rmm_split(text)
        len1 = len(result1)
        len2 = len(result2)
        if len1 < len2:
            return result1
        elif len1 > len2:
            return result2
        else:
            if result1 == result2:
                return result1
            else:
                num1 = 0
                num2 = 0
                for word in result1:
                    if len(word) == 1:
                        num1 += 1
                for word in result2:
                    if len(word) == 1:
                        num2 += 1
                if num1 <= num2:
                    return result1
                else:
                    return result2



def load_dict(path):
    tmp = set()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip().split(' ')[0]
            tmp.add(word)
    return tmp


if __name__ == '__main__':
    words = load_dict('dict.txt')
    max_len = max(map(len, [word for word in words]))
    print(words)
    # test
    tokenizer = Tokenizer(words, max_len)
    texts = [
        '研究生命的起源',
        '无线电法国别研究',
        '人要是行，干一行行一行，一行行行行行，行行行干哪行都行。',
        '语言及开发类课程进两个系统均可。',
        '南京市长江大桥'

    ]
    for text in texts:
        # 前向最大匹配
        print('前向最大匹配:', '/'.join(tokenizer.fmm_split(text)))
        # 后向最大匹配
        print('后向最大匹配:', '/'.join(tokenizer.rmm_split(text)))
        # 双向最大匹配
        print('双向最大匹配:', '/'.join(tokenizer.bimm_split(text)))
        print('')
