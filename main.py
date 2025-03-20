from requirement import Requirement
from argparse import ArgumentParser
from logo import LOGO
from os import getcwd
from rich import print

parser = ArgumentParser()

parser.add_argument("-f", "--file-name", dest="file_name", help="Nom du fichier requirements.txt à générer", metavar="FILE_NAME", default="requirements.txt")
parser.add_argument("directory", nargs="?", help="Chemin du dossier à analyser", default=getcwd())

options = parser.parse_args()
directory = options.directory

print(LOGO)

req = Requirement(directory)
req.generate_requirements_txt(file_name=options.file_name)

print("✅ Fichier requirements.txt généré avec succès !")