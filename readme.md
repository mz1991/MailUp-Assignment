### Simple MailUP Rest Client

This project is a simple MailUp Rest Client written in Python3.
It allows you to:
- select a MailUp list
- create a new MailUp group
- Add some recipients (at least 3) to the new group
- Create a new list message
- Send the message to the previously created group

### Installation

```sh
$ git clone https://github.com/mz1991/MailUp-Assignment
$ cd MailUp-Assignment
$ nano mail_up_configuration.ini
Insert you client_id, client_secret, username and password.

$ virtualenv -p python3 virtualenvname
$ cd virtualenvname
$ ./bin/pip install -r your_path/MailUp-Assignment/requirements.txt
$ ./bin/python your_path/MailUp-Assignment/main.py
```

[Documentation](https://gist.github.com/mz1991/f3b861223e76405c5bf07dabda5e6516)