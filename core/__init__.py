from importlib import import_module
import sys

# TODO: REMOVE after transition to echo_core.tools
module = import_module('universalCode.echo_core.tools')
sys.modules[__name__] = module
