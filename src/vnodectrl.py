import os
import sys
import os.path
from optparse import OptionParser
import plugins
import utils
from plugins import *

def main(args):
	modules = []
	commands = {}
	# Locate the configuration.
	config_file = "{0}/.vnodectrl.d/3.x/vnodectrl.conf".format(os.getenv("HOME"));
	configuration = utils.getConfig(config_file)

	if configuration == False:
		print "No configuration available. Make sure everything is installed properly"
		return 1

	# Locate deployment instructions.
	configuration["deployment"] = utils.getDeploymentConfig()

	for plugin in plugins.__all__:
		module = getattr(plugins, plugin)
		modules.append(module)
		for command, options in module.COMMANDS.iteritems():
			options['module'] = module
			commands[command] = options

	parser = OptionParser()
	(options, args) = parser.parse_args()

	if len(args) > 0:
		primary_command = args[0];
		command_info = commands.get(primary_command, None);
		if command_info != None:
			plugin_class = getattr(command_info['module'], command_info['plugin'])
			plugin = plugin_class(configuration);
			plugin.execute(primary_command, args, options)
		else:
			print "Unrecognized command"

	else:
		print "Available Commands:\n"
		for command, options in commands.iteritems():
			print "{0}\t{1}".format(command, options['description']);

sys.exit(main(sys.argv))