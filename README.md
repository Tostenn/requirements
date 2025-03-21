![logo](/image/logo.png)

![Python](https://img.shields.io/pypi/pyversions/quizen)  
# Requirements  

Who hasn’t struggled with this? 😵‍🚫 After finishing a Python project, you have to list all the libraries used, find their exact versions, and finally generate a clean `requirements.txt`. And of course, there's always a missing package or an incorrect version... A real headache! 😤  

But don't worry anymore! Requirements is here to save you. 🦸‍♂️ This tool automatically scans your project, identifies imported modules, checks installed versions, and generates a perfect `requirements.txt` in no time. ⏳✨  

No more hassle, just efficiency! 🚀  

---  

## 🎯 Installation  

```sh
git clone https://github.com/your-repo/requirements.git
cd requirements
pip install -r requirements.txt
```  

---  

## ⚙️ Usage  

Simply run the following command in your project directory:  

```sh
# requirements/
python main.py <project_folder>
```  

By default, it generates a `requirements.txt` file by analyzing all Python files in the folder.  

### 🔧 Available Options  

| Option | Description |
|--------|-------------|
| `directory` | Specifies the folder to scan (default: current directory). |
| `-f`, `--file-name` | Name of the generated requirements file (default: `requirements.txt`). |
| `--ignore-files` | List of files to ignore. |
| `--include-files` | List of files to include in the analysis. |
| `--include-self` | Includes the current script in the analysis. |
| `--ignore-modules` | List of modules to exclude. |
| `--include-modules` | List of modules to manually add. |
| `--include-modules-no-version` | Includes modules without specifying their version. |
| `-v`, `--verbose` | Enables verbose mode (detailed execution output). |
| `--version` | Displays the Requirements version. |
| `--no-logo` | Disables the logo display. |
| `--no-animation` | Disables loading animations. |
| `--case-sensitive` | Enables case sensitivity for module names. |
| `--match-module-names` | Shows matches between detected modules and installed names. |  

---  

## 🛠 Usage Examples  

### 1️⃣ Simple generation  

```sh
python main.py 
```  

Generates `requirements.txt` for the project in the current directory.  

### 2️⃣ Ignore specific files  

```sh
python -m requirements --ignore-files script_test.py config.py
```  

### 3️⃣ Add specific modules  

```sh
python -m requirements --include-modules requests numpy pandas
```  

---  

## 🏆 Why Use Requirements?  

✅ Fully automated 📌  

✅ Time-saving 🚀  

✅ No more missing modules ✅  

✅ Compatible with all Python projects  

Try it out and make your life easier! 😃  

---  

## Contribution  

Check out the [CONTRIBUTING.md](.github/CONTRIBUER.md) file to learn how to contribute to this project.