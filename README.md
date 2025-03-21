![logo](/image/logo.png)

![Python](https://img.shields.io/pypi/pyversions/quizen)
# Requirements

Qui n'a jamais connu cette galère ? 😵‍🚫 Après avoir terminé un projet Python, il faut lister toutes les bibliothèques utilisées, retrouver leurs versions exactes et enfin générer un `requirements.txt` propre. Et bien sûr, il y a toujours un package manquant ou une version incorrecte... Bref, une vraie prise de tête ! 😤

Mais ne vous inquiétez plus ! Requirements est là pour vous sauver. 🦸‍♂️ Cet outil scanne automatiquement votre projet, identifie les modules importés, vérifie les versions installées et génère un `requirements.txt` parfait en un rien de temps. ⏳✨

Fini le casse-tête, place à l'efficacité ! 🚀

---

## 🎯 Installation


```sh
git clone https://github.com/votre-repo/requirements.git
cd requirements
pip install -r requirements.txt
```

---

## ⚙️ Utilisation

Exécutez simplement la commande suivante dans le répertoire de votre projet :

```sh
# requirements/
python main.py <dossier_du_projet>
```

Par défaut, il génère un fichier `requirements.txt` en analysant tous les fichiers Python du dossier.

### 🔧 Options Disponibles

| Option | Description |
|--------|-------------|
| `directory` | Spécifie le dossier à scanner (par défaut : dossier courant). |
| `-f`, `--file-name` | Nom du fichier requirements généré (par défaut : `requirements.txt`). |
| `--ignore-files` | Liste des fichiers à ignorer. |
| `--include-files` | Liste des fichiers à inclure dans l'analyse. |
| `--include-self` | Inclut le script actuel dans l'analyse. |
| `--ignore-modules` | Liste des modules à exclure. |
| `--include-modules` | Liste des modules à ajouter manuellement. |
| `--include-modules-no-version` | Inclut les modules sans spécifier leur version. |
| `-v`, `--verbose` | Active le mode verbeux (détails affichés pendant l'exécution). |
| `--version` | Affiche la version de Requirements. |
| `--no-logo` | Désactive l'affichage du logo. |
| `--no-animation` | Désactive les animations de chargement. |
| `--case-sensitive` | Active la distinction entre majuscules et minuscules pour les modules. |
| `--match-module-names` | Affiche les correspondances entre modules détectés et noms installés. |

---

## 🛠 Exemples d'utilisation

### 1️⃣ Génération simple

```sh
python main.py 
```

Génère `requirements.txt` pour le projet dans le dossier courant.

### 2️⃣ Ignorer certains fichiers

```sh
python -m requirements --ignore-files script_test.py config.py
```

### 3️⃣ Ajouter des modules spécifiques

```sh
python -m requirements --include-modules requests numpy pandas
```

---

## 🏆 Pourquoi utiliser Requirements ?

✅ Automatisation complète 📌

✅ Gain de temps 🚀

✅ Fini les oublis de modules ✅

✅ Compatible avec tous les projets Python

Essayez-le et simplifiez-vous la vie ! 😃

---

## Contribution

Consultez le fichier [CONTRIBUTING.md](.github\CONTRIBUER.md) pour savoir comment contribuer à ce projet.