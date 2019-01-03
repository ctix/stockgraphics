import configparser

CONFIGFILE = '../config/stocks.ini'


class ConfigOfStocks(object):
    """Config files category of fields of Stocks"""
    def __init__(self, configfn=CONFIGFILE):
        self.config = configparser.ConfigParser()
        self.config.read(configfn)

    def get_all_sections_name(self):
        """all the category for the interesting stocks"""
        return self.config.sections()
        # print("all sections ==>{} ".format(secs))

    def get_section_option_value(self, sec, opt):
        """the stock code by field/category and name """
        return self.config.get(sec, opt)

    def get_options_in_the_section(self, section_name):
        """stockname in a section/category"""
        return self.config.options(section_name)

    def get_all_option_list(self):
        """return all the option=stockname in a list"""
        option_list = []
        sections = self.get_all_sections_name()
        for sec in sections:
            opts = self.get_options_in_the_section(sec)
            option_list.append(opts)
        return option_list

    def get_section_value_list(self, section_name):
        """return values/stockcode in a section"""
        lst = []
        opts = self.config.options(section_name)
        # print("options under {} ==> {}".format(sections,a))
        for op in opts:
            val = self.get_section_option_value(section_name, op)
            lst.append(val)
        return lst

    def get_all_in_list(self):
        """get all values == stock code in the config files"""
        allst = []
        secs = self.config.sections()
        for sc in secs:
            lst_ = self.get_section_value_list(sc)
            allst += lst_
        return set(allst)  # unique name in list


if __name__ == "__main__":
    cfg = ConfigOfStocks()
    secs = cfg.get_all_sections_name()
    print("all sections name {}".format(secs))
    ll = cfg.get_section_list("index")
    print("options under index ==> {}".format(ll))
    ll = cfg.get_section_list("hi-tek")
    print("options under hi-tek ==> {}".format(ll))
    ll = cfg.get_section_list("monitored")
    print("stocks under monitored ==> {}".format(ll))
    lst = cfg.get_all_in_list()
    print("ALL options values ==> {}".format(lst))
