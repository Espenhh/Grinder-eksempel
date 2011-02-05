from net.grinder.script.Grinder import grinder
from net.grinder.script import Test
from net.grinder.plugin.http import HTTPRequest
from net.grinder.common import GrinderException
from HTTPClient import Codecs, NVPair
from net.grinder.plugin.http import HTTPPluginControl
from net.grinder.plugin.http import HTTPUtilities
from org.json import *
from java.util import Random
from java.lang import String
from no.bekk.open.test.util import TestDataGenerator

baseUrl = grinder.properties.getProperty("baseUrl", "http://localhost:8080")
sokeord = grinder.properties.getProperty("sokeord", "twitter")
antallTestbrukere = grinder.properties.getProperty("antalltestbrukere", 1)
basicAuthBrukernavn = grinder.properties.getProperty("basicAuthBrukernavn", "admin")
basicAutoPassord = grinder.properties.getProperty("basicAutoPassord", "")
randomGenerator = Random()

class TestRunner:
    def __call__(self):
        grinder.statistics.delayReports = 1
        error = grinder.logger.error
        log = grinder.logger.output
        
		randomTall = randomGenerator.nextInt(400000)

        brukerNummer = TestDataGenerator.hentTilfeldigBrukerKontoNummer(randomTall)
        log("Behandler bruker med brukernummer: " + brukerNummer)

		backdoorAktiveringsHeader = ( NVPair("brukerNummer", brukerNummer ), NVPair("brukerType", "49" ) )
        
        httpUtilities = HTTPPluginControl.getHTTPUtilities()

        twitterTest = Test(301, "REST twittersoek")
        twitterRequest = twitterTest.wrap(HTTPRequest(url=baseUrl, headers=backdoorAktiveringsHeader))
        
        profilbildeTest = Test(302, "REST profilbilder")
        profilbildeRequest = profilbildeTest.wrap(HTTPRequest(), headers=backdoorAktiveringsHeader)
        
        try:
            log("Soek etter 'Grinder' paa twitter og henter JSON-resultater")
            twitterJson = twitterRequest.GET("search.json?q=" + sokeord, (), ( httpUtilities.basicAuthorizationHeader(basicAuthBrukernavn, basicAutoPassord), )).text
            twitterObjekt = JSONObject(twitterJson)
            twitterResultater = twitterObjekt.getJSONArray("results")
            for i in range(0,twitterResultater.length()):
                enkeltTweet = twitterResultater.getJSONObject(i)
                brukerID = enkeltTweet.getString("from_user_id_str")
                log("Henter profilbilde for bruker:" + brukerID)
                profilbildeUrl = enkeltTweet.getString("profile_image_url")
                profilbildeRequest.GET(profilbildeUrl, (), ( httpUtilities.basicAuthorizationHeader(basicAuthBrukernavn, basicAutoPassord), ))
        except JSONException, ex:
            grinder.statistics.forLastTest.setSuccess(0)
            error("EXCEPTION HENDTE:")
            error(str(ex))