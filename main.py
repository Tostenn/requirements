from requirement import Requirement
from argparse import ArgumentParser
from logo import LOGO
from os import getcwd
from rich import print
from alive_progress import alive_bar

parser = ArgumentParser()

parser.add_argument("directory", nargs="?", help="Chemin du dossier à analyser", default=getcwd())

parser.add_argument("-f", "--file-name", dest="file_name", help="Nom du fichier requirements.txt à générer", metavar="FILE_NAME", default="requirements.txt")

parser.add_argument("--ignore-files", help="Fichiers à ignorer", nargs="+", default=[])
parser.add_argument("--inclure-fichiers", help="Fichiers à inclure", nargs="+", default=[])
parser.add_argument("--inclure-me", help="Inclure le module actuel", action="store_true")

parser.add_argument("--ignore-modules", help="Modules à ignorer", nargs="+", default=[])
parser.add_argument("--inclure-modules", help="Modules à inclure", nargs="+", default=[])

parser.add_argument("-v", "--verbose", action="store_true", help="Activer le mode détaillé")
parser.add_argument("--version", action="version", version="%(prog)s 1.0")
parser.add_argument("--no-logo", action="store_true", help="Désactiver le logo")

parser.add_argument("--no-annimation", action="store_true", help="Désactiver l'animation de chargement")
parser.add_argument("--case-sensitive", action="store_true", help="Activer la sensibilité à la casse")
parser.add_argument("--matchs-name-modules", action="store_true", help="Afficher les modules correspondants")

parser.add_argument("--inclure-modules-no-version", help="Modules à inclure sans version",action="store_true")


options = parser.parse_args()
directory = options.directory

if not options.no_logo:
    print(LOGO)

req = Requirement(directory)

files = req.get_python_files(
    ignore_files=options.ignore_files,
    inclure_fichiers=options.inclure_fichiers,
    inclure_me=options.inclure_me,
    inclure_me_files=[__file__]
)

if not options.no_annimation:
    
    imports = set()
    with alive_bar(len(files), title="Analyse des fichiers Python") as bar:
        for file in files:
            if options.verbose:
                print(f"traitement: [green bold]{file}[/green bold]")
                
            imports.update(req.extract_import(file))
            bar.text = f"Analyse du fichier: {file}"
            bar()

    third_party = None
    funcs = {
        "exclusion des module natif": lambda: req.filter_third_party_modules(
            imports,
            case_sensitive=options.case_sensitive
        ),
        "correspondance des nom des module": lambda: req.match_moddules_names(third_party, case_sensitive=options.case_sensitive),
        "récuperation des version": lambda: req.get_installed_versions(
            third_party,
            inclure_modules_no_version=options.inclure_modules_no_version,
            ignore_modules=options.ignore_modules,
        ),
        f"sauvegarde du fichier {options.file_name}": lambda: req.save_requirements_txt(file_name=options.file_name, module_versions=third_party)
    }
    
    with alive_bar(len(funcs), title="Génération du fichier requirements.txt") as bar:
        for func in funcs:
            third_party = funcs[func]()
            if options.verbose:
                print(f"✅ {func}")
                
            bar.text = f"{func}"
            bar()
else:
    imports = req.extract_imports(
        files,
        ignore_modules=options.ignore_modules,
        inclure_modules=options.inclure_modules,
    )

    third_party = req.filter_third_party_modules(
        imports,
        case_sensitive=options.case_sensitive,
    )

    if options.matchs_name_modules:
        third_party = req.match_moddules_names(
            third_party,
            case_sensitive=options.case_sensitive
        )
        
    installed_versions = req.get_installed_versions(
        third_party,
        inclure_modules_no_version=options.inclure_modules_no_version,
        ignore_modules=options.ignore_modules,
    )

    req.save_requirements_txt(file_name=options.file_name, module_versions=installed_versions)
# print(installed_versions, third_party)

# req.generate_requirements_txt(file_name=options.file_name)

print("✅ Fichier requirements.txt généré avec succès !")