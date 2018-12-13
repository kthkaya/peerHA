import socket
import subprocess, psutil
import vici

class Swan:
    def __init__(self):
        self.primary = { 'primary' : { 'version' : '1',  'local_addrs' : ['192.168.0.102'] , 'remote_addrs' : ['192.168.0.104'],
                              'local' : { 'auth' : 'psk' , 'id' : '192.168.0.102'} ,
                              'remote' : { 'auth' : 'psk' , 'id' : '192.168.0.104'}, 
                              'children' : { 'primary' : {'mode' : 'tunnel', 'start_action' : 'start', 
                                                         'local_ts' : ['10.10.10.0/24'], 'remote_ts' : ['10.20.20.0/24']}}}}
    
        self.bkp = { 'bkp' : { 'version' : '1',  'local_addrs' : ['192.168.0.102'] , 'remote_addrs' : ['192.168.0.105'],
                              'local' : { 'auth' : 'psk' , 'id' : '192.168.0.102'} ,
                              'remote' : { 'auth' : 'psk' , 'id' : '192.168.0.105'}, 
                              'children' : { 'bkp' : {'mode' : 'tunnel', 'start_action' : 'start', 
                                                         'local_ts' : ['10.10.10.0/24'], 'remote_ts' : ['10.20.20.0/24']}}}}
    
        self.viciSession = 0
    
    def removeConn(self, connName):
        unload = { 'name' : connName }
        terminate = { 'ike' : connName, 'timeout': '-1'}
        self.viciSession.unload_conn(unload)
        self.viciSession.terminate(terminate)
        psutil.Popen(["ipsec", "down", connName], stdout=subprocess.PIPE)
    
    def addConn(self, connName):        
        if "primary" in connName:
            self.viciSession.load_conn(self.primary)
        elif "bkp" in connName:
            self.viciSession.load_conn(self.bkp)
    
    def openViciSes(self):
        s = socket.socket(socket.AF_UNIX)
        s.connect("/var/run/charon.vici")
        self.viciSession = vici.Session(s)
    
    def closeViciSes(self):
        self.viciSession.close()