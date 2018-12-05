# read different formatted files
# included , but not exclusive
# config ini
# json files


import pytest
import sys
sys.path.append("../")
import pw.readconfig
import os
import configparser
import re

config = configparser.ConfigParser()
config.read('../pw/stocks.ini')

num_here = re.compile(r'[]+-]?\d+$')

sections = config.sections()

class Test_Config_Files(object):
    self.options = []

    def test_files_exist(self):
        msg = "File doesn't Exist!!"
        assert  os.path.exists("../pw/rest.ini")
        assert  os.path.exists("../pw/stocks.ini")
        #assert  os.path.exists("../pw/ocks.ini"), msg

    @pytest.fixture
    def handle(self):
        """file handle to operate on file"""
        config = configparser.ConfigParser()
        config.read('../pw/stocks.ini')
        return config

    @pytest.fixture(params = sections)
    def section(self,request):
        """one of stock category """
        return request.param

    def test_each_sections_len(self,section):
        assert len(section) >=4

    def test_section_not_null(self,section):
        assert section != ""

    def test_sections_no_num(self,section):
        assert not num_here.search(section)

    @pytest.fixture(params = sections)
    def options(self,request, handle, section):
        """options ,here is  stock name"""
        opt = handle.options(section)
        print("options {} under section={}\n".format(opt,section))
        self.joptions.append(opt)
    #return options
        return request.param

    #@pytest.fixture(params = options)
    #def test_config_options(self,request,options):
        #for opt in options:
            #print("item ==> {}".format(opt))
            #assert len(opt) < 6
    ###TODO Continue checking all the items in the files
    ## Not in the case , Stopping while encounter first error
    ## & skip the followings

    #def items
    #def test_kk():
        #pass






