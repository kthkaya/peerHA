import os
import subprocess
#from ping3 import ping
from time import sleep
from hamodule import Swan


def ping(ipAddr):
    result = str(subprocess.Popen(["/bin/ping", "-c4", "-w2", ipAddr], stdout=subprocess.PIPE).stdout.read())
    words = result.split()
    
    for word in words:
            if "%" in word:
                return int((word[:-1]))
        

if __name__ == '__main__':
    mySwan = Swan()
    primaryPeer= "192.168.0.105"
    
    mySwan.openViciSes()
    mySwan.addConn("primary")
    #mySwan.closeViciSes()
    backupActive = False
    
    while True:
        response = ping(primaryPeer)
        print (response)
        
        if response<50:
            #print (hostname, 'is up!')
            if backupActive:
                #Preempt here
                print("Preempting")
                mySwan.openViciSes()
                mySwan.removeConn("bkp")
                mySwan.addConn("primary")
                #mySwan.closeViciSes()
                backupActive = False
        else:
            #print (hostname, 'is down!')
            if not backupActive:
                #Activate backup here
                print("Activating backup")
                mySwan.openViciSes()
                mySwan.removeConn("primary")
                mySwan.addConn("bkp")
                #mySwan.closeViciSes()
                backupActive = True
        sleep(10)
