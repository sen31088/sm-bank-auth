# Banking App Project

## Structure
- This App using a functional structure to organize the files of the project by what they do. Inside the main package, there are three more packages namely: controller, service and model.

```
|-- Design_doc.md
|-- Dockerfile
|-- app.py
|-- config.py
|-- controllers
|   |-- cards_controller.py
|   |-- fund_transfer_controller.py
|   |-- home_controller.py
|   |-- register_controller.py
|   |-- transactions_controller.py
|   `-- users_controller.py
|-- models
|   |-- __pycache__
|   |   |-- model_auth.cpython-39.pyc
|   |   |-- model_cards.cpython-39.pyc
|   |   |-- model_fund_transfer.cpython-39.pyc
|   |   |-- model_register.cpython-39.pyc
|   |   |-- model_transactions.cpython-39.pyc
|   |   `-- model_users.cpython-39.pyc
|   |-- model_auth.py
|   |-- model_cards.py
|   |-- model_fund_transfer.py
|   |-- model_register.py
|   |-- model_transactions.py
|   `-- model_users.py
|-- project_structure.md
|-- requirements.txt
|-- samp.py
|-- statements
|-- static
|   |-- backup.css
|   |-- card.png
|   |-- cards.png
|   |-- fund-trans.png
|   |-- header.jpg
|   |-- home.png
|   |-- home2.png
|   |-- logout.png
|   |-- recent-trans.png
|   |-- script.js
|   |-- sm-logo-blue .png
|   |-- sm-logo-white (3).png
|   |-- sm-logo-white .png
|   |-- style.css
|   |-- tick.png
|   `-- users-icon.png
|-- templates
|   |-- add-beneficiary-sucess.html
|   |-- add-beneficiary.html
|   |-- add-user.html
|   |-- admin-detailed-transactions.html
|   |-- admin-home.html
|   |-- admin-index.html
|   |-- admin-index1.html
|   |-- admin-recent-transactions.html
|   |-- admin-register.html
|   |-- cards.html
|   |-- del-beneficiary-sucess.html
|   |-- delete-beneficiary.html
|   |-- delete-user.html
|   |-- detailed-transactions.html
|   |-- forget-password.html
|   |-- home.html
|   |-- index.html
|   |-- info.txt
|   |-- layout.html
|   |-- mail-activation.html
|   |-- mail-otp.html
|   |-- mail-password-reset.html
|   |-- mail-register.html
|   |-- mail-suspended.html
|   |-- onetime-transfer.html
|   |-- password-reset.html
|   |-- pending-users.html
|   |-- recent-transactions.html
|   |-- register.html
|   |-- success.html
|   |-- suspend-user.html
|   |-- transfer-sucess.html
|   |-- transfer.html
|   |-- two-factor-index.html
|   |-- user-add-sucess.html
|   |-- user-delete-sucess.html
|   |-- user-details-sucess.html
|   |-- user-details.html
|   `-- user-suspend-sucess.html
|-- test.py
|-- tests
|   `-- test.py
`-- utils
    |-- sendmail.py
    `-- signature-logo.jpg

```