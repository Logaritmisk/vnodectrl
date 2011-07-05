from base import VnodectrlPlugin
import dns.zone
from dns.exception import DNSException
from dns.rdataclass import *
from dns.rdatatype import *

COMMANDS = {
	"dns-record-add" : {
		"description": "Add DNS record",
		"plugin": "DNSPlugin",
		"name": "bind-record-add"
	},
	"dns-record-delete" : {
		"description": "Delete DNS record.",
		"plugin": "DNSPlugin",
		"name": "dns-record-delete"
	},
	"dns-record-list" : {
		"description": "List DNS Records in zone.",
		"plugin": "DNSPlugin",
		"name": "dns-record-list"						
	}
}

class DNSPlugin(VnodectrlPlugin):
	def __init__(self, config):
		self.config = config
		
	def execute(self, cmd, args, options):
		"""
		Main dispatcher for all commands.
		"""
		self.zone = dns.zone.from_file(str(self.config['dns']['zone_file']), str(self.config['dns']['domain']))
		if cmd == "dns-record-list":
			self.listRecords()
		elif cmd == "dns-record-add":
			self.addRecord(args)
		elif cmd == "dns-record-delete":
			self.removeRecord(args)
		
	def listRecords(self):
		"""
		Print all records in the zone
		"""
		print "Records in zone:"
		for name, node in self.zone.nodes.items():
			print name
	
	def addRecord(self, args):
		"""
		Removes a record from the DNS zone file.
		"""
		# We need a few arguments for this to work. Let's make
		# sure they are all there.
		if len(args) < 4:
			print "You did not specify all the required arguments, please specify them in the following order:\n\
			<name> <type> <address>"
		name = args[1]
		type = args[2]
		address = args[3]
		
		rdataset = self.zone.find_rdataset(name, rdtype=type, create=True)
		rdata = dns.rdtypes.IN.A.A(IN, A, address=address)
		rdataset.add(rdata, ttl=86400)
		self.zone.to_file(self.config['dns']['zone_file'])
	
	def removeRecord(self, args):
		"""
		Removes a record from the DNS zone file.
		"""
		if len(args) < 2:
			print "You must specify the record you want to remove."
		name = args[1];
		self.zone.delete_node(name)
		self.zone.to_file(self.config['dns']['zone_file'])