# Program:
    stockholm

# Discription:
    A simulated malware program that mimics ransomware behavior by encrypting all files
    in a target directory. The program can also reverse the encryption using a provided key.
        • The target directory must be named "infection" and located within the user’s HOME directory.
        • The provided key must be at least 16 characters long.
        • This program targets common file extensions associated with ransomware like WannaCry.

 # Installation:
    • Clone the project into your HOME directory and name the directory `infection`:
        bash stockholm [-h] [-v] [-s] [-r KEY] [KEY]
    • Install the required Python packages:
        bash stockholm [-h] [-v] [-s] [-r KEY] [KEY]
    • Set the value of SALT and IV in main.py by take the result of os.urandom():
        IV   = os.urandom(12)
        SALT = os.urandom(16+)
    • Optional set the value of key in the main.py:
        KEY = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Usege:
    bash stockholm [-h] [-v] [-s] [-r KEY] [KEY]

# Option:
| Option                  | Description                                      |
| ----------------------- | ------------------------------------------------ |
| `-h, --help`            | Show this help message and exit                  |
| `-v, --version`         | Show the version of the program                  |
| `-s, --silent`          | Run the program without producing any log output |
| `-r KEY, --reverse KEY` | Reverse the encryption using the given key       |

# Make Commands:
| Command               | Description                                                         |
| --------------------- | ------------------------------------------------------------------- |
| `make help`           | Show this help message and usage                                    |
| `make version`        | Show the version of the program                                     |
| `make silent [KEY]`   | Run the program silently (no log output), optionally provide KEY    |
| `make activate [KEY]` | Encrypt all files in the target directory using the provided KEY    |
| `make reverse [KEY]`  | Reverse the encryption using the given KEY                          |
| `make qreverse [KEY]` | Reverse the encryption silently (no log output) using the given KEY |
