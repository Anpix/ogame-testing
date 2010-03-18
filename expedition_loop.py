#import re
import weblogic
import planets
import re
import time
import random
import small_expedition
import large_redesign_expedition

class ExpeditionLoop:
    
    def __init__(self, wl, ld):
        self.wl = wl
        self.ld = ld
        self.fleet1 = "http://%s.ogame.org/game/index.php?page=fleet1&session=%s"
        self.impossibleDispatchREGEX = re.compile(r"Fleet dispatch impossible")
        self.fleetSlotREGEX = re.compile(r"<span>fleets:</span> ([0-9]+)/([0-9]+)")
        self.expSlotREGEX = re.compile(r"<span>Expeditions:</span> ([0-9]+)/([0-9]+)") 
    
    def smallExpeditionFromPlanet(self, planet):
        planet.switch("overview", self.ld.session);
        gal = planet.location.galaxy
        ss = planet.location.solarsystem
        posn = planet.location.slot
        print gal + ":" + ss + ":" + posn
        self.smallExpeditionFromCoords(gal, ss, posn)
    
    def largeExpeditionFromPlanet(self, planet):
        planet.switch("overview", self.ld.session);
        gal = planet.location.galaxy
        ss = planet.location.solarsystem
        posn = planet.location.slot
        print gal + ":" + ss + ":" + posn
        self.largeExpeditionFromCoords(gal, ss, posn)
    
    def smallExpeditionFromCoords(self, gal, ss, posn):
        f = small_expedition.SmallExpedition(self.wl, self.ld)
        return f.expeditionFlightFromPlanet(gal, ss, posn)
    
    def largeExpeditionFromCoords(self, gal, ss, posn):
        f = large_redesign_expedition.LargeExpedition(self.wl, self.ld)
        return f.expeditionFlightFromPlanet(gal, ss, posn)
    
    def delayTime(self):
        delay = random.randint(1,5)
        print "Sleeping " + str(delay) + " seconds..."
        time.sleep(delay)
    
    def runExpeditions(self, wl, ld):
        loginpage = wl._recentResponse
        planetManager = planets.PlanetManager(wl)
        loop.delayTime()
        current = planets.PlanetManager.currentPlanet(planetManager, loginpage)
        
        if not self.checkOpenSlots():
            print "No open slots, cancelling expedition loop!"
            return
        loop.largeExpeditionFromCoords(current.location.galaxy, current.location.solarsystem, current.location.slot)

        planetList = planets.PlanetManager.availablePlanets(planetManager, loginpage)
        
        for planet in planetList:
            if not self.checkOpenSlots():
                print "No open slots, cancelling expedition loop!"
                return
            loop.delayTime()
            loop.largeExpeditionFromPlanet(planet)
            
        for planet in planetList:
            if not self.checkOpenSlots():
                print "No open slots, cancelling small expedition loop!"
                return
            loop.delayTime()
            loop.smallExpeditionFromPlanet(planet)
        
        #small expeditions prioritized after last
        loop.smallExpeditionFromCoords(current.location.galaxy, current.location.solarsystem, current.location.slot)
    
    def checkOpenSlots(self):
        fleet_url = self.fleet1 %\
                    (self.wl.server, self.ld.session)
        page = self.wl.fetchResponse(fleet_url)
        ret = False
        
        fleetMatch = self.fleetSlotREGEX.search(page.getvalue())
        fleetCurrent = fleetMatch.group(1)
        fleetTotal = fleetMatch.group(2)
        print "Fleet :: " + fleetCurrent + "/" + fleetTotal
         
        expMatch = self.expSlotREGEX.search(page.getvalue())
        expCurrent = expMatch.group(1)
        expTotal = expMatch.group(2)
        print "Expeditions :: " + expCurrent + "/" + expTotal
        
        if int(fleetCurrent) < int(fleetTotal) and int(expCurrent) < int(expTotal):
            ret = True
        else:
            print "No fleetslots available to send more expeditions!"
        print ret
        return ret
        
if __name__ == '__main__':
    wl = weblogic.Weblogic()
    ld = wl.login()
    loop = ExpeditionLoop(wl, ld)
    loop.runExpeditions(wl, ld)
    """
    loginpage = wl._recentResponse
    planetManager = planets.PlanetManager(wl)
    loop.delayTime()
    
    current = planets.PlanetManager.currentPlanet(planetManager, loginpage)
    loop.largeExpeditionFromCoords(current.location.galaxy, current.location.solarsystem, current.location.slot)
    
    planetList = planets.PlanetManager.availablePlanets(planetManager, loginpage)    
    for planet in planetList:
        loop.delayTime()
        loop.smallExpeditionFromPlanet(planet)
    
    #small expeditions prioritized after last
    loop.smallExpeditionFromCoords(current.location.galaxy, current.location.solarsystem, current.location.slot)
    """
"""
    for planet in planetList:
        loop.delayTime()
        loop.largeExpeditionFromPlanet(planet)
"""   
    
    