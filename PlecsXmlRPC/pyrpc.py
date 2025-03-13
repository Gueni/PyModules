
import xmlrpc.client
import time

proxy = xmlrpc.client.ServerProxy("http://localhost:1080/RPC2")
proxy.plecs.load("/home/hunter/Documents/Workspace/Python_code/PlecsXmlRPC/Pyrpc.plecs")
proxy.plecs.scope('Pyrpc/Scope', 'ClearTraces')
opts = {'ModelVars' :  { 'R2' : 50e-6 } }

for R in range(1,15):
    opts['ModelVars']['R2'] = R
    proxy.plecs.simulate("Pyrpc", opts)
    proxy.plecs.scope('Pyrpc/Scope','HoldTrace')
    time.sleep(4)
    # proxy.plecs.scope('Pyrpc/Scope', 'SaveTraces', 'ﬁleName')
proxy.plecs.close('Pyrpc') 



