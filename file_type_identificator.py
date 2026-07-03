import os
from pathlib import Path
import readline  
import sys

SIGNATURES = [
    ("000000186674797A6D703432", ".mp4", "MP4 video file"),
    ("0000000C6A5020200D0A", ".jp2", "JPEG 2000 graphic file"),
    ("526172211A0700", ".rar", "RAR archive"),
    ("4D6963726F736F667420566973756F6C", ".sln", "Visual Studio Solution"),
    ("2521504F532D41646F62652D332E30", ".eps", "EPS file"),
    ("504B0304140008000800", ".jar", "JAR archive"),
    ("5374616E64617264204A6574", ".mdb", "Microsoft Access Database"),
    ("2142444E42", ".pst", "Outlook PST file"),
    ("7B5C72746631", ".rtf", "RTF document"),
    ("4B444D56", ".vmdk", "VMWare disk file"),
    ("3F5F0300", ".hlp", "Windows Help file"),
    ("4D534346", ".cab", "CAB installer file"),
    ("4D546864", ".mid", "MIDI file"),
    ("38425053", ".psd", "Photoshop file"),
    ("7F454C46", ".elf", "ELF executable (Linux)"),
    ("89504E47", ".png", "PNG image"),
    ("47494638", ".gif", "GIF image"),
    ("CAFEBABE", ".class", "Java class file"),
    ("D7CDC69A", ".wmf", "Windows Meta File"),
    ("3026B2758E66CF", ".wmv", "ASF container (.wmv/.wma)"),
    ("1F8B08", ".gz", "GZip archive"),
    ("7573746172", ".tar", "Tar archive"),
    ("465753", ".swf", "Flash SWF"),
    ("464C56", ".flv", "Flash Video"),
    ("494433", ".mp3", "MP3 with ID3 tag"),
    ("00000100", ".ico", "Icon file"),
    ("789C", ".zlib", "Zlib-compressed stream"),
    ("2521", ".ps", "PostScript file"),
    ("424D", ".bmp", "Bitmap image"),
    ("4949", ".tif", "TIFF image"),
    ("504B0304", ".zip", "ZIP-based container (zip/docx/xlsx/pptx/apk/jar)"),
    ("D0CF11E0A1B11AE1", ".doc", "OLE2/CFB container (doc/xls/ppt/vsd/msi/msg)"),
    ("52494646", ".wav", "RIFF container (wav/avi)"),
    ("25504446", ".pdf", "PDF-based file (pdf/ai)"),
    ("4D5A", ".exe", "PE executable (exe/dll/sys)"),
    ("4C01", ".obj", "Object code file"),
]


class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    MAGENTA = "\033[35m"
    BLUE = "\033[34m"

BANNER = rf"""{Color.CYAN}{Color.BOLD}
███████╗██╗██╗     ███████╗       
██╔════╝██║██║     ██╔════╝       
█████╗  ██║██║     █████╗         
██╔══╝  ██║██║     ██╔══╝         
██║     ██║███████╗███████╗       
╚═╝     ╚═╝╚══════╝╚══════╝       
                                  
████████╗██╗   ██╗██████╗ ███████╗
╚══██╔══╝╚██╗ ██╔╝██╔══██╗██╔════╝
   ██║    ╚████╔╝ ██████╔╝█████╗  
   ██║     ╚██╔╝  ██╔═══╝ ██╔══╝  
   ██║      ██║   ██║     ███████╗
   ╚═╝      ╚═╝   ╚═╝     ╚══════╝
{Color.RESET}{Color.DIM}          Classical File Type Analysis with Magic Numbers Toolkit{Color.RESET}                    
"""

def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        print_end   - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    # Print New Line on Complete
    if iteration == total: 
        print()

