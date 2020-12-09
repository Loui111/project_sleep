from urllib import parse
import urllib

def url_decoding(self, url):
                                # url: https://search.shopping.naver.com/search/all?frm=NVSHAKW&origQuery=%ED%86%A0%ED%8D%BC%EB%A7%A4%ED%8A%B8%EB%A6%AC%EC%8A%A4&pagingIndex=1&pagingSize=150&productSet=total&query=%ED%86%A0%ED%8D%BC%EB%A7%A4%ED%8A%B8%EB%A6%AC%EC%8A%A4&sort=rel&timestamp=&viewType=list
    url2 = url.find('query=')  # 118
    url3 = url[url2 + 6:]  # query=%ED%86%A0%ED%8D%BC%EB%A7%A4%ED%8A%B8%EB%A6%AC%EC%8A%A4&sort=rel&timestamp=&viewType=list
    url4 = url3.find('&')  # 123
    url5 = url3[:url4]  # %ED%86%A0%ED%8D%BC%EB%A7%A4%ED%8A%B8%EB%A6%AC%EC%8A%A4
    decoded = urllib.parse.unquote(url5)  #decoded: 접이식매트리

    return decoded