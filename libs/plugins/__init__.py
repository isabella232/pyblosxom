# vim: tabstop=4 shiftwidth=4
import os, glob

def load_plugins(py, entryList):
	"""
	Loads plugins from this directory and binds them to the py
	dict.
	"""
	index = __file__.rfind(os.sep)
	if index == -1:
		path = "." + os.sep
	else:
		path = __file__[:index]

	_module_list = glob.glob( os.path.join(path, "*.py"))

	for mem in _module_list:
		mem2 = mem[mem.rfind(os.sep)+1:mem.rfind(".")]

		# we skip modules whose names start with an _ .  this
		# allows people to test stuff without having to move
		# it in and out of a directory.
		if mem2[0] == "_":
			continue

		try:
			name = "libs.plugins." + mem2
			_module = __import__(name)
			for comp in name.split(".")[1:]:
				_module = getattr(_module, comp)

			# if the module has a load function, we call it
			# with our py dict so it can bind itself to variable
			# names of its own accord

			if _module.__dict__.has_key("load"):
				_module.load(py, entryList)
		except SystemExit:
			raise SystemExit
		except Exception, e:
			# FIXME - we kicked up an exception--where to we spit 
			# it out to?
			print e
