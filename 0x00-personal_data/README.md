# 0x00. Personal data - Back-end Authentication


## Learning Objectives

By the end of this project, you should be able to explain the following concepts without using Google:

1. Examples of Personally Identifiable Information (PII)
2. How to implement a log filter that will obfuscate PII fields
3. How to encrypt a password and verify the validity of an input password
4. How to authenticate to a database using environment variables

## Requirements

- All files will be interpreted/compiled on Ubuntu 18.04 LTS using Python 3.7.
- All files should end with a new line.
- The first line of all your files should be exactly `#!/usr/bin/env python3`.
- A `README.md` file at the root of the project folder is mandatory.
- Your code should follow the `pycodestyle` style guide (version 2.5).
- All files must be executable.
- The length of your files will be tested using `wc`.
- All modules should have documentation (verified with `python3 -c 'print(__import__("my_module").__doc__)'`).
- All classes should have documentation (verified with `python3 -c 'print(__import__("my_module").MyClass.__doc__)'`).
- All functions (inside and outside a class) should have documentation (verified with `python3 -c 'print(__import__("my_module").my_function.__doc__)'` and `python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'`).
- Documentation should be a complete sentence explaining the purpose of the module, class, or method.
- All functions should be type annotated.

## Tasks

### 0. Regex-ing

Write a function called `filter_datum` that returns the log message obfuscated.

**Arguments:**
- `fields`: A list of strings representing all fields to obfuscate.
- `redaction`: A string representing the value to replace the field with.
- `message`: A string representing the log line.
- `separator`: A string representing the character separating fields in the log line.

The function should use a regex to replace occurrences of certain field values. `filter_datum` should be less than 5 lines long and use `re.sub` to perform the substitution with a single regex.

**Example:**
```python
#!/usr/bin/env python3
"""
Main file
"""

filter_datum = __import__('filtered_logger').filter_datum

fields = ["password", "date_of_birth"]
messages = [
    "name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;",
    "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"
]

for message in messages:
    print(filter_datum(fields, 'xxx', message, ';'))
```

### 1. Log Formatter

Copy the following code into `filtered_logger.py`.

```python
import logging

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        raise NotImplementedError
```

Update the class to accept a list of strings `fields` as a constructor argument. Implement the `format` method to filter values in incoming log records using `filter_datum`. Values for fields in `fields` should be filtered. The `format` method should be less than 5 lines long.

**Example:**
```python
#!/usr/bin/env python3
"""
Main file
"""

import logging

RedactingFormatter = __import__('filtered_logger').RedactingFormatter

message = "name=Bob;email=bob@dylan.com;ssn=000-123-0000;password=bobby2019;"
log_record = logging.LogRecord("my_logger", logging.INFO, None, None, message, None, None)
formatter = RedactingFormatter(fields=("email", "ssn", "password"))
print(formatter.format(log_record))
```

### 2. Create Logger

Use `user_data.csv` for this task.

Implement a `get_logger` function that takes no arguments and returns a `logging.Logger` object. The logger should be named `user_data` and log up to `logging.INFO` level. It should not propagate messages to other loggers. It should have a `StreamHandler` with `RedactingFormatter` as the formatter. Create a tuple `PII_FIELDS` at the root of the module containing the fields from `user_data.csv` considered PII. Use it to parameterize the formatter.

**Example:**
```python
#!/usr/bin/env python3
"""
Main file
"""

import logging

get_logger = __import__('filtered_logger').get_logger
PII_FIELDS = __import__('filtered_logger').PII_FIELDS

print(get_logger.__annotations__.get('return'))
print(f"PII_FIELDS: {len(PII_FIELDS)}")
```

### 3. Connect to Secure Database

Database credentials should never be stored in code or checked into version control. Store them as environment variables on the application server. The database is protected by `PERSONAL_DATA_DB_USERNAME` (default: `root`), `PERSONAL_DATA_DB_PASSWORD` (default: `""`), and `PERSONAL_DATA_DB_HOST` (default: `localhost`). The database name is stored in `PERSONAL_DATA_DB_NAME`.

Implement a `get_db` function that returns a connector to the database (`mysql.connector.connection.MySQLConnection` object). Use the `os` module to obtain credentials from the environment and `mysql-connector-python` to connect to the MySQL database.

**Example:**
```python
#!/usr/bin/env python3
"""
Main file
"""

get_db = __import__('filtered_logger').get_db

db = get_db()
cursor = db.cursor()
cursor.execute("SELECT COUNT(*) FROM users;")
for row in cursor:
    print(row[0])
cursor.close()
db.close()
```

### 4. Read and Filter Data

Implement a `main` function that takes no arguments and returns nothing. The function will obtain a database connection using `get_db` and retrieve all rows in the `users` table, displaying each row in a filtered format.

Filtered fields: `name`, `email`, `phone`, `ssn`, `password`.

Only your `main` function should run when the module is executed.

**Example:**
```python
#!/usr/bin/env python3
"""
Main file
"""

get_db = __import__('filtered_logger').get_db

def main():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        print(row)  # Format the output according to your needs
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()
```

### 5. Encrypting Passwords

User passwords should never be stored in plain text in a database. Implement a `hash_password` function that expects a string argument `password` and returns a salted, hashed password as a byte string using the `bcrypt` package.

**Example:**
```python
#!/usr/bin/env python3
"""
Main file
"""

hash_password = __import__('encrypt_password').hash_password

password = "MyAmazingPassw0rd"
print(hash_password(password))
print(hash_password(password))
```

### 6. Check Valid Password

Implement an `is_valid` function that expects two arguments and returns a boolean.

**Arguments:**
- `hashed_password`: bytes
- `password`: string

Use `bcrypt` to validate that the provided password matches the hashed password.

**Example:**
```python
#!/usr/bin/env python3
"""
Main file
"""

hash_password = __import__('encrypt_password').hash_password
is_valid = __import__('encrypt_password').is_valid

password = "MyAmazingPassw0rd"
encrypted_password = hash_password(password)
print