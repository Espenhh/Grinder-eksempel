from net.grinder.script.Grinder import grinder
from net.grinder.script import Test
from net.grinder.plugin.http import HTTPRequest
from net.grinder.common import GrinderException
from net.grinder.plugin.http import HTTPPluginControl
from org.json import *

baseUrl = grinder.properties.getProperty("baseUrl", "http://localhost:8080")
sokeord = grinder.properties.getProperty("sokeord", "twitter")

class TestRunner:
    def __call__(self):
        grinder.statistics.delayReports = 1
        error = grinder.logger.error
        log = grinder.logger.output
            
        twitterTest = Test(901, "REST twittersoek")
        twitterRequest = twitterTest.wrap(HTTPRequest(url=baseUrl))
        
        profilbildeTest = Test(902, "REST profilbilder")
        profilbildeRequest = profilbildeTest.wrap(HTTPRequest())
        
        try:
            log("Soek etter 'Grinder' paa twitter og henter JSON-resultater")
            twitterJson = twitterRequest.GET("search.json?q=" + sokeord).text
            twitterObjekt = JSONObject(twitterJson)
            twitterResultater = twitterObjekt.getJSONArray("results")
            for i in range(0,twitterResultater.length()):
                enkeltTweet = twitterResultater.getJSONObject(i)
                brukerID = enkeltTweet.getString("from_user_id_str")
                log("Henter profilbilde for bruker:" + brukerID)
                profilbildeUrl = enkeltTweet.getString("profile_image_url")
                profilbildeRequest.GET(profilbildeUrl)
        except JSONException, ex:
            grinder.statistics.forLastTest.setSuccess(0)
            error("EXCEPTION HENDTE:")
            error(str(ex))