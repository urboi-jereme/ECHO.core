from importlib import import_module
import sys

# TODO: REMOVE after transition to echo_core.utils
module = import_module('universalCode.echo_core.utils')
sys.modules[__name__] = module
