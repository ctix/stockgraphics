# read different formatted files
# included , but not exclusive
# config ini
# json files

import pytest
import sys
sys.path.append("..")
from pw import readconfig
import os
# import configparser
# import re


class Test_Config_Files(object):
    def test_files_exist(self):
        msg = "File doesn't Exist!!"
        assert os.path.exists("../config/rest.ini"), msg
        assert os.path.exists("../config/stocks.ini")

    @pytest.fixture
    def my_config(self):
        '''Returns a Wallet instance with a zero balance'''
        return readconfig.ConfigOfStocks()

    @pytest.mark.parametrize("section,     option,    expected", [
                            ("monitored", "htgx",    "sz002023"),
                            ("wine",      "gzmt",      "sh600519"),
                            ("hi-tek",    "jjw",        "sz300474"), ])
    def test_get_section_option_value(self, my_config,
                                      section, option, expected):
        assert my_config.get_section_option_value(section, option) == expected

    def test_have_more_sections_than3(self, my_config):
        seclst = my_config.get_all_sections_name()
        assert len(seclst) >= 3

    @pytest.fixture(params=[("wine", "gzmt"),
            ("index", "sh"), ("hi-tek", "slw")])
    def name_categroy_data(self, request):
        return request.param

    def test_options_in_section(self, name_categroy_data, my_config):
        """options ,here is  stock name in the section/category"""
        section, expected = name_categroy_data
        assert expected in my_config.get_options_in_the_section(section)


# class Test_Config_Files(object):
    # def __init__(self):
        # Config = readconfig.ConfigOfStocks()
        # self.sections = Config.get_all_sections_name()
        # self.options = []

    # @pytest.fixture
    # def handle(self):
        # """file handle to operate on file"""
        # config = configparser.ConfigParser()
        # config.read('../config/stocks.ini')
        # return config

    # @pytest.fixture(params = self.sections)
    # def section(self,request):
        # """one of stock category """
        # return request.param

    # @pytest.fixture(params = sections)
    # def options(self,request, handle, section):
        # """options ,here is  stock name"""
        # opt = handle.options(section)
        # print("items {} under section={}\n".format(opt,section))
        # self.joptions.append(opt)
        # return request.param

    # @pytest.fixture(params = options)
    # def test_config_options(self,request,options):
        # for opt in options:
        # print("item ==> {}".format(opt))
        # assert len(opt) < 6

    # # def test_transactions(my_config, section, option, expected):
        # # assert my_config.get_section_option_value(section, option) == expected
        # # my_wallet.add_cash(earned)
        # # my_config.
        # # my_wallet.spend_cash(spent)
        # # my_config.
        # # assert my_wallet.balance == expected

    # def test_section_not_null(self,section):
        # assert section != ""

    # def test_sections_no_num(self,section):
        # assert not num_here.search(section)

    # def test__monitored_sections(self):
        # assert "monitored" in self.sections

    # def test_get_monitored_stocks(self,section):
        # assert stock_list

    # TODO Continue checking all the items in the files
    # Not in the case , Stopping while encounter first error
    # & skip the followings

    # def items
    # def test_kk():
        # pass
if __name__ == "__main__":
    pass
