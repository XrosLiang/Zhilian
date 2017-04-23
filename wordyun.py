import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba


def fc(text):
    text = open(text, 'r').read()
    fc_text = jieba.cut(text, cut_all=True)
    return " ".join(fc_text)

def pic(content):
    wc = WordCloud()
    wordcloud = wc.generate(content)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()

def main(text):
    content = fc(text)
    print("正在生成词云...")
    pic(content)

if __name__ == '__main__':
    main('demand.txt')
