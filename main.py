
from requirement import Requirement
from optparse import OptionParser
from os import getcwd
parser = OptionParser()

(options, args) = parser.parse_args()

if len(args) == 0:directory = getcwd()
else:directory = args[0]

req = Requirement()
p = req.generate_requirements_txt(directory)
