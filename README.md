
# Dephokey — PasswordManager v.0.3.3 

Depholey — PasswordManager is an application that stores sensitive data under an encryption key within its own database. 
This allows to avoid to connect with third-party servers, keeping all data and its credentials under user's control, 
respecting its privacy.

## User guide

_\*how to use this app\*_

## Installation guide

### Folder
Open your favorite IDE, create a new folder and go inside
```
mkdir <new_folder>
```

---

### Clone repository
Once you are inside your new folder, you can clone this repo with the next command:
```
git clone https://github.com/Ildiar25/dephokey
```
This creates a new folder named ___'dephokey'___. Go inside with command `cd dephokey`

---

### Add virtual environment
Now, you need a new virtual environment. To create a new one, please follow the next step:
```bash
python -m venv .venv
```
Once it is created, activate with the following instructions:

**From PowerShell:**
```bash
.venv/Scripts/Activate.ps1
```

**From CMD:**
```bash
.venv/Scripts/activate.bat
```

*__ATTENTION:__ When you try to activate you can get the next message:*
```
+ .venv/Scripts/Activate.ps1
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : SecurityError: (:) [], PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess
```

That's because windows has script execution disabled by default.
You can solve this problem opening Windows PowerShell in administrator mode and running the next comand. Then answer 
_'yes'_:
```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
```

Now, you can activate virtual environment.

---

### Install requirements.txt
This app need some dependencies, and you can install them automatically writting the next code:

```bash
pip install -r requirements.txt
```

---

### Run tests
Before application use, you will need to check if all features are working correctly. To do that, you must run 
python tests with the following comand:

```bash
python -m unittest discover tests
```

---

### Open App
Now, our app is ready to run. Enjoy it!

```bash
flet run app.py
```
