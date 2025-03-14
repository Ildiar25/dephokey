
# Dephokey — PasswordManager v.0.3.3 

Dephokey — PasswordManager v.0.3.3 is an application that stores sensitive data under an encryption key within its own 
database. Avoids connecting to third-party servers, keeping all data and its credentials under user's control, 
thus respecting their privacy.

## User Guide

_\*how to use this app\*_

## Installation Guide
First ensure you have Python v.3.11.5 or superior, Git v.2.45.1 or superior & Docker v28.0.1 or superior 
installed on your computer. You can download it from these urls:


[![Static Badge](https://img.shields.io/badge/Python-Download-blue)](https://www.python.org/downloads/)
[![Static Badge](https://img.shields.io/badge/Git-Download-blue)](https://git-scm.com/downloads)
[![Static Badge](https://img.shields.io/badge/Docker-Download-blue)](https://www.docker.com/)

### Create Folder
Open your favorite IDE, create a new folder and navigate into it
```
# Creates folder
mkdir <new_folder>

# Navigate into it
cd <new_folder>
```

---

### Clone Repository
Once you are inside your new folder, you can clone this repo with the next command:
```
git clone https://github.com/Ildiar25/dephokey
```
This creates a new folder named `dephokey`. Navigate into it with command `cd dephokey`.

---

### Create Virtual Environment
Now, you need a new virtual environment. To create a new one, please follow the next step:
```bash
python -m venv .venv
```
Once it is created, activate with the following instructions:

**From PowerShell:**
```bash
.venv\Scripts\Activate.ps1
```

**From CMD:**
```bash
.venv\Scripts\activate.bat
```

*__ATTENTION:__ When you try to activate you can get the next message:*
```
+ .venv/Scripts/Activate.ps1
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : SecurityError: (:) [], PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess
```

That's because windows has script execution disabled by default.
You can solve this problem opening Windows PowerShell in administrator mode and running the next command. Then answer 
_'yes'_:
```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
```

Now, you can activate virtual environment.

---

### Install Dependencies
This app need some dependencies, and you can install them automatically writing the next code:
```bash
pip install -r requirements.txt
```

---

### Start Email Server
This command open 1025 port on localhost
```bash
docker compose -f compose.yaml up -d
```

---

### Run Tests
Before application use, you will need to check if all features are working correctly. To do that, you must run 
python tests with the following command:
```bash
python -m unittest discover tests
```

---

### Run App
Now, our app is ready to run. Enjoy it!
```bash
flet run app.py
```

---

### Stop Server
Once you finished, you can stop the server with next command:
```bash
docker compose -f compose.yaml down
```
