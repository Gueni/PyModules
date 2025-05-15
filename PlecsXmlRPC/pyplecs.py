
import xmlrpc.client
class pyplecs:
    
    def __init__(self,url,port,path,modelvar):
        '''
        '''
        self.url        =   url
        self.port       =   port
        self.path       =   path
        self.modelvar   =   modelvar
    
    def rpc_connect(self):
        '''
        '''
        self.server =   xmlrpc.client.ServerProxy(self.url + ':' + self.port)

    def load_model(self):
        '''
        '''
        #add bloc to test if path is valid 
        self.server.plecs.load(self.path)
    
    def ClearTrace(self,scopePath):
        '''
        '''
        self.server.plecs.scope(scopePath,'ClearTraces')
    
    def ClearAllTraces(self,scopedict):
        '''
        '''
        for key,val in scopedict:
            self.server.plecs.scope(val,'ClearTraces')

opts = {'ModelVars' :  { 'R2' : 50e-6 } }

for R in range(1,15):
    opts['ModelVars']['R2'] = R
    proxy.plecs.simulate("Pyrpc", opts)
    proxy.plecs.scope('Pyrpc/Scope','HoldTrace')
    time.sleep(4)
    # proxy.plecs.scope('Pyrpc/Scope', 'SaveTraces', 'ﬁleName')
proxy.plecs.close('Pyrpc') 