class FileIdentifier:
    @staticmethod
    def get_ext_and_type(header_bytes):
        for hex, ext, desc in SIGNATURES:
            sig = bytes.fromhex(hex)
            if (header_bytes.startswith(sig)):
                return ext, desc
        return None, None

    @staticmethod
    def read_and_return_type(path: str) -> str:
        path = Path(path).expanduser()

        try:
            if not path.is_file():
                return f"{Color.RED}Error: Not a regular file{Color.RESET}"

            
            max_len = max(len(bytes.fromhex(sig)) for sig, _ in SIGNATURES)

            with path.open("rb") as f:
                header = f.read(max_len)

            for hex_sig, desc in SIGNATURES:
                sig = bytes.fromhex(hex_sig)
                if header.startswith(sig):
                    return desc

            
            hex_bytes = header[:32].hex(" ").upper()
            return (
                "Unknown file type\n"
                f"First {min(len(header),32)} bytes:\n"
                f"{hex_bytes}"
            )

        except PermissionError:
            return f"{Color.RED}Error: Permission denied{Color.RESET}"
        except Exception as e:
            return f"{Color.RED}Error: {e}{Color.RESET}"
        
    @staticmethod
    def read_and_verify_by_dir(dir: str) -> str:
        mismatched = []
        total_files = 0
        loading = True

        try:
            file_list = []

            print("Loading...")

            for (root, dirs, files) in os.walk(dir):
                for file in files:
                    file_list.append(Path(root)/file)

            total_files = len(file_list)    
            if total_files == 0:
                print(f"\n{Color.YELLOW}No files found in directory{Color.RESET}")
                return
            
            printProgressBar(0, total_files, prefix='Progress:', suffix='Complete', length=50)

            for i, full_path in enumerate(file_list):
                try:
                    max_len = max(len(bytes.fromhex(sig)) for sig,_,_ in SIGNATURES)
                    with full_path.open("rb") as f:
                        header = f.read(max_len)

                    ext, type = FileIdentifier.get_ext_and_type(header_bytes=header)
                    current_ext = full_path.suffix.lower()

                    if ext and ext != ext:
                        mismatched.append({
                            'path': full_path,
                            'current_ext': current_ext if current_ext else '(no extension)',
                            'detected_ext': ext,
                        })
                except (PermissionError, OSError) as e:
                    pass

                printProgressBar(i+1, total_files, prefix='Progress:', suffix='Complete', length=50)

            print(f"\n{Color.CYAN}{'═' * 60}{Color.RESET}")
            print(f"{Color.BOLD}Results:{Color.RESET}")
            print(f"  Total files scanned: {Color.BOLD}{total_files}{Color.RESET}")
            
            if mismatched:
                print(f"  {Color.RED}Files with mismatched extensions: {len(mismatched)}{Color.RESET}")
                print(f"\n{Color.YELLOW}Mismatched files:{Color.RESET}")
                for idx, item in enumerate(mismatched, 1):
                    print(f"\n  {Color.BOLD}{idx}.{Color.RESET} {item['path']}")
                    print(f"     Current extension: {Color.RED}{item['current_ext']}{Color.RESET}")
                    print(f"     Detected type: {Color.GREEN}{item['detected_ext']}{Color.RESET} ({item['detected_type']})")
            else:
                print(f"  {Color.GREEN}All files have matching extensions! ✓{Color.RESET}")
            
        except Exception as e:
            print(f"\n{Color.RED}Error: {e}{Color.RESET}")


        except Exception as e:
            return f"{Color.RED}Error: {e}{Color.RESET}"
    
class CLI:
    WIDTH = 60
    HOME = str(Path.home()) + "\\"
    
    def __init__(self):
        self.file = FileIdentifier()  

    @staticmethod
    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    def pause(self):
        input(f"\n{Color.DIM} Press Enter to return to the menu...{Color.RESET}")

    def pre_input(self):
        readline.insert_text(self.HOME)
        readline.redisplay()

    def read_option(self) -> str:
        readline.set_pre_input_hook(self.pre_input)
        user_input = input(f"{Color.YELLOW}>{Color.RESET} Option: ")
        
        readline.set_pre_input_hook()
        return user_input
    
    def prompt(self, msg: str) -> str:
        return input(f"{Color.YELLOW}›{Color.RESET} {msg}: ").strip()
    
    def read_path(self) -> str:
        readline.set_pre_input_hook(self.pre_input)
        user_input = input(f"{Color.YELLOW}>{Color.RESET} File path: ")
        
        readline.set_pre_input_hook()
        return user_input
    
    def read_dir(self) -> str:
        readline.set_pre_input_hook(self.pre_input)
        user_input = input(f"{Color.YELLOW}>{Color.RESET}  Directory: ")
        
        readline.set_pre_input_hook()
        return user_input
    
    def show_menu(self):
        self.clear()
        print(BANNER)
        print(f"{Color.CYAN}{'═' * self.WIDTH}{Color.RESET}")
        options = [
            ("1", "Verify a file"),
            ("2", "Verify each parent file of a dir"),
            ("0", "Exit"),
        ]
        for key, label in options:
            print(f"  {Color.BOLD}{key}{Color.RESET}  {label}")
        print(f"{Color.CYAN}{'═' * self.WIDTH}{Color.RESET}")

    def erro(self, msg: str):
        print(f"{Color.RED}X{Color.RESET} {msg}")

    def read_file(self):
        self.clear()
        path = self.read_path()
        result = self.file.read_and_return_type(path=path)
        print(f"\n{Color.GREEN}File Type: {Color.BOLD}{result}{Color.RESET}")
        self.pause()


    def read_file_from_dir(self):
        self.clear()
        dir = self.read_dir()
        result = self.file.read_and_verify_by_dir(dir=dir)
        print(f"\n{Color.GREEN}File Type: {Color.BOLD}{result}{Color.RESET}")
        self.pause()
    
    def run(self):
        actions = {
            "1": self.read_file,
            "2": self.read_file_from_dir
        }
        while True:
            self.show_menu()
            choice = self.prompt("Select an option")
            
            if choice == "0":
                print(f"\n{Color.CYAN}Goodbye!{Color.RESET}\n")
                sys.exit(0)
            
            if (choice is None):
                self.erro("Invalid option.")
                self.pause()
                continue       

            action = actions.get(choice)

            try: 
                action()
            except Exception as e:
                self.erro(f"Unexpected error: {e}")
                self.pause()

def main():
    try: 
        CLI().run()
    except KeyboardInterrupt:
        print(f"\n\n{Color.CYAN}Interrupted. Goodbye.{Color.RESET}\n")
        sys.exit(0)
        
if __name__ == "__main__":
    main()