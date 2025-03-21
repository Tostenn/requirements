from os import walk
from os.path import join
from re import compile as compileRE
from sys import stdlib_module_names
from pkg_resources import working_set
from pathlib import Path
from rich import print

class Requirement:
    def __init__(self, directory: str, **kwargs):
        self.directory = directory
        self.file_name = kwargs.get("file_name", "requirements.txt")
        self.verbose = kwargs.get("verbose", False)
        self.ignore_files = kwargs.get("ignore_files", None)
        self.include_files = kwargs.get("include_files", None)
        self.include_self = kwargs.get("include_self", False)
        self.inclure_self_files = kwargs.get("inclure_self_files", [])
        self.ignore_modules = kwargs.get("ignore_modules", [])
        self.include_modules = kwargs.get("include_modules", [])
        self.case_sensitive = kwargs.get("case_sensitive", False)
        self.matchs_name_modules = kwargs.get("matchs_name_modules", False)
        self.include_modules_no_version = kwargs.get("include_modules_no_version", False)
        self.installed_packages = {pkg.key: pkg.version for pkg in working_set}
        
    def get_python_files(self):
        """Retrieve all Python files in the project directory."""
        python_files = []
        
        if self.include_self:
            self.inclure_self_files = [*self.inclure_self_files, __file__]
        
        for root, _, files in walk(self.directory):
            for file in files:
                if file.endswith(".py"):
                    if self.ignore_files and file in self.ignore_files:
                        if self.verbose:
                            self.verbose_output("Ignoring file", file, "warning")
                        continue
                    
                    python_files.append(join(root, file))
                    if self.verbose:
                        self.verbose_output("Adding file", file, "success")
        
        if self.include_files:
            for file in self.include_files:
                if Path(file).is_file():
                    python_files.append(file)
                    if self.verbose:
                        self.verbose_output("Including file", file, "info")
                    
        if self.include_self:
            python_files.extend(self.inclure_self_files)
            if self.verbose:
                self.verbose_output("Including self files", "All self-included files added", "info")
            
        return python_files
    
    def verbose_output(self, title, message: str, status: str = "info"):
        """Displays a formatted message if verbose mode is enabled."""
        status_colors = {
            "error": "bold red",
            "warning": "bold yellow",
            "info": "bold blue",
            "success": "bold green"
        }
        print(f"[{status_colors.get(status, 'white')}] {title}: {message}")
            
    def extract_import(self, file_path):
        """Extracts imported module names from a Python file."""
        import_pattern = compileRE(r"^\s*(?:import|from) (\S+)")
        imports = set()
        
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                match = import_pattern.match(line)
                if match:
                    module = match.group(1).split(".")[0]
                    
                    if module in self.ignore_modules:
                        if self.verbose:
                            self.verbose_output("Ignoring module", module, "warning")
                        continue
                    
                    imports.add(module)
                    if self.verbose:
                        self.verbose_output("Detected module", module, "success")
        
        if self.include_modules:
            imports.update(self.include_modules)
            if self.verbose:
                self.verbose_output("Including additional modules", "Manual additions applied", "info")
            
        return imports
    
    def extract_imports(self, files):
        """Extracts imported module names from multiple Python files."""
        all_imports = set()
        for file in files:
            if self.verbose:
                self.verbose_output("Processing file", file, "info")
                
            imports = self.extract_import(file)
            all_imports.update(imports)
        return all_imports
    
    def filter_third_party_modules(self, imports):
        """Filters out standard Python modules, keeping only third-party ones."""
        standard_libs = stdlib_module_names if self.case_sensitive else {mod.lower() for mod in stdlib_module_names}
        third_party = {mod for mod in imports if (mod.lower() if not self.case_sensitive else mod) not in standard_libs}
        
        if self.verbose:
            for mod in third_party:
                self.verbose_output("Third-party module detected", mod, "success")
        
        return third_party
    
    def get_installed_versions(self, modules):
        """Retrieves installed versions for detected modules."""
        module_versions = {}
        
        for mod in modules:
            if mod in self.ignore_modules:
                if self.verbose:
                    self.verbose_output("Ignoring module", mod, "warning")
                continue
            
            if mod in self.installed_packages:
                module_versions[mod] = self.installed_packages[mod]
                if self.verbose:
                    self.verbose_output("Module version", f"{mod} -> {self.installed_packages[mod]}", "info")
            elif self.include_modules_no_version:
                module_versions[mod] = "0.0.0"
                if self.verbose:
                    self.verbose_output("Module without version", f"{mod} -> 0.0.0", "warning")
                
        return module_versions

    def filter_third_party_modules(self, imports:list[str]):
        """Filtre les modules tiers (exclut les modules standards de Python)."""
        standard_libs = stdlib_module_names  # Liste des modules natifs de Python
        
        standard_libs = {mod.lower():mod for mod in standard_libs} if not self.case_sensitive else set(standard_libs)
        
        third_party = set()
        for mod in imports:
            if not self.case_sensitive:
                mod = mod.lower()
                
            if mod not in standard_libs:
                third_party.add(mod)
                
                if self.verbose:
                    self.verbose_output(title='third party',message=f"{mod}")
                
        return third_party
    
    def match_modules_names(self,modules:set[str]):
        """Retourne les noms des modules."""
        names_mod = list(self.installed_packages.keys())
        
        modules = list(modules)
        
        for mod_index in range(len(modules)):
            mod = modules[mod_index]
            if not self.case_sensitive:
                mod = mod.lower()
            
            for _,name in enumerate(names_mod):
                if not self.case_sensitive:
                    name = name.lower()
                    
                if '_' in mod or '-' in mod:
                    if name in [mod.replace("_", "-"), mod.replace("-", "_")]:
                        modules[mod_index] = names_mod[_]
                        
                        if self.verbose:
                            self.verbose_output(title='correspondance',message=f"{mod} -> {names_mod[_]}")
                        break
                    
                if mod.capitalize() in name:
                    modules[mod_index] = names_mod[_]
                    
                    if self.verbose:
                        self.verbose_output(title='correspondance',message=f"{mod} -> {names_mod[_]}")
                    break
                
                if mod in name:
                    modules[mod_index] = names_mod[_]
                    
                    if self.verbose:
                        self.verbose_output(title='correspondance',message=f"{mod} -> {names_mod[_]}")
                    break
        return modules
            
    def generate_requirements_txt(self):
        """Generates the requirements.txt file based on used modules."""
        files = self.get_python_files()
        all_imports = self.extract_imports(files)
        third_party_modules = self.filter_third_party_modules(all_imports)
        
        if self.matchs_name_modules:
            third_party_modules = self.match_modules_names(third_party_modules)
        
        module_versions = self.get_installed_versions(third_party_modules)
        self.save_requirements_txt(module_versions)

    def save_requirements_txt(self, module_versions:dict):
        """Saves detected modules and their versions into a requirements.txt file."""
        try:
            with open(self.file_name, "w", encoding="utf-8") as f:
                for mod, version in module_versions.items():
                    f.write(f"{mod}=={version}\n")
            if self.verbose:
                self.verbose_output("File saved", f"{self.file_name} successfully created", "success")
            return True
        except Exception as e:
            if self.verbose:
                self.verbose_output("Error saving file", str(e), "error")
            return False
