#!/usr/bin/env python3
# PDF Slide Guard
# Copyright (c) 2025 Kenshi Muto
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the MIT License.

import argparse
import fitz
import pypdf
from pypdf.generic import RectangleObject
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import os
from typing import List
import logging

logger = logging.getLogger(__name__)
DEFAULT_FONT_ALIAS = 'JapaneseGothic'

def setup_japanese_font(font_path: str, default_alias: str) -> str:
    """Registers the Japanese font and returns the alias to be used."""
    current_alias = default_alias

    if os.path.exists(font_path):
        try:
            pdfmetrics.registerFont(TTFont(current_alias, font_path))
            pdfmetrics.registerFontFamily(current_alias, normal=current_alias)
            logger.info(f"Registered Japanese font '{current_alias}' from '{font_path}'.")
            return current_alias
        except Exception as e:
            logger.error(f"Failed to register font: {e}. Switching to default font.")
            return 'Helvetica'
    else:
        logger.warning(f"Font file not found at '{font_path}'. Using default font.")
        return 'Helvetica'


def extract_page_texts(pdf_path: str) -> List[str]:
    """Extracts text from the PDF pages."""
    doc = fitz.open(pdf_path)
    page_texts: List[str] = []

    for page in doc:
        # 'text' mode and sort=True for logical reading order
        text = page.get_text('text', sort=True)
        page_texts.append(text)
    doc.close()
    logger.info(f"Extracted text from {len(page_texts)} pages.")
    return page_texts

def convert_to_high_res_image_pdf(input_pdf_path: str, temp_output_pdf_path: str, zoom_factor: float, jpg_quality: int):
    """Converts PDF pages to high-resolution images and saves them into a new PDF with original page size."""
    doc = fitz.open(input_pdf_path)
    new_doc = fitz.open()

    logger.info(f"Generating high-resolution image PDF (Zoom x{zoom_factor:.1f})...")
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        mat = fitz.Matrix(zoom_factor, zoom_factor)
        pix = page.get_pixmap(matrix=mat)

        scaled_width = pix.width / zoom_factor
        scaled_height = pix.height / zoom_factor

        img_bytes = pix.tobytes(output='jpeg', jpg_quality=jpg_quality)
        temp_page = new_doc.new_page(width=scaled_width * zoom_factor, height=scaled_height * zoom_factor)
        temp_page.insert_image(temp_page.rect, stream=img_bytes)

    new_doc.save(temp_output_pdf_path)
    new_doc.close()
    doc.close()
    logger.info(f"Saved high-resolution image PDF to temporary file: {temp_output_pdf_path}")

    return zoom_factor

def create_transparent_text_overlay(text: str, page_width: float, page_height: float, font_name: str) -> pypdf.PdfReader:
    """Creates a PDF overlay with transparent text."""
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=(page_width, page_height))

    # Set transparency: Black (K=1) with alpha=0 (invisible)
    can.setFillColorCMYK(0, 0, 0, 1, alpha=0)

    # Use the registered font
    # Note: Font size 0.1 is extremely small and primarily for searchability/metadata, not visual rendering
    can.setFont(font_name, 0.1)

    # Write text (position is arbitrary for non-coordinate-based overlay)
    # ReportLab coordinate system is bottom-left (0, 0)
    can.drawString(50, page_height - 50, text)

    can.showPage()
    can.save()
    packet.seek(0)

    return pypdf.PdfReader(packet)


def apply_search_layer(base_pdf_path: str, text_list: List[str], output_pdf_path: str, font_name: str, keep_size: bool, zoom_factor: float):
    """Overlays the transparent text layer onto the image PDF."""
    logger.info("Overlaying transparent text and finalizing file...")
    base_reader = pypdf.PdfReader(base_pdf_path)
    writer = pypdf.PdfWriter()

    for i, page_text in enumerate(text_list):
        if i >= len(base_reader.pages):
            logger.warning("Extracted text pages exceeded base PDF page count.")
            break

        base_page = base_reader.pages[i]

        page_width = float(base_page.mediabox[2])
        page_height = float(base_page.mediabox[3])

        if keep_size:
            final_width = page_width / zoom_factor
            final_height = page_height / zoom_factor
            scale_factor = 1.0 / zoom_factor
        else:
            final_width = page_width
            final_height = page_height
            scale_factor = 1.0

        # Create the transparent text overlay
        overlay_pdf = create_transparent_text_overlay(page_text, final_width, final_height, font_name)
        overlay_page = overlay_pdf.pages[0]

        # Merge the transparent layer onto the high-res image page
        base_page.scale_by(scale_factor)
        base_page.mediabox = RectangleObject([0, 0, final_width, final_height])
        base_page.cropbox = RectangleObject([0, 0, final_width, final_height])

        base_page.merge_page(overlay_page)
        writer.add_page(base_page)

    with open(output_pdf_path, 'wb') as output_file:
        writer.write(output_file)

        logger.info(f"Final searchable PDF saved to: {output_pdf_path}")


def main():
    parser = argparse.ArgumentParser(
        description='A workaround tool to convert PDFs into high-resolution, searchable image-based PDFs.',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        'input_pdf',
        type=str,
        help='Input PDF file path.'
    )
    parser.add_argument(
        'output_pdf',
        type=str,
        help='Output PDF file path.'
    )

    parser.add_argument(
        '-z', '--zoom_factor',
        type=float,
        default=3.0,
        help='Zoom factor for high-resolution image conversion (default: 3.0).'
    )

    parser.add_argument(
        '-j', '--jpeg_quality',
        type=int,
        default=85,
        help='JPEG image quality (1-100). Lower values result in smaller file sizes (default: 85).'
    )

    parser.add_argument(
        '-k', '--keep_size',
        action='store_true',
        help='Output PDF retains the original size.'
    )

    parser.add_argument(
        '-f', '--font_path',
        type=str,
        default='/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf',
        help='Path to the Japanese TrueType/OpenType font file (e.g., ipaexg.ttf).'
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress INFO messages and only show WARNING/ERROR/FATAL logs.'
    )

    args = parser.parse_args()
    temp_img_pdf = f"{args.output_pdf}.temp.pdf"

    if args.quiet:
        log_level = logging.WARNING
    else:
        log_level = logging.INFO

    logging.basicConfig(
        level=log_level,
        format='%(levelname)s: %(message)s'
    )

    try:
        # 1. Japanese Font Setup
        used_font_alias = setup_japanese_font(args.font_path, DEFAULT_FONT_ALIAS)
        # 2. Text Extraction
        page_texts = extract_page_texts(args.input_pdf)
        # 3. High-Res Image PDF Generation
        used_zoom_factor = convert_to_high_res_image_pdf(args.input_pdf, temp_img_pdf, args.zoom_factor, args.jpeg_quality)
        # 4. Apply Transparent Search Layer
        size_info = "Original size will be restored." if args.keep_size else "Scaled page size will be retained."
        logger.info(f"Finalizing PDF. Size mode: {size_info}")
        apply_search_layer(temp_img_pdf, page_texts, args.output_pdf, used_font_alias, keep_size=args.keep_size, zoom_factor=used_zoom_factor)
    except Exception as e:
        logger.error(f"\nFATAL ERROR occurred. Process aborted: {e}")
    finally:
        # 5. Clean up temporary file
        if os.path.exists(temp_img_pdf):
            os.remove(temp_img_pdf)
            logger.info(f"Cleaned up temporary file '{temp_img_pdf}'.")


if __name__ == '__main__':
    main()
