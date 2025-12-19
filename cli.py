#!/usr/bin/env python3
"""
PDF Steganography Tool - Command Line Interface
Hide and extract files in PDF documents via CLI
"""

import argparse
import sys
import os
from pdf_stego import PDFSteganography


def format_size(size_bytes):
    """Format bytes to human-readable size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def hide_command(args):
    """Handle hide command"""
    stego = PDFSteganography()
    
    print("=" * 60)
    print("PDF STEGANOGRAPHY - HIDE FILE")
    print("=" * 60)
    print(f"Cover PDF: {args.pdf}")
    print(f"File to hide: {args.file}")
    print(f"Output PDF: {args.output}")
    print("-" * 60)
    
    success = stego.hide_file(args.pdf, args.file, args.output)
    
    if success:
        print("=" * 60)
        print("✓ OPERATION COMPLETED SUCCESSFULLY")
        print("=" * 60)
        return 0
    else:
        print("=" * 60)
        print("✗ OPERATION FAILED")
        print("=" * 60)
        return 1


def extract_command(args):
    """Handle extract command"""
    stego = PDFSteganography()
    
    print("=" * 60)
    print("PDF STEGANOGRAPHY - EXTRACT FILE")
    print("=" * 60)
    print(f"Source PDF: {args.pdf}")
    print(f"Output directory: {args.output}")
    print("-" * 60)
    
    # Check if hidden data exists
    if not stego.check_hidden_data(args.pdf):
        print("✗ No hidden data found in this PDF")
        print("=" * 60)
        return 1
    
    # Get hidden file info
    info = stego.get_hidden_file_info(args.pdf)
    if info:
        filename, size = info
        print(f"Hidden file detected: {filename} ({format_size(size)})")
        print("-" * 60)
    
    # Extract the file
    extracted_path = stego.extract_file(args.pdf, args.output)
    
    if extracted_path:
        print("=" * 60)
        print("✓ OPERATION COMPLETED SUCCESSFULLY")
        print("=" * 60)
        return 0
    else:
        print("=" * 60)
        print("✗ OPERATION FAILED")
        print("=" * 60)
        return 1


def check_command(args):
    """Handle check command"""
    stego = PDFSteganography()
    
    print("=" * 60)
    print("PDF STEGANOGRAPHY - CHECK FILE")
    print("=" * 60)
    print(f"Checking: {args.pdf}")
    print("-" * 60)
    
    try:
        if stego.check_hidden_data(args.pdf):
            info = stego.get_hidden_file_info(args.pdf)
            if info:
                filename, size = info
                print("✓ Hidden data FOUND")
                print(f"  Filename: {filename}")
                print(f"  Size: {format_size(size)}")
            else:
                print("✓ Hidden data markers found but unable to read info")
        else:
            print("✗ No hidden data found")
        
        print("=" * 60)
        return 0
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        print("=" * 60)
        return 1


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='PDF Steganography Tool - Hide and extract files in PDF documents',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Hide a file in a PDF
  python cli.py hide cover.pdf secret.txt output.pdf
  
  # Extract hidden file from PDF
  python cli.py extract stego.pdf ./extracted/
  
  # Check if PDF contains hidden data
  python cli.py check stego.pdf

Supported file formats: .txt, .jpg, .png, .pdf, .docx, .exe
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Hide command
    hide_parser = subparsers.add_parser('hide', help='Hide a file inside a PDF')
    hide_parser.add_argument('pdf', help='Cover PDF file')
    hide_parser.add_argument('file', help='File to hide')
    hide_parser.add_argument('output', help='Output PDF file with hidden data')
    hide_parser.set_defaults(func=hide_command)
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract hidden file from PDF')
    extract_parser.add_argument('pdf', help='PDF file with hidden data')
    extract_parser.add_argument('output', help='Output directory for extracted file')
    extract_parser.set_defaults(func=extract_command)
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Check if PDF contains hidden data')
    check_parser.add_argument('pdf', help='PDF file to check')
    check_parser.set_defaults(func=check_command)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    # Execute command
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
