from requirement import Requirement
from optparse import OptionParser
from os import getcwd
parser = OptionParser()

parser.add_option("-f", "--file-name", dest="file_name", help="Nom du fichier requirements.txt à générer", metavar="FILE_NAME")
(options, args) = parser.parse_args()
print()

if len(args) == 0:directory = getcwd()
else:directory = args[0]

req = Requirement(directory)
req.generate_requirements_txt(file_name=options.file_name)
