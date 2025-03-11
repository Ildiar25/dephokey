
# Dephokey Roadmap 2024

---

## 1st Sprint

* Models
  * [x] User
  * [x] Site
  * [x] CreditCard
  * [x] Note
  * [x] PasswordRequest

* Features
  * [x] Data Encryption
  * [x] Email Management

## 2nd Sprint

* Database
  * [x] Implement ORM SQLAlchemy
  * [x] SQLite language
  * [x] Data Filler
  * [x] Implement item search

* Authentication
  * [x] Roles
  * [x] Hashing

  
# Dephokey Roadmap 2025

---

## 1st Sprint

* User Interface
  * [x] Login Page
  * [x] Signin Page
  * [x] Reset Password Page
  * [x] Home
  * [ ] Admin Page

* Navigation
  * [x] Home Content
  * [ ] Admin Content
  * [x] Sites Content
  * [x] Creditcards Content
  * [x] Notes Content
  * [x] Searchbar Results
  * [x] Settings

* Forms
  * [x] Add Item
  * [x] Edit Item
  * [x] Delete Item
  * [x] Generate Password
  * [x] Generate Creditcard Number
  * [x] Change Password

## 2nd Sprint

* HTML
  * [x] Email Template Design
  * [x] Token Generator

* User Session
  * [x] Session monitoring

---

---

# Clients (Platform)

Currently, Dephokey is only supported by **Windows Operative System**.

* [x] Windows OS
* [ ] MacOS
* [ ] Linux
* [ ] Android
* [ ] iOS
* [ ] Web

# All Models

### ◈ User
¿What is?
Attributes:
- ID:
- Role:
- Fullname:
- Email:
- Hashed Password:
- created:

Methods:
- None

### ◈ Site
¿What is?
Properties:
- ID:
- Name:
- Address:
- Username:
- Encrypted Password:
- User:
- Created:

Methods:
- None

### ◈ Note
¿What is?
Properties:
- ID:
- Title:
- Encrypted Content:
- User:
- Created

Methods:
- None

### ◈ CreditCard
¿What is?
Properties:
- ID:
- Cardholder:
- Encrypted Number:
- Encrypted CVC:
- Valid Until:
- Expired:
- Alias:
- User:
- Created:

Methods:
- None

### ◈ PasswordRequest
¿What is?
Properties:
- ID:
- Encrypted Code:
- User:
- Created:

Methods:
- None

### ◈ CreateEmail
¿What is?
Properties:
- ...

Methods:
- ...

### ◈ SendEmail
¿What is?
Properties:
- ...

Methods:
- ...

---

---

# Future Changes
* [ ] Add modify date to main models.
* [ ] Add a generic Key on Keyring. Each user will have its own encrypted key by using Generic Key.
* [ ] Admin can change creation & modify date.
* [ ] Send welcome mail and verify user email.
* [ ] Create Login class. Add third-party credentials to login (as Google, GitHub and others).
* [ ] Save database on system's directory.
* [ ] Add many creditcard types (as Debit or Credit).
* [ ] Add password security level.
