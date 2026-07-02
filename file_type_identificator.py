import os
from pathlib import Path
import readline  
import sys

SIGNATURES = [
    ("000000186674797A6D703432", "MP4 video file (.mp4)"),
    ("0000000C6A5020200D0A", "JPEG 2000 graphic file (.jp2)"),
    ("526172211A0700", "RAR archive (.rar)"),
    ("4D6963726F736F667420566973756F6C", "Visual Studio Solution (.sln)"),
    ("2521504F532D41646F62652D332E30", "EPS file (.eps)"),
    ("504B0304140008000800", "JAR archive (.jar)"),
    ("5374616E64617264204A6574", "Microsoft Access Database (.mdb)"),
    ("2142444E42", "Outlook PST file (.pst)"),
    ("7B5C72746631", "RTF document (.rtf)"),
    ("4B444D56", "VMWare disk file (.vmdk)"),
    ("3F5F0300", "Windows Help file (.hlp)"),
    ("4D534346", "CAB installer file (.cab)"),
    ("4D546864", "MIDI file (.mid)"),
    ("38425053", "Photoshop file (.psd)"),
    ("7F454C46", "ELF executable (Linux)"),
    ("89504E47", "PNG image (.png)"),
    ("47494638", "GIF image (.gif)"),
    ("CAFEBABE", "Java class file (.class)"),
    ("D7CDC69A", "Windows Meta File (.wmf)"),
    ("3026B2758E66CF", "ASF container (.wmv/.wma)"),
    ("1F8B08", "GZip archive (.gz)"),
    ("7573746172", "Tar archive (.tar)"),
    ("465753", "Flash SWF (.swf)"),
    ("464C56", "Flash Video (.flv)"),
    ("494433", "MP3 with ID3 tag (.mp3)"),
    ("00000100", "Icon file (.ico)"),
    ("789C", "Zlib-compressed stream (.zlib/.sdf)"),
    ("2521", "PostScript file (.ps)"),
    ("424D", "Bitmap image (.bmp)"),
    ("4949", "TIFF image (.tif)"),
    ("504B0304", "ZIP-based container (zip/docx/xlsx/pptx/apk/jar)"),
    ("D0CF11E0A1B11AE1", "OLE2/CFB container (doc/xls/ppt/vsd/msi/msg)"),
    ("52494646", "RIFF container (wav/avi)"),
    ("25504446", "PDF-based file (pdf/ai)"),
    ("4D5A", "PE executable (exe/dll/sys)"),
    ("4C01", "Object code file (.obj)"),
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

from pathlib import Path

class FileIdentifier:
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

    def read_path(self) -> str:
        readline.set_pre_input_hook(self.pre_input)
        user_input = input(f"{Color.YELLOW}>{Color.RESET} File path: ")
        
        readline.set_pre_input_hook()
        return user_input
    
    def show_menu(self):
        self.clear()
        print(BANNER)
    
    def run(self):
        while True:
            self.show_menu()
            choice = self.read_path()
            
            if choice.lower() in ('exit', 'quit', 'q'):
                print(f"\n{Color.CYAN}Goodbye!{Color.RESET}\n")
                break
                
            if not choice:
                continue
                
            
            result = self.file.read_and_return_type(choice)
            print(f"\n{Color.GREEN}File Type: {Color.BOLD}{result}{Color.RESET}")
            self.pause()

def main():
    try: 
        CLI().run()
    except KeyboardInterrupt:
        print(f"\n\n{Color.CYAN}Interrupted. Goodbye.{Color.RESET}\n")
        sys.exit(0)
        
if __name__ == "__main__":
    main()