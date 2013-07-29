############ BEGIN ASSIGNMENT SPECIFIC CODE - YOU'LL HAVE TO EDIT THIS ##############

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController   
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
import os

# Make sure you change this string to the last segment of your class URL.
# For example, if your URL is https://class.coursera.org/pgm-2012-001-staging, set it to "pgm-2012-001-staging".
URL = 'sdn-001'

# the "Identifier" you used when creating the part
partIds = ['m7a']                        
# used to generate readable run-time information for students
partFriendlyNames = ['Create a server load-balance application using PyResonance'] 
# source files to collect (just for our records)
sourceFiles = ['%s/pyretic/pyretic/pyresonance/resonance_policy.py' % os.environ[ 'HOME' ],
               '%s/pyretic/pyretic/pyresonance/resonance_states.py' % os.environ[ 'HOME' ],
               '%s/pyretic/pyretic/pyresonance/resonance_handlers.py' % os.environ[ 'HOME' ],
               '%s/pyretic/pyretic/pyresonance/resonance_main.py' % os.environ[ 'HOME' ],
               '%s/pyretic/pyretic/pyresonance/sendy_json.py' % os.environ[ 'HOME' ] ]     

# My network topology
class MyTopo(Topo):
    "1 switch and 3 host topology with varying delays"

    def __init__(self, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        
        s1 = self.addSwitch('s1')

        h1 = self.addHost('h1')
        self.addLink(h1, s1)
        h2 = self.addHost('h2')
        self.addLink(h2, s1, delay='200ms')
        h3 = self.addHost('h3')
        self.addLink(h3, s1)
          
def output(partIdx):
  """Uses the student code to compute the output for test cases."""
  outputString = ''
  
  if partIdx == 0: # This is m6a
    print "a. Firing up Mininet"
    net = Mininet(topo=MyTopo(), controller=lambda name: RemoteController( 'c0', '127.0.0.1' ), host=CPULimitedHost, link=TCLink)                                  
    net.start() 

    h1 = net.get('h1')
  
    print "b. Starting Test"
    # Start pings
    outputString += h1.cmdPrint('ping', '-c9', '10.0.0.100')
    
    print "c. Stopping Mininet"
    net.stop()
    
  return outputString.strip()

print output(0)
