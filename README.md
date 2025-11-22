# 🛡️ PDF Slide Guard

[日本語](README-ja.md)

## Overview

**PDF Slide Guard** is a command-line tool designed to circumvent display issues and rendering errors that occur on certain online slide-sharing websites and older PDF viewers.

It rebuilds every page of the original PDF as a **high-resolution image** without losing the original **text information**, and overlays a **searchable transparent text layer** on top.

This ensures **display compatibility** while preserving text **searchability and copy functionality**.

-----

## Features

  * **Maximum Compatibility:** Converts complex vector data (fonts, graphics, etc.) into a single image, fundamentally avoiding PDF parser errors.
  * **Searchability Preservation:** The generated PDF is text-searchable because the original text data is embedded as a transparent layer.
  * **High-Resolution Output:** Allows for free adjustment of the zoom factor and JPEG quality, balancing image quality and file size.
  * **Flexible Page Size:** To prevent degradation from re-scaling on slide sites, you can choose to either **restore the original size (`-k`)** or **retain the scaled-up size (default)** for the output.
  * **Japanese Language Support:** Supports Japanese fonts for embedding transparent text using ReportLab.

## Using Docker

Docker images are available on Docker Hub and ghcr.io.

```bash
docker pull kenshimuto/pdfslideguard:latest
```

## Installing without Docker

### 1. Install Dependencies

This tool relies on `PyMuPDF`, `pypdf`, and `ReportLab`. Install them using the provided `requirements.txt`:

```bash
pip3 install -r requirements.txt
```

### 2. Prepare Japanese Font

For embedding transparent text, a Japanese TrueType/OpenType font file is required on the system or specified path. The tool defaults to looking for IPAex Gothic (`ipaexg.ttf`).

```bash
# Example of the default path (Linux)
/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf
```

If you wish to use a different font, specify its path using the `-f` option (see Usage below).

### 3. Package Installation

Download the latest `pdfslideguard` package from the [Releases](https://www.google.com/search?q=https://github.com/kmuto/pdfslideguard/releases) page and install it using the `pip3` command.

```bash
pip3 install pdfslideguard-X.X.X.tar.gz
```

## Usage

### Basic Syntax

```bash
pdfslideguard [OPTIONS] [INPUT_PDF] [OUTPUT_PDF]
```

### Options

| Option | Argument | Default | Description |
| :--- | :--- | :--- | :--- |
| **`-z`, `--zoom_factor`** | `float` | `3.0` | Zoom factor for high-resolution rendering. Higher values yield better quality. |
| **`-j`, `--jpg_quality`** | `int` | `85` | JPEG image quality (1-100). Lower values result in smaller file sizes. |
| **`-f`, `--font_path`** | `str` | Default Path | Path to the Japanese font file (`.ttf`, `.otf`). |
| **`-q`, `--quiet`** | (Flag) | `False` | Suppresses INFO messages, showing only WARNING/ERROR logs. |
| **`-k`, `--keep_size`** | (Flag) | `False` | If set, the final PDF size will be **restored to the original dimensions**. If omitted (default), the **scaled-up page dimensions will be retained**. |

If you use the Docker image, you must mount the input and output directories as shown below to allow the container to process the files.

```bash
docker run --rm \
    -v ".:/work" \
    kenshimuto/pdfslideguard [OPTIONS] \
    /work/INPUT_PDF /work/OUTPUT_PDF
```

### Examples

#### 1. Running with Default Settings (Retaining Scaled Size)

```bash
pdfslideguard presentation_input.pdf final_output.pdf
# Result: A PDF with retained scaled dimensions and JPEG quality 85 is generated.
```

#### 2. Reducing File Size and Restoring Original Size

```bash
pdfslideguard presentation_input.pdf final_output.pdf -z 1.8 -j 70 -k
# Result: Compressed with a zoom factor of 1.8, JPEG quality 70, and the page size is restored to original dimensions.
```

#### 3. Specifying an Alternate Font Path

```bash
pdfslideguard input.pdf output.pdf -f /home/user/my_fonts/NotoSansJP-Regular.otf
```

## License

This project is licensed under the **MIT License**.

```
Copyright 2025 Kenshi Muto

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
