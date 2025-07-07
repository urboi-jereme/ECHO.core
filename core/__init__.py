from importlib import import_module
import sys
module = import_module('universalCode.core')
sys.modules[__name__] = module
