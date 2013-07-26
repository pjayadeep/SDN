'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 4 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
from pox.lib.packet import *
import os
import csv
from sets import Set

''' Add your imports here ... '''



log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]  

''' Add your global variables here ... '''



class Firewall (EventMixin):

	def __init__ (self):
		self.listenTo(core.openflow, priority=65535)
		log.debug("Enabling Firewall Module")
		self.firewall = self.readPolicies(policyFile)

	def _handle_ConnectionUp (self, event):    

		for src, dst in self.firewall: # add flow to drop - no action

			fm = of.ofp_flow_mod()
			fm.match.dl_src = EthAddr(src)
			fm.match.dl_dst = EthAddr(dst)
			fm.match.dl_type = ethernet.IP_TYPE
			fm.match.nw_proto = ipv4.ICMP_PROTOCOL
			fm.match.tp_src=8 # ICMP echo
			event.connection.send(fm)
			

        	log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))


	def readPolicies(self,file) :
		macSet = Set()
		with open(file,'rb') as csvfile :
			fields  = csv.DictReader(csvfile)
			for row in fields:
				macSet.add( (row['mac_0'], row['mac_1']) )
		return macSet



def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
