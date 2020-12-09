import re

def StrToInt(self, price):
    result = re.sub('[^0-9]', '', price)
    return result