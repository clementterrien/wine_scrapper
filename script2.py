import re
from product import data
from service import getRefInURL
def main():
    feature = 'hello'
    bonjour = 'https://www.vinatis.com/39420-pinot-noir-2018-bread-and-butter'
    #eturn re.compile(fr".*?{feature}.*?", bonjour)
    u = getRefInURL(bonjour)

    return True
    # #x = list(filter(lambda v: re.match(r'.+% vol', v), test))
    # #x = list(filter(lambda v: test in test_list, test))
    # #x = any(item in test_list for item in test)
    # #region = [e for e in test if e in test_list]
    #print(test)

print(main())