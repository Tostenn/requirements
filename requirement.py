from os import walk
from os.path import join
from re import compile as compileRE
from sys import stdlib_module_names
from pkg_resources import working_set
from pathlib import Path

class Requirement:
    def __init__(self, directory:str):
        self.directory = directory
        self.installed_packages = {pkg.key: pkg.version for pkg in working_set}
        
    def get_python_files(self, **kwargs):
        """Récupère tous les fichiers Python dans le répertoire du projet."""
        python_files = []
        
        ignore_files = kwargs.get("ignore_files", None)
        inclure_fichiers = kwargs.get("inclure_fichiers", None)
        
        inclure_me = kwargs.get("inclure_me", False)
        
        if inclure_me:
            inclure_me_files = kwargs.get("inclure_me_files", [])
            inclure_me_files = [*inclure_me_files, __file__]
        
        for root, _, files in walk(self.directory):
            for file in files:
                if file.endswith(".py"):
                    if ignore_files and file in ignore_files:
                        continue
                    
                    python_files.append(join(root, file))
        
        if inclure_fichiers:
            for file in inclure_fichiers:
                if Path(file).is_file():
                    python_files.append(file)
                    
        if inclure_me:
            python_files.extend(inclure_me_files)
            
        return python_files
    
    def extract_import(self, file_path):
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
    
    def extract_imports(self, files):
        """Extrait les noms des modules importés dans une liste de fichiers Python."""
        all_imports = set()
        for file in files:
            imports = self.extract_import(file)
            all_imports.update(imports)
        return all_imports
    
    def filter_third_party_modules(self, imports:list[str], **kwargs):
        """Filtre les modules tiers (exclut les modules standards de Python)."""
        standard_libs = stdlib_module_names  # Liste des modules natifs de Python
        case_sensitive = kwargs.get("case_sensitive", False)
        
        standard_libs = {mod.lower():mod for mod in standard_libs} if not case_sensitive else set(standard_libs)
        
        ignore_modules = kwargs.get("ignore_modules", [])
        inclure_modules = kwargs.get("inclure_modules", [])
        
        third_party = set()
        for mod in imports:
            if not case_sensitive:
                mod = mod.lower()
                
            if mod not in standard_libs:
                if mod in ignore_modules:
                    continue
                
                third_party.add(standard_libs.get(mod, mod))
        
        if inclure_modules:
            third_party.update(inclure_modules)
        
        return third_party
    
    def match_moddules_names(self,modules:set[str], **kwargs):
        """Retourne les noms des modules."""
        names_mod = list(self.installed_packages.keys())
        case_sensitive = kwargs.get("case_sensitive", False)
        
        modules = list(modules)
        
        for mod_index in range(len(modules)):
            mod = modules[mod_index]
            if not case_sensitive:
                mod = mod.lower()
            
            for _,name in enumerate(names_mod):
                if not case_sensitive:
                    name = name.lower()
                    
                if '_' in mod or '-' in mod:
                    if name in [mod.replace("_", "-"), mod.replace("-", "_")]:
                        modules[mod_index] = names_mod[_]
                        break
                if mod.capitalize() in name:
                    modules[mod_index] = names_mod[_]
                    break
                
                if mod in name:
                    modules[mod_index] = names_mod[_]
                    break
        return modules
            
    def get_installed_versions(self, modules, **kwargs):
        """Récupère les versions des modules installés."""
        
        inclure_modules_no_version = kwargs.get("inclure_modules_no_version", False)
        inclure_modules = kwargs.get("inclure_modules", [])
        ignore_modules = kwargs.get("ignore_modules", [])
        
        module_versions = {}
        
        for mod in modules:
            if mod in ignore_modules:
                continue
            
            if mod in inclure_modules:
                module_versions[mod] = self.installed_packages.get(mod)
                continue
            
            if mod in self.installed_packages:
                module_versions[mod] = self.installed_packages.get(mod)
            elif inclure_modules_no_version:
                module_versions[mod] = "0.0.0"
                
        return module_versions

    def generate_requirements_txt(self, **kwargs):
        """Génère un fichier requirements.txt basé sur les modules utilisés dans le projet."""
        files = self.get_python_files()
        
        all_imports = self.extract_imports(files)
        
        third_party_modules = self.filter_third_party_modules(all_imports)
        module_versions = self.get_installed_versions(third_party_modules)
        
        name = kwargs.get("file_name")
        
        self.save_requirements_txt(name, module_versions)

    def save_requirements_txt(self, file_name:str, module_versions:dict, **kwargs):
        """Sauvegarde les modules dans un fichier requirements.txt."""
        
        try:
            with open(file_name, "w", encoding="utf-8") as f:
                for mod, version in module_versions.items():
                    f.write(f"{mod}=={version}\n")
            return True
        except Exception as e:
            return False
