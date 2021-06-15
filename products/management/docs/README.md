# python manage.py configemails

this is a custom helper command that you can use to rapidly setup your
email configuration for django to use.

just type in the command and it will guide you through the prompts.  


# manual config

create a file named `email.config.json` in the root directory. It's structure should look 
like this:

```json
{
    "username": "yourname@gmail.com",
    "password": "your_email_password",
    "admin_emails": [
        "admin1@gmail.com",
        "admin2@gmail.com",
        "admin3@gmail.com",
    ]
}
```
