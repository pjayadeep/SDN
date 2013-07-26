'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 3 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.util import irange,dumpNodeConnections

class CustomTopo(Topo):
	"Simple Data Center Topology"

	"linkopts - (1:core, 2:aggregation, 3: edge) parameters"
	"fanout - number of child switch per parent switch"
	def __init__(self, corelinkopts, aggrlinkopts, edgelinkopts, fanout=2, **opts):
		# Initialize topology and default options
		Topo.__init__(self, **opts)
		c1 = self.addSwitch('c1')
		self.createLinks(c1,fanout,2,corelinkopts,aggrlinkopts,edgelinkopts)
	hid = 0
	eid = 0
	aid = 0

	def hostID(self):
		self.hid = self.hid + 1
		return self.hid
	def eswID(self):
		self.eid = self.eid + 1
		return self.eid
	def aswID(self):
		self.aid = self.aid + 1
		return self.aid
		
	def createLinks(self, s, fanout,depth,corelinkopts, aggrlinkopts,edgelinkopts):
		if (depth == 0 ): #host <-> switch
			for i in range(1,fanout+1):
				h = self.addHost('h%d' % self.hostID())
				self.addLink(s, h,**edgelinkopts)
				
		elif depth == 1: # edge<->aggr
			for i in range(1,fanout+1):
				s1 = self.addSwitch('e%d' % self.eswID())
				self.createLinks(s1,fanout, depth-1,corelinkopts, aggrlinkopts, edgelinkopts )
				self.addLink(s, s1, **aggrlinkopts)

		elif depth == 2: # aggr<->core
			for i in range(1,fanout+1):
				s1 = self.addSwitch('a%d' % self.aswID())
				self.createLinks(s1,fanout, depth-1, corelinkopts, aggrlinkopts, edgelinkopts)
				self.addLink(s, s1, **corelinkopts)

		
def Test():
	corelinkopts = {'bw':10, 'delay':'5ms' }
	aggrlinkopts = {'bw':5, 'delay':'5ms' }
	edgelinkopts = {'bw':1, 'delay':'5ms' }
	#linkopts = {}
	linkopts = {'bw':10, 'delay':'5ms', 'loss':1, 'max_queue_size':1000, 'use_htb':True}
	topo = CustomTopo(linkopts, linkopts, linkopts, fanout=2)
	net = Mininet(topo,link=TCLink)
	net.start()

	print "Dumping host connections"
	dumpNodeConnections(net.hosts)
	print "Testing bandwidth between h1 and h4"
	h1, h4 = net.get('h1', 'h4')
	net.iperf((h1, h4))
	h8 = net.get('h8')
	net.iperf((h1, h8))

	net.stop()


	    
topos = { 'custom': ( lambda: CustomTopo() ) }

if __name__ == '__main__':
	setLogLevel('info')
	Test()
