```
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
          Classical File Type Analysis with Magic Numbers Toolkit
```

A command-line tool for identifying the real type of a file by reading its **magic bytes** (file signature) instead of trusting its extension — useful for spotting disguised, mislabeled, or spoofed files.

## Features

- Detects file type by matching the binary header against a database of 30+ known magic byte signatures (PNG, PDF, ZIP-based formats, PE executables, ELF binaries, OLE2/CFB containers, archives, media files, and more)
- Single file check — reads the header and reports the detected file type
- Recursive directory scan — walks an entire directory tree and flags files whose extension doesn't match their detected type
- Live progress bar while scanning large directories
- Handles unknown signatures gracefully by dumping the first bytes in hex for manual inspection
- Colored, menu-driven CLI (ANSI escape codes)

## Requirements

- Python 3.8+
- No external dependencies

## Usage

Run from source:

```bash
python file_identifier.py
```

Then choose an option from the menu:

```
1  Verify a file
2  Verify each parent file of a dir
0  Exit
```

## How magic byte detection works

Most file formats start with a fixed sequence of bytes — a **signature** or "magic number" — that identifies the format regardless of what extension the file was given. A `.jpg` renamed to `.txt` still starts with the same JPEG header, and a Windows executable disguised as a `.pdf` still starts with `MZ`, not `%PDF`. This tool reads only the first bytes of each file (no need to load the whole thing into memory) and compares them against a signature table to determine the file's real type, then — in directory mode — cross-checks that against the extension currently on disk to surface mismatches.

Note: signature matching identifies *format*, not *safety* — a correctly identified file can still be malicious. This tool is meant as a triage/recon aid, not a full file-analysis or antivirus solution.
