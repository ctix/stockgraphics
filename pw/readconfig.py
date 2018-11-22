

import configparser

config = configparser.ConfigParser()
config.read('stocks.ini')

def test():
    secs = config.sections()
    print("all sections ==>{} ".format(secs))
    a = config.options("hi-tek")
    print("options under hi-tek ==> {}".format(a))

def get_stocks(sections):
    lst = []
    opts = config.options(sections)
    #print("options under {} ==> {}".format(sections,a))
    for op in opts:
        val = config.get(sections,op)
        lst.append(val)
    return lst

def get_all():
    allst = []
    secs = config.sections()
    for sc in secs:
       lst = get_stocks(sc)
       allst += lst

    return allst
if __name__ == "__main__":
    ll = get_stocks("index")
    print("options under index ==> {}".format(ll))
    ll = get_stocks("hi-tek")
    print("options under hi-tek ==> {}".format(ll))

    lst =  get_all()
    print("ALL options ==> {}".format(lst))

