import os
from time import sleep
from hamodule import Swan

def ping(ipAddr):
    return os.system("ping -c 3 -w2 " + ipAddr + " > /dev/null 2>&1")

if __name__ == '__main__':
    mySwan = Swan()
    primaryPeer= "192.168.0.104"
    
    mySwan.openViciSes()
    mySwan.addConn("primary")
    mySwan.closeViciSes()
    backupActive = False
    
    while True:
        response = ping(primaryPeer)
        if response == 0:
            #print (hostname, 'is up!')
            if backupActive:
                #Preempt here
                print("Preempting")
                mySwan.openViciSes()
                mySwan.removeConn("bkp")
                mySwan.addConn("primary")
                mySwan.closeViciSes()
                backupActive = False
        else:
            #print (hostname, 'is down!')
            if not backupActive:
                #Activate backup here
                print("Activating backup")
                mySwan.openViciSes()
                mySwan.removeConn("primary")
                mySwan.addConn("bkp")
                mySwan.closeViciSes()
                backupActive = True
        sleep(10)