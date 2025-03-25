
# 🏁 Dephokey Roadmap 2024

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

  
# 🏁 Dephokey Roadmap 2025

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

# 💻 Clients (Platform)

Currently, Dephokey is only supported by **Windows Operating System**.

* [x] Windows OS
* [ ] MacOS
* [ ] Linux
* [ ] Android
* [ ] iOS
* [ ] Web

# 🗂️ All Models

### 👨‍💼 User
This model allows the creation of a user instance to work with. 

Parameters:
- ID: str || ID with 15 random characters
- Role: UserRole || Enum of different roles
- Fullname: str || The user's name
- Email: str || The user's email
- Hashed Password: str || The user's hashed password
- created: datetime || Timestamp of instance creation

Return:
- None

Methods:
- None

### 🌐 Site
This model allows the creation of a site instance to work with. 

Parameters:
- ID: str || ID with 15 random characters
- Name: str | None || The site's name
- Address: str || Website address
- Username: str || The user's username
- Encrypted Password: str || The user's encrypted site password
- User: User || Needs User instance (user session)
- Created: datetime || Timestamp of instance creation

Return:
- None

Methods:
- None

### 📝 Note
This model allows the creation of a note instance to work with. 

Parameters:
- ID: str || ID with 15 random characters
- Title: str | None || The note's title
- Encrypted Content: str || The encrypted note content
- User: User || Needs User instance (user session)
- Created: datetime || Timestamp of instance creation

Return:
- None

Methods:
- None

### 💳 Credit Card
This model allows the creation of a credit card instance to work with. 

Parameters:
- ID: str || ID with 15 random characters
- Cardholder: str || Credit card owner's name
- Encrypted Number: str || The encrypted credit card number
- Encrypted CVC: str || The encrypted credit card CVC
- Valid Until: datetime || Expiration date of the credit card
- Expired: bool || True if expired
- Alias: str | None || Credit card alias
- User: User || Needs User instance (user session)
- Created: datetime || Timestamp of instance creation

Return:
- None

Methods:
- None

### 🔒 Password Request
This model allows the creation of a password request instance to work with. 

Parameters:
- ID: str || ID with 15 random characters
- Encrypted Code: str || The encrypted token
- User: User || Needs User instance (user session)
- Created: datetime || Timestamp of instance creation
- Expires at: datetime || Timestamp of instance expiration

Return:
- None

Methods:
- None

### 📧 Create Message
This model allows the creation of a message instance to work with.

Parameters:
- Style: MessageStyle || Enum from different messages
- Sender: str || The user's email or the app email
- Recipient: str || The user's email or the app email
- Subject: str | None || The message title
- Token: str | None || The user's token
- Name: str | None || The user's name
- Content: str | None || The message body

Return:
- MIMEMultipart (CreateMessage) || Message with an image, plain text and HTML variations

Methods:
- Create: Callable[[], MIMEMultipart] || Returns a MIMEMultipart message object

### 📤 Send Email
This model allows sending message.

Attributes:
- Host: str || The host name or IP
- Port: int || Port number
- Message: CreateMessage || The message itself

Methods:
- Send: Callable[[], bool] || Tries to connect with the given server and send the email. If sending is successful, 
  returns True, otherwise returns False.

---

# 📅 Future Changes
* [ ] Create a Login class to support third-`party authentication (Google, GitHub, etc.).
* [ ] Implement a _Remember Me_ option for user sessions.
* [ ] Develop a Password class to evaluate password length, detect repetitions and enforce expiration dates.
* [ ] Enhance password security with additional validation measures.


* [ ] Add a modification date to all main models.
* [ ] Support multiple credit card types (as Debit or Credit).
* [ ] Implement a login attempt limit to enhance security. 
* [ ] Send a welcome email upon registration and verify user email.
* [ ] Allow admins to modify creation and modification dates.


* [ ] Introduce a master encryption key stored in the system's keyring. Each user's key will be encrypted useing 
  this master key.
* [ ] Store the database in the system's directory for better accessibility and security.
