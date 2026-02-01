# PDF Compressor

A desktop GUI application for compressing PDF files, built with Python and Tkinter.

<img width="509" height="443" alt="image" src="https://github.com/user-attachments/assets/2df20200-54cc-413a-9ed4-07a38baa8258" />


## Features

- Simple drag-and-drop style interface
- Three compression levels (Low, Medium, High)
- Real-time progress indicator
- Shows original vs compressed file size
- Works great with scanned documents and image-heavy PDFs

## Requirements

- **Python 3.8+**
- **Ghostscript** (handles the actual PDF compression)

## Installation

### 1. Install Ghostscript

**macOS (Homebrew):**
```bash
brew install ghostscript
```

**Ubuntu/Debian:**
```bash
sudo apt-get install ghostscript
```

**Windows:**
Download from [Ghostscript official site](https://www.ghostscript.com/releases/gsdnld.html) and add to PATH.

### 2. Clone the Repository

```bash
git clone https://github.com/sriraj/PDFcompressor_P.git
cd PDFcompressor
```

### 3. Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Running the App

```bash
python main.py
```

### How to Compress a PDF

1. Click **Browse...** to select a PDF file
2. Choose a compression level:
   - **Low**: Preserves quality (300 DPI, 95% quality)
   - **Medium**: Balanced (150 DPI, 75% quality)
   - **High**: Maximum compression (72 DPI, 50% quality)
3. Click **Compress PDF**
4. Choose where to save the compressed file
5. Wait for compression to complete
6. View the results showing original and compressed sizes

## Compression Levels Explained

| Level  | DPI | Image Quality | Best For |
|--------|-----|---------------|----------|
| Low    | 300 | 95%           | Print-quality documents |
| Medium | 150 | 75%           | General use, email attachments |
| High   | 72  | 50%           | Web upload, maximum size reduction |

## Project Structure

```
PDFcompressor/
├── main.py           # GUI application entry point
├── compressor.py     # PDF compression logic using Ghostscript
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Troubleshooting

### "Ghostscript is not installed"

Make sure Ghostscript is installed and accessible from the command line:
```bash
gs --version
```

If not found, install it using the instructions above.

### "No size change" or minimal compression

This can happen if:
- The PDF is already optimized
- The PDF is text-only (no images to compress)
- Try using **High** compression for better results

### App window doesn't appear

Ensure you're running Python 3 with Tkinter support:
```bash
python3 -c "import tkinter; print('Tkinter OK')"
```

On Linux, you may need to install Tkinter:
```bash
sudo apt-get install python3-tk
```

## Runbook

### Quick Start
```bash
cd /path/to/PDFcompressor
source venv/bin/activate
python main.py
```

### Full Setup (First Time)
```bash
# 1. Install Ghostscript
brew install ghostscript  # macOS

# 2. Navigate to project
cd /path/to/PDFcompressor

# 3. Create and activate venv
python3 -m venv venv
source venv/bin/activate

# 4. Run app
python main.py
```

### Verify Installation
```bash
# Check Ghostscript
gs --version

# Check Python
python3 --version

# Test compression module
python3 -c "from compressor import check_ghostscript_installed; print('GS:', check_ghostscript_installed())"
```

### Command-Line Compression (Advanced)

You can use the compressor module directly:

```python
from compressor import compress_pdf

result = compress_pdf(
    input_path="input.pdf",
    output_path="output.pdf",
    compression_level="high"  # low, medium, or high
)

print(f"Original: {result['original_size']} MB")
print(f"Compressed: {result['compressed_size']} MB")
print(f"Reduction: {result['reduction_percent']}%")
```

### Deactivate Virtual Environment

When done:
```bash
deactivate
```

## License

MIT License
