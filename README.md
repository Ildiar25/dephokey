
# Dephokey — PasswordManager v.1.0.0 

Dephokey — PasswordManager v.1.0.0 is an application that stores sensitive data under an encryption key within its own 
database. It avoids connecting to third-party servers, keeping all data and its credentials under the user's control, 
thus respecting their privacy. 

You can see our roadmap here: \
[![Static Badge](https://img.shields.io/badge/Dephokey-Roadmap-FB9820?logo=readdotcv&logoColor=white
)](docs/roadmap.md)

---

## User Guide

_This guide will show you which features this app has with gif examples._

### How to create a new account
To create a new account, navigate to sign up page, fill the text fields and press the submit button. The app will 
redirect you to de login page automatically.

![Create Account](docs/media/gifs/create-user.gif "How to create a new account")

---

### How to sign in on the app
To sign in, fill the text fields on main page and press the submit button. The app will redirect you to home page.

![Log in](docs/media/gifs/login.gif "How to Log in on the app")

---

### How to recover your account
**NOTE: You must have Docker installed and running on your computer before to enable this function (see the 
installation guide).** \
First, navigate to reset password and write your registered email. Then catch the email and write the sended token.
Finally, complete the text fields form and submit. Your password has been changed!

![Reset Password](docs/media/gifs/reset-password.gif "How to recover your account")

---

### How to add elements
You must choose what you want to add into database. This example shows how to add a new website.
First, click on the add button. Fill the form with necessary data and submit it. Your new site will appear on sites 
page.

![Add Site](docs/media/gifs/add-site.gif "How do add a site")

---

### How to edit elements
All widgets have an edit button. You will find it near close button. \
When you click on it, an edit form will appear. Now you can update all data and submit it. Your new info will 
appear on its page like the next example.

![Edit CreditCard](docs/media/gifs/edit-creditcard.gif "How to edit a creditcard")

---

### How to delete elements
All widgets can delete itself with delete button. \
When you click on it, a dialog alert will you ask if you want to continue and the page will be updated after it.

![Delete Note](docs/media/gifs/delete-note.gif "How to delete a note")

---

### How to send feedback
**NOTE: You must have Docker installed and running on your computer before to enable this function (see the 
installation guide).** \
First navigate to about page. Then you can fill the form and send it to our offices. Of course, it will be response 
as soon as possible!

![Feedback Email](docs/media/gifs/feedback-email.gif "How to send feedback")

---

### How to delete your account
To delete your account, navigate to settings page and click on delete account button.
A dialog alert will you ask if you want to continue and then the app will close your session and redirect to login page.

![Delete Account](docs/media/gifs/delete-account.gif "How to delete your account")

---

### Generators
This app includes some extra tools: A secure password generator and a credit card number generator. Both of them can 
be used to add new test elements to the database.

**Password Generator** \
![Password Generator](docs/media/gifs/generate-password.gif "How to generate a secure password")

**Credit Card Number Generator** \
![Credit Card Number Generator](docs/media/gifs/generate-number.gif "How to generate a credit card number")

---

## Installation Guide
First ensure you have Python v.3.11.5 or later, Git v.2.45.1 or later and Docker v28.0.1 or later 
installed on your computer (note: Docker **is not essential** for this app, it just allows you to work with emails). 
You can download them from these URLs:


[![Static Badge](https://img.shields.io/badge/Python-Download-3776AB?logo=python&logoColor=white
)](https://www.python.org/downloads/)
[![Static Badge](https://img.shields.io/badge/Git-Download-F05032?logo=git&logoColor=white
)](https://git-scm.com/downloads)
[![Static Badge](https://img.shields.io/badge/Docker-Download-2496ED?logo=docker&logoColor=white
)](https://www.docker.com/)

### 🔹 Create a folder
Open your favorite IDE, create a new folder and navigate into it
```
# Creates folder
mkdir <new_folder>

# Navigate into it
cd <new_folder>
```

---

### 🔹 Clone the repository
Once you are inside your new folder, you can clone this repo with the following command:
```
git clone https://github.com/Ildiar25/dephokey
```
This creates a new folder named `dephokey`. Navigate into it with the command `cd dephokey`.

---

### 🔹 Create a virtual environment
Now, you need a new virtual environment. To create a new one, please follow the steps below:
```bash
python -m venv .venv
```
Once it is created, activate it with the following instructions:

**From PowerShell:**
```bash
.venv\Scripts\Activate.ps1
```

**From CMD:**
```bash
.venv\Scripts\activate.bat
```

*__ATTENTION:__ When you try to activate it you can get the following message:*
```
+ .venv/Scripts/Activate.ps1
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : SecurityError: (:) [], PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess
```

That's because Windows has script execution disabled by default. \
You can solve this problem by opening Windows PowerShell in Administrator Mode and running the following command. Then 
answer _'yes'_:
```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
```

Now, you can activate the virtual environment.

---

### 🔹 Install Dependencies
This app needs some dependencies, and you can install them automatically by running the following command:
```bash
pip install -r requirements.txt
```

---

### 🔹 Start Email Server
This command opens port 1025 on localhost in detached mode (make sure Docker is running before)
```bash
docker compose -f compose.yaml up -d
```

---

### 🔹 Run Tests
Before using the app, you will need to check if all features are working correctly. To do that, you must run 
the python tests with the following command:
```bash
python -m unittest discover tests
```

---

### 🔹 Run the app
Now, your app is ready to run. Enjoy it!
```bash
flet run app.py
```

---

### 🔹 Stop the server
Once you are finished, you can stop the server with the following command:
```bash
docker compose -f compose.yaml down
```

---

![Thank You](docs/media/thank-you.jpg "Thank you very much!")

---

### About me

Hi! I'm Joan and this is my first major project! I'm learning programming since 2024, and I'm more than glad to show 
off my progress with you all! I hope you enjoyed this app as I'd enjoyed to program it thus your feedback is very 
important to me. See you on my next project and thank you very much! \
Best regards!



Joan \
Ps: You can contact me or see my works from these URLs:

[![Static Badge](https://img.shields.io/badge/LinkedIn-Profile-green)](https://www.linkedin.com/in/joan-pastor-vicens-aa5b4a55)
[![Static Badge](https://img.shields.io/badge/GitHub-Portfolio-green?logo=github&logoColor=white
)](https://github.com/Ildiar25)
