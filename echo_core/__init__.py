from importlib import import_module
import sys
module = import_module('universalCode.echo_core')
sys.modules[__name__] = module
