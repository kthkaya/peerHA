"""
https://lists.strongswan.org/pipermail/users/2018-April/012495.html
"""

import vici
import time
from collections import OrderedDict

s = vici.Session()
load_config = { 'vv' : { 'version' : '1',  'local_addrs' : ['10.155.3.2'] , 'remote_addrs' : ['10.10.10.1'], 'proposals' : ['aes128-sha1-modp1024'], 'fragmentation' : 'yes', 'encap' : 'yes', 'mobike' : 'no', 'local' : { 'id' : 'priyank+site', 'auth' : 'psk' } ,  'remote' : { 'auth' : 'psk' , 'id' : '10.10.10.1'}, 'aggressive' : 'yes', 'dpd_delay' : '30s', 'keyingtries' : '300', 'children' : { 'vv' : {'mode' : 'tunnel', 'start_action' : 'start', 'ipcomp' : 'no', 'rekey_time' : '14400s', 'start_action' : 'start', 'esp_proposals' : ['null-md5-modp1024'], 'mark_in' : '1073751018', 'mark_out' : '1073751018', 'dpd_action' : 'restart', 'life_time' : '28800s'}}}}

# Load the connection to strongswan
s.load_conn(load_config)

print("===================Load start =========================")
print("List of conn after loading:")
conns = s.list_conns()
for conn in conns:
    print("{}".format(conn))
print("List of valid sas after loading:")
valid_sas = s.list_sas()
for sa in valid_sas:
    print("{}".format(sa))
print("===================Load end ===========================")

time.sleep(10)

print("===================Terminate Start =============================")
terminate = { 'ike' : 'vv', 'timeout': '-1'}
s.terminate(terminate)

unload = { 'name' : 'vv' }
s.unload_conn(unload)

print("List of conn after unload:")
conns = s.list_conns()
for conn in conns:
    print("{}".format(conn))

print("List of sas after unload:")
invalid_sas = s.list_sas()
for sa in invalid_sas:
    print("{}".format(sa))
print("===================Terminate End =============================")