"""
PDF Steganography Tool - Core Module
Hides data files inside PDF files using PDF structure manipulation
"""

import os
import struct
import base64
from typing import Tuple, Optional

class PDFSteganography:
    """
    Class for hiding and extracting files in PDF documents.
    Uses the PDF structure to append hidden data after the %%EOF marker.
    """
    
    MARKER = b"<<HIDDEN_DATA_START>>"
    MARKER_END = b"<<HIDDEN_DATA_END>>"
    SUPPORTED_FORMATS = ['.txt', '.jpg', '.png', '.pdf', '.docx', '.exe']
    
    def __init__(self):
        self.pdf_path = None
        self.hidden_file_path = None
    
    @staticmethod
    def validate_pdf(pdf_path: str) -> bool:
        """Validate if the file is a valid PDF"""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"File not found: {pdf_path}")
        
        with open(pdf_path, 'rb') as f:
            header = f.read(5)
            if header != b'%PDF-':
                raise ValueError("Not a valid PDF file")
        return True
    
    @staticmethod
    def validate_file_format(file_path: str) -> bool:
        """Validate if the file format is supported"""
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in PDFSteganography.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported file format: {ext}. Supported formats: {', '.join(PDFSteganography.SUPPORTED_FORMATS)}")
        return True
    
    def hide_file(self, pdf_path: str, file_to_hide: str, output_path: str) -> bool:
        """
        Hide a file inside a PDF document
        
        Args:
            pdf_path: Path to the cover PDF file
            file_to_hide: Path to the file to be hidden
            output_path: Path for the output PDF with hidden data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate inputs
            self.validate_pdf(pdf_path)
            self.validate_file_format(file_to_hide)
            
            if not os.path.exists(file_to_hide):
                raise FileNotFoundError(f"File to hide not found: {file_to_hide}")
            
            # Read the PDF content
            with open(pdf_path, 'rb') as pdf_file:
                pdf_content = pdf_file.read()
            
            # Read the file to hide
            with open(file_to_hide, 'rb') as hidden_file:
                hidden_data = hidden_file.read()
            
            # Get original filename and extension
            original_filename = os.path.basename(file_to_hide)
            
            # Prepare metadata
            filename_bytes = original_filename.encode('utf-8')
            filename_length = len(filename_bytes)
            data_length = len(hidden_data)
            
            # Create the hidden data package
            # Format: [filename_length(4 bytes)][filename][data_length(4 bytes)][data]
            hidden_package = (
                struct.pack('<I', filename_length) +
                filename_bytes +
                struct.pack('<I', data_length) +
                hidden_data
            )
            
            # Find the last %%EOF marker
            eof_marker = b'%%EOF'
            eof_position = pdf_content.rfind(eof_marker)
            
            if eof_position == -1:
                raise ValueError("Invalid PDF: %%EOF marker not found")
            
            # Insert hidden data after %%EOF
            # Keep everything up to and including %%EOF, then add hidden data
            modified_pdf = (
                pdf_content[:eof_position + len(eof_marker)] +
                b'\n' +
                self.MARKER +
                hidden_package +
                self.MARKER_END +
                b'\n'
            )
            
            # Write the output file
            with open(output_path, 'wb') as output_file:
                output_file.write(modified_pdf)
            
            print(f"✓ Successfully hidden '{original_filename}' ({data_length} bytes) in PDF")
            print(f"✓ Output saved to: {output_path}")
            return True
            
        except Exception as e:
            print(f"✗ Error hiding file: {str(e)}")
            return False
    
    def extract_file(self, pdf_path: str, output_dir: str) -> Optional[str]:
        """
        Extract hidden file from a PDF document
        
        Args:
            pdf_path: Path to the PDF file with hidden data
            output_dir: Directory to save the extracted file
            
        Returns:
            Path to the extracted file if successful, None otherwise
        """
        try:
            # Validate PDF
            self.validate_pdf(pdf_path)
            
            # Read the PDF content
            with open(pdf_path, 'rb') as pdf_file:
                pdf_content = pdf_file.read()
            
            # Find the hidden data markers
            start_pos = pdf_content.find(self.MARKER)
            end_pos = pdf_content.find(self.MARKER_END)
            
            if start_pos == -1 or end_pos == -1:
                raise ValueError("No hidden data found in this PDF")
            
            # Extract the hidden package
            start_pos += len(self.MARKER)
            hidden_package = pdf_content[start_pos:end_pos]
            
            # Parse the hidden package
            # Read filename length
            filename_length = struct.unpack('<I', hidden_package[0:4])[0]
            
            # Read filename
            filename = hidden_package[4:4+filename_length].decode('utf-8')
            
            # Read data length
            data_length_pos = 4 + filename_length
            data_length = struct.unpack('<I', hidden_package[data_length_pos:data_length_pos+4])[0]
            
            # Read hidden data
            data_start_pos = data_length_pos + 4
            hidden_data = hidden_package[data_start_pos:data_start_pos+data_length]
            
            # Validate extracted data length
            if len(hidden_data) != data_length:
                raise ValueError("Data corruption detected: extracted data length mismatch")
            
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Write the extracted file
            output_path = os.path.join(output_dir, filename)
            
            # Handle duplicate filenames
            counter = 1
            base_name, ext = os.path.splitext(filename)
            while os.path.exists(output_path):
                output_path = os.path.join(output_dir, f"{base_name}_{counter}{ext}")
                counter += 1
            
            with open(output_path, 'wb') as output_file:
                output_file.write(hidden_data)
            
            print(f"✓ Successfully extracted '{filename}' ({data_length} bytes)")
            print(f"✓ Saved to: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"✗ Error extracting file: {str(e)}")
            return None
    
    def check_hidden_data(self, pdf_path: str) -> bool:
        """
        Check if a PDF contains hidden data
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            True if hidden data exists, False otherwise
        """
        try:
            self.validate_pdf(pdf_path)
            
            with open(pdf_path, 'rb') as pdf_file:
                pdf_content = pdf_file.read()
            
            return self.MARKER in pdf_content and self.MARKER_END in pdf_content
            
        except Exception as e:
            print(f"✗ Error checking PDF: {str(e)}")
            return False
    
    def get_hidden_file_info(self, pdf_path: str) -> Optional[Tuple[str, int]]:
        """
        Get information about hidden file without extracting it
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Tuple of (filename, file_size) if hidden data exists, None otherwise
        """
        try:
            self.validate_pdf(pdf_path)
            
            with open(pdf_path, 'rb') as pdf_file:
                pdf_content = pdf_file.read()
            
            start_pos = pdf_content.find(self.MARKER)
            end_pos = pdf_content.find(self.MARKER_END)
            
            if start_pos == -1 or end_pos == -1:
                return None
            
            start_pos += len(self.MARKER)
            hidden_package = pdf_content[start_pos:end_pos]
            
            # Read filename length and filename
            filename_length = struct.unpack('<I', hidden_package[0:4])[0]
            filename = hidden_package[4:4+filename_length].decode('utf-8')
            
            # Read data length
            data_length_pos = 4 + filename_length
            data_length = struct.unpack('<I', hidden_package[data_length_pos:data_length_pos+4])[0]
            
            return (filename, data_length)
            
        except Exception as e:
            print(f"✗ Error reading hidden file info: {str(e)}")
            return None


if __name__ == "__main__":
    # Simple test
    stego = PDFSteganography()
    print("PDF Steganography Tool - Core Module")
    print(f"Supported formats: {', '.join(PDFSteganography.SUPPORTED_FORMATS)}")
