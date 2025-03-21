from requirement import Requirement
from argparse import ArgumentParser
from logo import LOGO
from os import getcwd
from rich import print
from alive_progress import alive_bar

# Initialize argument parser
parser = ArgumentParser(description="Automatically generate a requirements.txt file for your project.")

# Directory argument
parser.add_argument(
    "directory", nargs="?", default=getcwd(),
    help="Path to the directory to scan. Defaults to the current working directory."
)

# Output file argument
parser.add_argument(
    "-f", "--file-name", dest="file_name", metavar="FILE_NAME", default="requirements.txt",
    help="Specify the name of the generated requirements file. Default: requirements.txt"
)

# File filtering options
parser.add_argument("--ignore-files", nargs="+", default=[], help="List of specific files to ignore during analysis.")
parser.add_argument("--include-files", nargs="+", default=[], help="List of specific files to include in the analysis.")
parser.add_argument("--include-self", action="store_true", help="Include the current script in the analysis.")

# Module filtering options
parser.add_argument("--ignore-modules", nargs="+", default=[], help="List of modules to exclude from the requirements file.")
parser.add_argument("--include-modules", nargs="+", default=[], help="List of modules to explicitly include in the requirements file.")
parser.add_argument("--include-modules-no-version", action="store_true", help="Include modules without specifying their version.")

# Display options
parser.add_argument("-v", "--verbose", action="store_true", help="Enable detailed output (verbose mode).")
parser.add_argument("--version", action="version", version="%(prog)s 1.0", help="Display the program version and exit.")
parser.add_argument("--no-logo", action="store_true", help="Disable the logo display.")

# Processing options
parser.add_argument("--no-animation", action="store_true", help="Disable loading animations.")
parser.add_argument("--case-sensitive", action="store_true", help="Enable case-sensitive module matching.")
parser.add_argument("--match-module-names", action="store_true", help="Show modules that match detected imports.")

# Parse command-line arguments
options = parser.parse_args()
directory = options.directory

# Display logo if not disabled
if not options.no_logo:
    print(LOGO)

# Initialize Requirement instance
req = Requirement(
    directory,
    file_name=options.file_name,
    verbose=options.verbose,
    ignore_files=options.ignore_files,
    include_files=options.include_files,
    include_self=options.include_self,
    inclure_self_files=[__file__],
    ignore_modules=options.ignore_modules,
    include_modules=options.include_modules,
    case_sensitive=options.case_sensitive,
    matchs_name_modules=options.match_module_names,
    include_modules_no_version=options.include_modules_no_version,
)

# Perform the analysis with or without animations
if not options.no_animation:
    files = req.get_python_files()
    imports = set()

    # Step 1: Scan Python files
    with alive_bar(len(files), title="🔍 Scanning Python files...") as bar:
        for file in files:
            imports.update(req.extract_import(file))
            bar.text = f"Processing file: {file}"
            bar()

    # Step 2: Generate requirements.txt
    processing_steps = {
        "Excluding standard library modules": req.filter_third_party_modules,
    }
    
    if options.match_module_names:
        processing_steps["Matching module names"] = req.match_modules_names
    
    processing_steps["Retrieving installed versions"] = req.get_installed_versions
    processing_steps["Saving requirements file"] = req.save_requirements_txt

    with alive_bar(len(processing_steps), title="⚙️ Generating requirements.txt...") as bar:
        for step, function in processing_steps.items():
            if options.verbose:
                print(f"🔹 {step}...")
            imports = function(imports)
            bar.text = step
            bar()
else:
    req.generate_requirements_txt()

print(f"\n✅ [green]{req.file_name} file successfully generated![/green] 🎉")
