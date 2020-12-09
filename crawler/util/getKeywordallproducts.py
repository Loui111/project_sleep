import configparser

def getKeywordallproducts(self):

    config = configparser.ConfigParser()
    config.read('./input/Keywordallproducts.ini', encoding='utf-8')
    keywords = config['KEYWORDS']['keywords']

    list = keywords.split('\n')
    keywords_list=[]

    for keyword in list:
        keywords_list.append(keyword[:-1])

    return keywords_list