from os import walk
from os.path import join
from re import compile as compileRE
from sys import stdlib_module_names
from pkg_resources import working_set


class Requirement:
    def __init__(self, directory:str):
        self.directory = directory
    
    def get_python_files(self):
        """Récupère tous les fichiers Python dans le répertoire du projet."""
        python_files = []
        for root, _, files in walk(self.directory):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(join(root, file))
        return python_files
    
    def extract_imports(self, file_path):
        """Extrait les noms des modules importés dans un fichier Python."""
        import_pattern = compileRE(r"^\s*(?:import|from) (\S+)")
        imports = set()
        
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                match = import_pattern.match(line)
                if match:
                    module = match.group(1).split(".")[0]  # Prend uniquement le module principal
                    imports.add(module)
        
        return imports
    
    def filter_third_party_modules(self, imports):
        """Filtre les modules tiers (exclut les modules standards de Python)."""
        standard_libs = stdlib_module_names  # Liste des modules natifs de Python
        third_party = {mod for mod in imports if mod not in standard_libs}
        return third_party
        
    def get_installed_versions(self, modules):
        """Récupère les versions des modules installés."""
        installed_packages = {pkg.key: pkg.version for pkg in working_set}
        return {mod: installed_packages.get(mod) for mod in modules if installed_packages.get(mod)}

    def generate_requirements_txt(self, **kwargs):
        """Génère un fichier requirements.txt basé sur les modules utilisés dans le projet."""
        all_imports = set()
        
        for file in self.get_python_files():
            all_imports.update(self.extract_imports(file))
        
        third_party_modules = self.filter_third_party_modules(all_imports)
        module_versions = self.get_installed_versions(third_party_modules)
        
        name = kwargs.get("file_name") or "requirements.txt"
        
        with open(name, "w", encoding="utf-8") as f:
            for mod, version in module_versions.items():
                f.write(f"{mod}=={version}\n")
        
        print("✅ Fichier requirements.txt généré avec succès !")
