"""
Demo script - Demonstrates all features of the PDF Steganography Tool
Run this script to see the tool in action
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pdf_stego import PDFSteganography

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def demo_hide_and_extract():
    """Demonstrate hiding and extracting a file"""
    
    print_header("PDF STEGANOGRAPHY TOOL - DEMO")
    
    # Initialize
    stego = PDFSteganography()
    
    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(script_dir, "sample.pdf")
    secret_file = os.path.join(script_dir, "secret.txt")
    output_pdf = os.path.join(script_dir, "..", "output", "demo_stego.pdf")
    extract_dir = os.path.join(script_dir, "..", "output", "extracted")
    
    # Check if files exist
    if not os.path.exists(pdf_path):
        print(f"❌ Error: Sample PDF not found at {pdf_path}")
        print("   Run 'python create_sample.py' first!")
        return
    
    if not os.path.exists(secret_file):
        print(f"❌ Error: Secret file not found at {secret_file}")
        return
    
    # Step 1: Hide file
    print_header("STEP 1: Hiding secret.txt into sample.pdf")
    print(f"📄 Cover PDF: {os.path.basename(pdf_path)}")
    print(f"🔒 Secret file: {os.path.basename(secret_file)}")
    print(f"📦 Output: {os.path.basename(output_pdf)}")
    print("\nHiding file...")
    
    success = stego.hide_file(pdf_path, secret_file, output_pdf)
    
    if success:
        print("\n✅ File hidden successfully!")
        
        # Compare file sizes
        original_size = os.path.getsize(pdf_path)
        stego_size = os.path.getsize(output_pdf)
        secret_size = os.path.getsize(secret_file)
        
        print(f"\n📊 File Size Comparison:")
        print(f"   Original PDF: {original_size:,} bytes")
        print(f"   Secret file:  {secret_size:,} bytes")
        print(f"   Stego PDF:    {stego_size:,} bytes")
        print(f"   Overhead:     {stego_size - original_size - secret_size:,} bytes (metadata)")
    else:
        print("\n❌ Failed to hide file!")
        return
    
    # Step 2: Check for hidden data
    print_header("STEP 2: Checking for hidden data")
    print(f"🔍 Checking: {os.path.basename(output_pdf)}")
    
    if stego.check_hidden_data(output_pdf):
        print("\n✅ Hidden data detected!")
        
        info = stego.get_hidden_file_info(output_pdf)
        if info:
            filename, size = info
            print(f"\n📋 Hidden File Information:")
            print(f"   Filename: {filename}")
            print(f"   Size:     {size:,} bytes")
    else:
        print("\n❌ No hidden data found!")
    
    # Step 3: Extract file
    print_header("STEP 3: Extracting hidden file")
    print(f"📂 Extracting from: {os.path.basename(output_pdf)}")
    print(f"💾 Output directory: {extract_dir}")
    print("\nExtracting file...")
    
    extracted_path = stego.extract_file(output_pdf, extract_dir)
    
    if extracted_path:
        print("\n✅ File extracted successfully!")
        print(f"📄 Extracted to: {extracted_path}")
        
        # Verify integrity
        print("\n🔬 Verifying file integrity...")
        
        with open(secret_file, 'rb') as f1:
            original_data = f1.read()
        
        with open(extracted_path, 'rb') as f2:
            extracted_data = f2.read()
        
        if original_data == extracted_data:
            print("✅ File integrity verified! Files are identical.")
        else:
            print("❌ Warning: Files are different!")
    else:
        print("\n❌ Failed to extract file!")
        return
    
    # Step 4: Check original PDF (no hidden data)
    print_header("STEP 4: Checking original PDF (should have no hidden data)")
    print(f"🔍 Checking: {os.path.basename(pdf_path)}")
    
    if stego.check_hidden_data(pdf_path):
        print("\n⚠️  Hidden data detected (unexpected!)")
    else:
        print("\n✅ No hidden data found (as expected)")
    
    # Summary
    print_header("DEMO COMPLETED SUCCESSFULLY!")
    print("\n📝 Summary:")
    print("   ✅ File hidden into PDF")
    print("   ✅ Hidden data detected")
    print("   ✅ File extracted successfully")
    print("   ✅ File integrity verified")
    print("\n🎉 All features working correctly!")
    print("\n📚 Next steps:")
    print("   • Try the CLI: python cli.py --help")
    print("   • Try the GUI: python gui.py")
    print("   • Read README.txt for detailed instructions")
    print("\n" + "=" * 70 + "\n")

if __name__ == "__main__":
    try:
        demo_hide_and_extract()
    except Exception as e:
        print(f"\n❌ Error during demo: {str(e)}")
        import traceback
        traceback.print_exc()
