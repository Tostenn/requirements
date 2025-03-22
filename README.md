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


## 🔍 What’s the Difference Between `pip freeze` and Requirements?  

Many developers use `pip freeze > requirements.txt` to generate a list of dependencies. However, this method has some limitations:  

1️⃣ **Global Environment vs. Project-Specific**  
   - `pip freeze` lists **all** installed libraries in the current environment, even those not used in the project.  
   - `Requirements`, on the other hand, scans the code and detects only the **actually imported** modules.  

2️⃣ **Dependency Versions**  
   - `pip freeze` captures the exact installed version, which can cause issues if it’s not compatible with other environments.  
   - `Requirements` allows you to include or exclude versions and provides options to adjust the output according to your needs. `(future)`  

3️⃣ **Advanced Customization**  
   - With `Requirements`, you can ignore specific files, manually add modules, exclude unnecessary dependencies, and more using various options.  

📌 **Example Usage**  
```sh
# Using pip freeze (captures all environment dependencies)
pip freeze > requirements.txt

# Using Requirements (analyzes only the current project)
python main.py my_project/ --ignore-files tests.py --include-modules requests
```

In short, `pip freeze` is ideal in a dedicated environment, while `Requirements` gives you more control to generate a cleaner and more tailored requirements file for your project. 🚀

## Contribution  

Check out the [CONTRIBUTING.md](.github/CONTRIBUER.md) file to learn how to contribute to this project.