"""PDF Compression module using Ghostscript."""

import os
import subprocess
import shutil


def get_file_size_mb(file_path: str) -> float:
    """Get file size in megabytes."""
    return os.path.getsize(file_path) / (1024 * 1024)


def check_ghostscript_installed() -> bool:
    """Check if Ghostscript is installed."""
    return shutil.which("gs") is not None


def compress_pdf(
    input_path: str,
    output_path: str,
    compression_level: str = "medium"
) -> dict:
    """
    Compress a PDF file using Ghostscript.

    Args:
        input_path: Path to the input PDF file
        output_path: Path for the compressed output PDF
        compression_level: 'low', 'medium', or 'high'

    Returns:
        Dictionary with original_size, compressed_size (in MB), and reduction_percent
    """
    if not check_ghostscript_installed():
        raise RuntimeError(
            "Ghostscript is not installed.\n"
            "Install it with: brew install ghostscript"
        )

    original_size = get_file_size_mb(input_path)

    # Image DPI and quality settings per level
    settings = {
        "low": {
            "dpi": 300,
            "image_quality": 95,
            "pdf_setting": "/printer",
        },
        "medium": {
            "dpi": 150,
            "image_quality": 75,
            "pdf_setting": "/ebook",
        },
        "high": {
            "dpi": 72,
            "image_quality": 50,
            "pdf_setting": "/screen",
        },
    }

    level = settings.get(compression_level.lower(), settings["medium"])

    # Ghostscript command with aggressive image compression
    gs_command = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={level['pdf_setting']}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        # Image downsampling settings
        "-dDownsampleColorImages=true",
        "-dDownsampleGrayImages=true",
        "-dDownsampleMonoImages=true",
        f"-dColorImageResolution={level['dpi']}",
        f"-dGrayImageResolution={level['dpi']}",
        f"-dMonoImageResolution={level['dpi']}",
        # Image compression
        "-dColorImageDownsampleType=/Bicubic",
        "-dGrayImageDownsampleType=/Bicubic",
        "-dMonoImageDownsampleType=/Subsample",
        # JPEG quality for color/gray images
        "-dAutoFilterColorImages=false",
        "-dAutoFilterGrayImages=false",
        "-dColorImageFilter=/DCTEncode",
        "-dGrayImageFilter=/DCTEncode",
        f"-dJPEGQ={level['image_quality']}",
        # Output file
        f"-sOutputFile={output_path}",
        input_path,
    ]

    # Run Ghostscript
    result = subprocess.run(
        gs_command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        error_msg = result.stderr or result.stdout or "Unknown error"
        raise RuntimeError(f"Ghostscript error: {error_msg}")

    # Check if output file was created
    if not os.path.exists(output_path):
        raise RuntimeError("Compression failed - output file not created")

    compressed_size = get_file_size_mb(output_path)

    if original_size > 0:
        reduction_percent = ((original_size - compressed_size) / original_size) * 100
    else:
        reduction_percent = 0

    return {
        "original_size": round(original_size, 2),
        "compressed_size": round(compressed_size, 2),
        "reduction_percent": round(reduction_percent, 1),
    }
