from net.grinder.script.Grinder import grinder
from net.grinder.script import Test
from net.grinder.plugin.http import HTTPRequest

class TestRunner:
    def __call__(self):
        kontoTest = Test(101, "Laste vg.no")
        kontoRequest = kontoTest.wrap(HTTPRequest())   
        kontoRequest.GET("http://www.vg.no")