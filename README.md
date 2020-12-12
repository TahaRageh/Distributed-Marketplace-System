# Distributed-Marketplace-System
An Online marketplace system that relays on Distributed Database models and using Python and Django Framework
[Demo Video] ()

# Features
* Create a new account.
* Login to your account.
* Add/Edit/remove Items to your account to be sold specifying the needed price.
* Deposit Cash into your account to purchase items.
* Search for items for sale by other users.
* Purchase item from another user , transfering money from your account to his account and transfering the item from your account to his account.
* View your account info such as current cash balance , List of purchased items, list of sold items and items to be sold yet.
* Mange inventory of the items.
* Generate different kinds of reports such as reports about the transactions performed on the systems.

# installation
Python 3.9

Run the following commands

```
git clone https://github.com/TahaRageh/Distributed-Marketplace-System
pip install -r requirements.txt
cd dsproject
```
then run 
```
python manage.py makemigrations
python manage.py migrate
```

Everything should be ready! All that's left is to run the server via the command `python manage.py runserver` and the site will be available at http://127.0.0.1:8000.
