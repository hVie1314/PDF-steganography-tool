#!/usr/bin/env python3
"""
PDF Steganography Tool - GUI Application
Graphical User Interface for hiding and extracting files in PDFs
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
from datetime import datetime
from pdf_stego import PDFSteganography


class PDFSteganographyGUI:
    """GUI application for PDF Steganography"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Steganography Tool")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Initialize steganography engine
        self.stego = PDFSteganography()
        
        # Configure style
        self.setup_styles()
        
        # Create GUI components
        self.create_widgets()
        
        # Center window
        self.center_window()
    
    def setup_styles(self):
        """Setup custom styles for widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Subtitle.TLabel', font=('Arial', 11, 'bold'), foreground='#34495e')
        style.configure('Info.TLabel', font=('Arial', 9), foreground='#7f8c8d')
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('Action.TButton', font=('Arial', 11, 'bold'))
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="🔒 PDF Steganography Tool",
            style='Title.TLabel'
        )
        title_label.grid(row=0, column=0, pady=(0, 5), sticky=tk.W)
        
        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="Ẩn và trích xuất dữ liệu trong file PDF",
            style='Info.TLabel'
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 15), sticky=tk.W)
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_frame.rowconfigure(2, weight=1)
        
        # Create tabs
        self.create_hide_tab()
        self.create_extract_tab()
        self.create_check_tab()
        
        # Log output area
        log_frame = ttk.LabelFrame(main_frame, text="Log Output", padding="5")
        log_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))
        main_frame.rowconfigure(3, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=8,
            width=70,
            font=('Consolas', 9),
            bg='#2c3e50',
            fg='#ecf0f1',
            wrap=tk.WORD
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar(value="Sẵn sàng")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=('Arial', 9)
        )
        status_bar.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Initial log message
        self.log_message("=== PDF Steganography Tool Started ===")
        self.log_message(f"Supported formats: {', '.join(PDFSteganography.SUPPORTED_FORMATS)}")
    
    def create_hide_tab(self):
        """Create the Hide File tab"""
        hide_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(hide_frame, text="  Ẩn File  ")
        
        # Cover PDF selection
        ttk.Label(hide_frame, text="1. Chọn file PDF gốc:", style='Subtitle.TLabel').grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        pdf_frame = ttk.Frame(hide_frame)
        pdf_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        pdf_frame.columnconfigure(0, weight=1)
        
        self.hide_pdf_var = tk.StringVar()
        ttk.Entry(pdf_frame, textvariable=self.hide_pdf_var, state='readonly').grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5)
        )
        ttk.Button(pdf_frame, text="Chọn PDF", command=self.select_hide_pdf).grid(
            row=0, column=1
        )
        
        # File to hide selection
        ttk.Label(hide_frame, text="2. Chọn file cần ẩn:", style='Subtitle.TLabel').grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        file_frame = ttk.Frame(hide_frame)
        file_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        file_frame.columnconfigure(0, weight=1)
        
        self.hide_file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.hide_file_var, state='readonly').grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5)
        )
        ttk.Button(file_frame, text="Chọn File", command=self.select_hide_file).grid(
            row=0, column=1
        )
        
        # Output PDF selection
        ttk.Label(hide_frame, text="3. Chọn vị trí lưu PDF output:", style='Subtitle.TLabel').grid(
            row=4, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        output_frame = ttk.Frame(hide_frame)
        output_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        output_frame.columnconfigure(0, weight=1)
        
        self.hide_output_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.hide_output_var, state='readonly').grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5)
        )
        ttk.Button(output_frame, text="Chọn Output", command=self.select_hide_output).grid(
            row=0, column=1
        )
        
        # Info label
        info_text = "Hỗ trợ: .txt, .jpg, .png, .pdf, .docx, .exe"
        ttk.Label(hide_frame, text=info_text, style='Info.TLabel').grid(
            row=6, column=0, sticky=tk.W, pady=(0, 15)
        )
        
        # Hide button
        ttk.Button(
            hide_frame,
            text="🔒 Ẩn File vào PDF",
            style='Action.TButton',
            command=self.hide_file_action
        ).grid(row=7, column=0, pady=(10, 0))
        
        hide_frame.columnconfigure(0, weight=1)
    
    def create_extract_tab(self):
        """Create the Extract File tab"""
        extract_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(extract_frame, text="  Trích xuất File  ")
        
        # PDF selection
        ttk.Label(extract_frame, text="1. Chọn file PDF chứa dữ liệu ẩn:", style='Subtitle.TLabel').grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        pdf_frame = ttk.Frame(extract_frame)
        pdf_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        pdf_frame.columnconfigure(0, weight=1)
        
        self.extract_pdf_var = tk.StringVar()
        ttk.Entry(pdf_frame, textvariable=self.extract_pdf_var, state='readonly').grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5)
        )
        ttk.Button(pdf_frame, text="Chọn PDF", command=self.select_extract_pdf).grid(
            row=0, column=1
        )
        
        # Output directory selection
        ttk.Label(extract_frame, text="2. Chọn thư mục lưu file trích xuất:", style='Subtitle.TLabel').grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        dir_frame = ttk.Frame(extract_frame)
        dir_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        dir_frame.columnconfigure(0, weight=1)
        
        self.extract_dir_var = tk.StringVar()
        ttk.Entry(dir_frame, textvariable=self.extract_dir_var, state='readonly').grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5)
        )
        ttk.Button(dir_frame, text="Chọn Thư mục", command=self.select_extract_dir).grid(
            row=0, column=1
        )
        
        # Info display
        self.extract_info_frame = ttk.LabelFrame(extract_frame, text="Thông tin file ẩn", padding="10")
        self.extract_info_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.extract_info_label = ttk.Label(
            self.extract_info_frame,
            text="Chọn file PDF để xem thông tin...",
            style='Info.TLabel',
            justify=tk.LEFT
        )
        self.extract_info_label.grid(row=0, column=0, sticky=tk.W)
        
        # Extract button
        ttk.Button(
            extract_frame,
            text="🔓 Trích xuất File từ PDF",
            style='Action.TButton',
            command=self.extract_file_action
        ).grid(row=5, column=0, pady=(10, 0))
        
        extract_frame.columnconfigure(0, weight=1)
    
    def create_check_tab(self):
        """Create the Check File tab"""
        check_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(check_frame, text="  Kiểm tra File  ")
        
        # PDF selection
        ttk.Label(check_frame, text="Chọn file PDF cần kiểm tra:", style='Subtitle.TLabel').grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        pdf_frame = ttk.Frame(check_frame)
        pdf_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        pdf_frame.columnconfigure(0, weight=1)
        
        self.check_pdf_var = tk.StringVar()
        ttk.Entry(pdf_frame, textvariable=self.check_pdf_var, state='readonly').grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5)
        )
        ttk.Button(pdf_frame, text="Chọn PDF", command=self.select_check_pdf).grid(
            row=0, column=1
        )
        
        # Check button
        ttk.Button(
            check_frame,
            text="🔍 Kiểm tra PDF",
            style='Action.TButton',
            command=self.check_file_action
        ).grid(row=2, column=0, pady=(10, 15))
        
        # Result display
        self.check_result_frame = ttk.LabelFrame(check_frame, text="Kết quả kiểm tra", padding="10")
        self.check_result_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        check_frame.rowconfigure(3, weight=1)
        
        self.check_result_text = scrolledtext.ScrolledText(
            self.check_result_frame,
            height=10,
            width=60,
            font=('Arial', 10),
            wrap=tk.WORD
        )
        self.check_result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.check_result_frame.columnconfigure(0, weight=1)
        self.check_result_frame.rowconfigure(0, weight=1)
        
        check_frame.columnconfigure(0, weight=1)
    
    # ===== Helper Methods =====
    
    def log_message(self, message):
        """Add message to log output"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_status(self, message):
        """Update status bar"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def format_size(self, size_bytes):
        """Format bytes to human-readable size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    # ===== Hide Tab Methods =====
    
    def select_hide_pdf(self):
        """Select cover PDF file"""
        filename = filedialog.askopenfilename(
            title="Chọn file PDF gốc",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.hide_pdf_var.set(filename)
            self.log_message(f"Đã chọn PDF gốc: {os.path.basename(filename)}")
    
    def select_hide_file(self):
        """Select file to hide"""
        filetypes = [
            ("Text files", "*.txt"),
            ("Image files", "*.jpg *.png"),
            ("PDF files", "*.pdf"),
            ("Word files", "*.docx"),
            ("Executable files", "*.exe"),
            ("All files", "*.*")
        ]
        filename = filedialog.askopenfilename(
            title="Chọn file cần ẩn",
            filetypes=filetypes
        )
        if filename:
            self.hide_file_var.set(filename)
            size = os.path.getsize(filename)
            self.log_message(f"Đã chọn file: {os.path.basename(filename)} ({self.format_size(size)})")
    
    def select_hide_output(self):
        """Select output PDF file"""
        filename = filedialog.asksaveasfilename(
            title="Chọn vị trí lưu PDF output",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.hide_output_var.set(filename)
            self.log_message(f"Output sẽ lưu tại: {os.path.basename(filename)}")
    
    def hide_file_action(self):
        """Execute hide file operation"""
        pdf_path = self.hide_pdf_var.get()
        file_path = self.hide_file_var.get()
        output_path = self.hide_output_var.get()
        
        # Validate inputs
        if not pdf_path:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file PDF gốc!")
            return
        
        if not file_path:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file cần ẩn!")
            return
        
        if not output_path:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn vị trí lưu output!")
            return
        
        # Execute operation
        self.log_message("=" * 50)
        self.log_message("Bắt đầu ẩn file vào PDF...")
        self.update_status("Đang xử lý...")
        
        try:
            success = self.stego.hide_file(pdf_path, file_path, output_path)
            
            if success:
                self.log_message("✓ Hoàn thành!")
                self.update_status("Ẩn file thành công")
                messagebox.showinfo(
                    "Thành công",
                    f"Đã ẩn file thành công!\n\nOutput: {os.path.basename(output_path)}"
                )
            else:
                self.update_status("Lỗi khi ẩn file")
                messagebox.showerror("Lỗi", "Không thể ẩn file. Xem log để biết chi tiết.")
        
        except Exception as e:
            self.log_message(f"✗ Lỗi: {str(e)}")
            self.update_status("Lỗi")
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi:\n{str(e)}")
    
    # ===== Extract Tab Methods =====
    
    def select_extract_pdf(self):
        """Select PDF file to extract from"""
        filename = filedialog.askopenfilename(
            title="Chọn file PDF chứa dữ liệu ẩn",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.extract_pdf_var.set(filename)
            self.log_message(f"Đã chọn PDF: {os.path.basename(filename)}")
            
            # Check and display hidden file info
            self.update_extract_info(filename)
    
    def select_extract_dir(self):
        """Select output directory for extracted file"""
        dirname = filedialog.askdirectory(title="Chọn thư mục lưu file trích xuất")
        if dirname:
            self.extract_dir_var.set(dirname)
            self.log_message(f"Thư mục output: {dirname}")
    
    def update_extract_info(self, pdf_path):
        """Update information about hidden file"""
        try:
            if self.stego.check_hidden_data(pdf_path):
                info = self.stego.get_hidden_file_info(pdf_path)
                if info:
                    filename, size = info
                    info_text = f"✓ Phát hiện file ẩn:\n\nTên file: {filename}\nKích thước: {self.format_size(size)}"
                    self.extract_info_label.config(text=info_text, foreground='green')
                else:
                    self.extract_info_label.config(
                        text="✗ Không thể đọc thông tin file ẩn",
                        foreground='orange'
                    )
            else:
                self.extract_info_label.config(
                    text="✗ Không tìm thấy dữ liệu ẩn trong PDF này",
                    foreground='red'
                )
        except Exception as e:
            self.extract_info_label.config(
                text=f"✗ Lỗi: {str(e)}",
                foreground='red'
            )
    
    def extract_file_action(self):
        """Execute extract file operation"""
        pdf_path = self.extract_pdf_var.get()
        output_dir = self.extract_dir_var.get()
        
        # Validate inputs
        if not pdf_path:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file PDF!")
            return
        
        if not output_dir:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thư mục output!")
            return
        
        # Execute operation
        self.log_message("=" * 50)
        self.log_message("Bắt đầu trích xuất file từ PDF...")
        self.update_status("Đang xử lý...")
        
        try:
            extracted_path = self.stego.extract_file(pdf_path, output_dir)
            
            if extracted_path:
                self.log_message("✓ Hoàn thành!")
                self.update_status("Trích xuất thành công")
                messagebox.showinfo(
                    "Thành công",
                    f"Đã trích xuất file thành công!\n\nFile: {os.path.basename(extracted_path)}\nVị trí: {output_dir}"
                )
            else:
                self.update_status("Lỗi khi trích xuất")
                messagebox.showerror("Lỗi", "Không thể trích xuất file. Xem log để biết chi tiết.")
        
        except Exception as e:
            self.log_message(f"✗ Lỗi: {str(e)}")
            self.update_status("Lỗi")
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi:\n{str(e)}")
    
    # ===== Check Tab Methods =====
    
    def select_check_pdf(self):
        """Select PDF file to check"""
        filename = filedialog.askopenfilename(
            title="Chọn file PDF cần kiểm tra",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.check_pdf_var.set(filename)
            self.log_message(f"Đã chọn PDF: {os.path.basename(filename)}")
    
    def check_file_action(self):
        """Execute check file operation"""
        pdf_path = self.check_pdf_var.get()
        
        # Validate input
        if not pdf_path:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file PDF!")
            return
        
        # Clear previous results
        self.check_result_text.delete(1.0, tk.END)
        
        # Execute operation
        self.log_message("=" * 50)
        self.log_message("Đang kiểm tra PDF...")
        self.update_status("Đang kiểm tra...")
        
        try:
            result_text = f"File: {os.path.basename(pdf_path)}\n"
            result_text += f"Đường dẫn: {pdf_path}\n"
            result_text += f"Kích thước: {self.format_size(os.path.getsize(pdf_path))}\n"
            result_text += "\n" + "=" * 50 + "\n\n"
            
            if self.stego.check_hidden_data(pdf_path):
                info = self.stego.get_hidden_file_info(pdf_path)
                if info:
                    filename, size = info
                    result_text += "KẾT QUẢ: ✓ PHÁT HIỆN DỮ LIỆU ẨN\n\n"
                    result_text += f"Tên file ẩn: {filename}\n"
                    result_text += f"Kích thước file ẩn: {self.format_size(size)}\n"
                    result_text += f"Định dạng: {os.path.splitext(filename)[1]}\n"
                    
                    self.log_message(f"✓ Phát hiện file ẩn: {filename}")
                else:
                    result_text += "KẾT QUẢ: ⚠ Phát hiện dữ liệu ẩn nhưng không đọc được thông tin\n"
                    self.log_message("⚠ Không đọc được thông tin file ẩn")
            else:
                result_text += "KẾT QUẢ: ✗ KHÔNG PHÁT HIỆN DỮ LIỆU ẨN\n\n"
                result_text += "PDF này không chứa dữ liệu ẩn hoặc chưa được xử lý\nbởi công cụ này."
                self.log_message("✗ Không phát hiện dữ liệu ẩn")
            
            self.check_result_text.insert(1.0, result_text)
            self.update_status("Kiểm tra hoàn tất")
        
        except Exception as e:
            error_text = f"LỖI KHI KIỂM TRA:\n\n{str(e)}"
            self.check_result_text.insert(1.0, error_text)
            self.log_message(f"✗ Lỗi: {str(e)}")
            self.update_status("Lỗi")
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi:\n{str(e)}")


def main():
    """Main entry point for GUI application"""
    root = tk.Tk()
    app = PDFSteganographyGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
