
# Dephokey Roadmap 2024

---

## 1st Sprint

* Models
  * [x] User
  * [x] Site
  * [x] Credit Card
  * [x] Note
  * [x] Password Request

* Features
  * [x] Data Encryption
  * [x] Email Management

## 2nd Sprint

* Database
  * [x] Implement ORM SQLAlchemy
  * [x] SQLite Language
  * [x] Data Filler
  * [x] Implement Item Search

* Authentication
  * [x] Roles
  * [x] Hashing

  
# Dephokey Roadmap 2025

---

## 1st Sprint

* User Interface
  * [x] Login Page
  * [x] Sign Up Page
  * [x] Reset Password Page
  * [x] Home Page
  * [x] Admin Page
  * [x] About Page

* Navigation
  * [x] Home Content
  * [x] Admin Content
  * [x] Sites Content
  * [x] Credit Cards Content
  * [x] Notes Content
  * [x] Searchbar Results
  * [x] Settings
  * [x] About

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
  * [x] Session Monitoring

---

---

# Clients (Platform)

Currently, Dephokey is only supported by **Windows Operating System**.

* [x] Windows OS
* [ ] MacOS
* [ ] Linux
* [ ] Android
* [ ] iOS
* [ ] Web

# All Models

### ◈ User
This model allows to create a user instance to work with. 

Parameters:
- ID: str || ID with 15 random characters
- Role: UserRole || Enum from different roles
- Fullname: str || The user's name
- Email: str || The user's email
- Hashed Password: str || Hashed user's password
- created: datetime || Timestamp when instance is created

Return:
- None

Methods:
- None

### ◈ Site
This model allows to create a site instance to work with. 

Parameters:
- ID: str || ID with 15 random characters
- Name: str | None || The web's name
- Address: str || Web address
- Username: str || User's username
- Encrypted Password: str || Encrypted user's site password
- User: User || Needs User instance (user session)
- Created: datetime || Timestamp when instance is created

Return:
- None

Methods:
- None

### ◈ Note
This model allows to create a note instance to work with. 

Parameters:
- ID: str || ID with 15 random characters
- Title: str | None || Note's title
- Encrypted Content: str || Encrypted note content
- User: User || Needs User instance (user session)
- Created: datetime || Timestamp when instance is created

Return:
- None

Methods:
- None

### ◈ Credit Card
This model allows to create a credit card instance to work with. 

Parameters:
- ID: str || ID with 15 random characters
- Cardholder: str || Credit card owner's name
- Encrypted Number: str || Encrypted credit card number
- Encrypted CVC: str || Encrypted credit card CVC
- Valid Until: datetime || Date when credit card expires
- Expired: bool || If it is expired, value is equal to True
- Alias: str | None || Credit card alias
- User: User || Needs User instance (user session)
- Created: datetime || Timestamp when instance is created

Return:
- None

Methods:
- None

### ◈ Password Request
This model allows to create a password request instance to work with. 

Parameters:
- ID: str || ID with 15 random characters
- Encrypted Code: str || Encrypted token
- User: User || Needs User instance (user session)
- Created: datetime || Timestamp when instance is created

Return:
- None

Methods:
- None

### ◈ Create Message
This model allows to create a message instance to work with.

Parameters:
- Style: MessageStyle || Enum from different messages
- Sender: str || User's email or app email
- Recipient: str || User's email or app email
- Subject: str | None || Message title
- Token: str | None || User's token
- Name: str | None || User's name
- Content: str | None || Body message content

Return:
- MIMEMultipart (CreateMessage) || Message with an image, plain text and HTML variations

Methods:
- Create: Callable[[], MIMEMultipart] || Returns a MIMEMultipart message object

### ◈ SendEmail
This model allows to send a message.

Attributes:
- Host: str || The host name or IP
- Port: int || Just the port
- Message: CreateMessage || The message itself

Methods:
- Send: Callable[[], bool] || Tries to connect with the given server and send the email. If sending is successful, 
  returns True, otherwise returns False.

---

# Future Changes
* [ ] Create Login class. Adds third-party credentials to Login (as Google, GitHub and others).
* [ ] Implement _remember me_ option.
* [ ] Create Password class. It shows security pass level. Controls if it is repeated. Add an expiration date.
* [ ] Add password security level.


* [ ] Add modification date to main models.
* [ ] Support multiple credit card types (as Debit or Credit).
* [ ] Add tries limit to login. 
* [ ] Send a welcome email and verify user email.
* [ ] Admin can change creation & modification date.


* [ ] Add a main key in the system's keyring. Each user will have its own encrypted key by using main key.
* [ ] Save database on system's directory.
