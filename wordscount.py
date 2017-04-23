import jieba
import time


def fc(text):
    """
    结巴分词
    :return: 
    """
    with open(text, 'r') as f:
        return [",".join(jieba.cut(line.strip())) for line in f.readlines()]

def count_all(text, content):
    """
    统计数量
    :param text:
    :param content: 
    :return: 
    """
    word_dict = {}
    word_list = [word.split(',') for word in content]
    for item in word_list[0]:
        if item not in word_dict:
            word_dict[item] = 1
        else:
            word_dict[item] += 1
    for key in word_dict:
        if key != " ":
            print(key+','+str(word_dict[key])+'\n')
            write_to_csv(text, key+','+str(word_dict[key])+'\n')
    return word_dict.items()

def operation(worddict):
    """
    排序操作
    :param word_dict: 
    :return: 
    """
    dict = sorted(worddict, key=lambda d:d[1], reverse=True)
    print(dict)

def write_to_csv(text, items):
    """
    以相同的文件名保存到csv文件
    :param text: 
    :param items: 
    :return: 
    """

    with open(text[:-4]+".csv", "a") as f:
        f.write(items)

def main(text):
    content = fc(text)
    time.sleep(1)
    word_dict = count_all(text, content)
    operation(word_dict)

if __name__ == '__main__':
    main("demand.txt")
