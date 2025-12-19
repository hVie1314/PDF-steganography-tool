================================================================================
                    PDF STEGANOGRAPHY TOOL - HƯỚNG DẪN SỬ DỤNG
================================================================================

GIỚI THIỆU
----------
PDF Steganography Tool là công cụ ẩn và trích xuất dữ liệu file vào trong 
file PDF. Công cụ sử dụng kỹ thuật steganography để ẩn dữ liệu sau marker 
%%EOF của file PDF mà không làm ảnh hưởng đến nội dung hiển thị của PDF.

TÍNH NĂNG
---------
✓ Ẩn file vào trong PDF
✓ Trích xuất file ẩn từ PDF
✓ Kiểm tra xem PDF có chứa dữ liệu ẩn không
✓ Hỗ trợ nhiều định dạng file: .txt, .jpg, .png, .pdf, .docx, .exe
✓ Giao diện dòng lệnh (CLI) và giao diện đồ họa (GUI)
✓ Không làm thay đổi nội dung hiển thị của PDF

YÊU CẦU HỆ THỐNG
---------------
- Python 3.7 trở lên
- Hệ điều hành: Windows, Linux, macOS
- Thư viện Python: PyPDF2, Pillow, python-docx

CÀI ĐẶT
-------
1. Cài đặt Python (nếu chưa có):
   - Tải từ: https://www.python.org/downloads/
   - Chọn "Add Python to PATH" khi cài đặt

2. Cài đặt các thư viện cần thiết:
   Mở Command Prompt hoặc Terminal và chạy:
   
   # Di chuyển đến thư mục project
   cd <đường_dẫn_đến_thư_mục>
   
   # Cài đặt dependencies 
   pip install -r requirements.txt

3. Kiểm tra cài đặt:
   python --version
   python -c "import PyPDF2; print('PyPDF2 OK')"
   python -c "import PIL; print('Pillow OK')"
   python -c "import docx; print('python-docx OK')"

CẤU TRÚC THƯ MỤC
----------------
HW-2/
├── pdf_stego.py          # Module chính xử lý steganography
├── cli.py                # Giao diện dòng lệnh (CLI)
├── gui.py                # Giao diện đồ họa (GUI - Tkinter)
│
├── requirements.txt      # Danh sách thư viện Python cần thiết
├── .gitignore            # Git ignore file
│
├── README.MD             # File hướng dẫn này
│
├── report.pdf            # Báo cáo kỹ thuật 
│
├── samples/              # Thư mục chứa file mẫu và scripts tiện ích
│   ├── sample.pdf        # PDF mẫu để test
│   ├── secret.txt        # File text mẫu để ẩn
│   ├── demo.py           # Script demo tự động (test toàn bộ tính năng)
│   └── create_sample.py  # Script tạo file PDF mẫu
│
└── output/               # Thư mục lưu kết quả
    ├── .gitkeep          # Giữ thư mục trong Git
    └── extracted/        # Thư mục lưu file trích xuất

================================================================================
                           HƯỚNG DẪN SỬ DỤNG GUI
================================================================================

KHỞI ĐỘNG GUI
-------------
1. Mở Command Prompt hoặc Terminal

2. Di chuyển đến thư mục project:
   cd <đường_dẫn_đến_thư_mục>

3. Chạy lệnh:
   python gui.py

ẨN FILE VÀO PDF (Tab "Ẩn File")
-------------------------------
1. Nhấn "Chọn PDF" để chọn file PDF gốc (cover PDF)

2. Nhấn "Chọn File" để chọn file cần ẩn
   - Hỗ trợ: .txt, .jpg, .png, .pdf, .docx, .exe

3. Nhấn "Chọn Output" để chọn vị trí và tên file PDF đầu ra

4. Nhấn "🔒 Ẩn File vào PDF"

5. Chờ thông báo hoàn thành

Ví dụ:
- PDF gốc: document.pdf
- File cần ẩn: secret.txt
- Output: document_stego.pdf

TRÍCH XUẤT FILE TỪ PDF (Tab "Trích xuất File")
----------------------------------------------
1. Nhấn "Chọn PDF" để chọn file PDF chứa dữ liệu ẩn
   - Công cụ sẽ tự động hiển thị thông tin file ẩn nếu có

2. Nhấn "Chọn Thư mục" để chọn nơi lưu file trích xuất

3. Nhấn "🔓 Trích xuất File từ PDF"

4. File được trích xuất sẽ giữ nguyên tên gốc

KIỂM TRA PDF (Tab "Kiểm tra File")
----------------------------------
1. Nhấn "Chọn PDF" để chọn file PDF cần kiểm tra

2. Nhấn "🔍 Kiểm tra PDF"

3. Xem kết quả trong khung hiển thị:
   - Nếu có dữ liệu ẩn: hiển thị tên file, kích thước
   - Nếu không có: thông báo không phát hiện dữ liệu ẩn

KHUNG LOG OUTPUT
----------------
- Hiển thị ở phía dưới cửa sổ
- Ghi lại tất cả thao tác và kết quả
- Tự động cuộn xuống thông tin mới nhất

================================================================================
                           HƯỚNG DẪN SỬ DỤNG CLIproject:
   cd <đường_dẫn_đến_thư_mục>

1. ẨN FILE VÀO PDF:
   Cú pháp:
   python cli.py hide <pdf_gốc> <file_cần_ẩn> <pdf_output>

   Ví dụ:
   python cli.py hide samples\sample.pdf samples\secret.txt output\stego.pdf

2. TRÍCH XUẤT FILE TỪ PDF:
   Cú pháp:
   python cli.py extract <pdf_chứa_dữ_liệu_ẩn> <thư_mục_output>

   Ví dụ:
   python cli.py extract output\stego.pdf output\extracted\

3. KIỂM TRA PDF:
   Cú phápy extract <pdf_chứa_dữ_liệu_ẩn> <thư_mục_output>

   Ví dụ:
   python cli.py extract output\stego.pdf output\extracted\

3. KIỂM TRA PDF:
   python cli.py check <pdf_cần_kiểm_tra>

   Ví dụ:
   python cli.py check output\stego.pdf

4. XEM TRỢ GIÚP:
   python cli.py --help
   python cli.py hide --help
   python cli.py extract --help
   python cli.py check --help

VÍ DỤ THỰC TẾ
-------------

Ví dụ 1: Ẩn file text vào PDF
------------------------------
python cli.py hide document.pdf secret.txt document_with_secret.pdf

Kết quả: File secret.txt được ẩn trong document_with_secret.pdf

Ví dụ 2: Ẩn hình ảnh vào PDF
----------------------------
python cli.py hide report.pdf photo.jpg report_stego.pdf

Kết quả: File photo.jpg được ẩn trong report_stego.pdf

Ví dụ 3: Trích xuất file ẩn
---------------------------
python cli.py extract document_with_secret.pdf ./extracted/

Kết quả: File secret.txt được trích xuất vào thư mục ./extracted/

Ví dụ 4: Kiểm tra PDF có dữ liệu ẩn không
-----------------------------------------
python cli.py check document_with_secret.pdf

Kết quả: Hiển thị thông tin file ẩn (tên, kích thước)

================================================================================
                            KỸ THUẬT VÀ CẤU TRÚC
================================================================================

CẤU TRÚC FILE PDF
-----------------
File PDF có cấu trúc cơ bản:
1. Header (%PDF-x.x)
2. Body (Objects)
3. Cross-reference table
4. Trailer
5. %%EOF marker (đánh dấu kết thúc)

KỸ THUẬT ẨN DỮ LIỆU
-------------------

2. Tìm vị trí marker %%EOF cuối cùng

3. Thêm dữ liệu sau %%EOF theo cấu trúc:
   
   %%EOF
   <<HIDDEN_DATA_START>>
   [độ dài tên file (4 bytes)]
   [tên file gốc]
   [độ dài dữ liệu (4 bytes)]
   [dữ liệu file ẩn]
   <<HIDDEN_DATA_END>>

4. PDF viewer chỉ đọc đến %%EOF nên nội dung hiển thị không đổi

   <<HIDDEN_DATA_END>>

4. PDF viewer chỉ đọc đến %%EOF nên nội dung hiển thị không đổi
5. Công cụ có thể đọc và trích xuất dữ liệu sau %%EOF

ƯU ĐIỂM
-------
✓ Không làm thay đổi nội dung hiển thị của PDF
✓ PDF vẫn mở bình thường bằng các trình đọc PDF
✓ Dễ triển khai và sử dụng
✓ Hỗ trợ nhiều loại file
✓ Bảo toàn metadata của file ẩn (tên file, định dạng)

NHƯỢC ĐIỂM
----------
✗ Kích thước file PDF tăng lên theo kích thước file ẩn
✗ Có thể phát hiện bằng cách so sánh kích thước file
✗ Dữ liệu sau %%EOF có thể bị xóa bởi một số công cụ tối ưu PDF

================================================================================
                              XỬ LÝ LỖI
================================================================================

LỖI THƯỜNG GẶP VÀ CÁCH KHẮC PHỤC
--------------------------------

1. "File not found"
   Nguyên nhân: Đường dẫn file không đúng
   Giải pháp: Kiểm tra lại đường dẫn, sử dụng đường dẫn tuyệt đối

2. "Not a valid PDF file"
   Nguyên nhân: File không phải là PDF hoặc bị hỏng
   Giải pháp: Kiểm tra file có mở được bằng PDF reader không

3. "Unsupported file format"
   Nguyên nhân: Định dạng file không được hỗ trợ
   Giải pháp: Chỉ sử dụng các định dạng: .txt, .jpg, .png, .pdf, .docx, .exe

4. "No hiddp: Sử dụng bản backup của file PDF

6. "Module not found" (ImportError)
   Nguyên nhân: Thiếu thư viện Python
   Giải pháp: Chạy lại lệnh: python -m pip install -r requirements.txt

7. "pip is not recognized"
   Nguyên nhân: pip không có trong PATH
   Giải pháp: Sử dụng: python -m"
   Nguyên nhân: File PDF đã bị chỉnh sửa hoặc hỏng
   Giải pháat: Sử dụng bản backup của file PDF

6. Module not found (ImportError)

⚠️ LƯU Ý QUAN TRỌNG:

1. Không nên sử dụng để ẩn thông tin cực kỳ nhạy cảm vì:
   - Kỹ thuật này có thể bị phát hiện bằng công cụ chuyên dụng
   - Dữ liệu KHÔNG được mã hóa (lưu dạng plain text/binary)
   - Có thể phát hiện qua phân tích kích thước file

2. Nếu cần bảo mật cao hơn:
   - Mã hóa file trước khi ẩn (sử dụng AES, GPG, etc.)
   - Sử dụng kết hợp với các kỹ thuật steganography khác
   - Sử dụng password protection cho PDF
   - Nén file trước khi ẩn để giảm kích thước

3. Kiểm tra kích thước file:
   - File PDF sau khi ẩn dữ liệu sẽ lớn hơn
   - Có thể gây nghi ngờ nếu chênh lệch quá lớn
   - Nên chọn PDF có kích thước phù hợp với file cần ẩn
   - Mã hóa file trước khi ẩn
   - Sử dụng kết hợp với các kỹ thuật steganography khác
   - Sử dụng password protection cho PDF

================================================================================
                              LIÊN HỆ & HỖ TRỢ
================================================================================

Thông tin dự án:
- Tên: PDF Steganography Tool
- Ngôn ngữ: Python 3
- Môn học: An toàn và phục hồi dữ liệu
- Trường Đại học Khoa học Tự nhiên - ĐHQG.HCM

📄 FILE CHÍNH:

1. pdf_stego.py - Module core chứa class PDFSteganography
   • hide_file() - Ẩn file vào PDF
   • extract_file() - Trích xuất file từ PDF
   • check_hidden_data() - Kiểm tra dữ liệu ẩn
   • get_hidden_file_info() - Lấy thông tin file ẩn
   • validate_pdf() - Kiểm tra tính hợp lệ của PDF
   • validate_file_format() - Kiểm tra định dạng file hỗ trợ

2. cli.py - Command Line Interface
   • Sử dụng argparse để xử lý tham số dòng lệnh
   • 3 sub-commands: hide, extract, check
   • Hiển thị output có màu và format đẹp

3. gui.py - Graphical User Interface
   • Framework: Tkinter (built-in Python)
   • 3 tabs: Ẩn File, Trích xuất File, Kiểm tra File
   • File browsers với validation
   • Log output realtime
   • Status bar và error dialogs

📋 FILE TÀI LIỆU:
🧪 CÁCH 1: Chạy demo tự động (Khuyến nghị)

   python samples\demo.py

   Demo sẽ tự động:
   ✓ Ẩn file secret.txt vào sample.pdf
   ✓ Kiểm tra dữ liệu ẩn
   ✓ Trích xuất file
   ✓ Verify file integrity

🧪 CÁCH 2: Test thủ công

1. Tạo file test:
   echo "This is a secret message" > test.txt

2. Chuẩn bị một file PDF bất kỳ (hoặc dùng samples\sample.pdf)

3. Ẩn file test:
   python cli.py hide samples\sample.pdf test.txt output\test.pdf

4. Kiểm tra:
   python cli.py check output\test.pdf

5. Trích xuất:
   python cli.py extract output\test.pdf output\extracted\

6. So sánh file gốc và file trích xuất:
   • Windows: fc test.txt output\extracted\test.txt
   • Linux/Mac: diff test.txt output/extracted/test.txt

✅ Nếu output hiển thị "Files are identical" → Công cụ hoạt động đúng!

11. samples/sample.pdf - File PDF mẫu để test

12. samples/secret.txt - File text mẫu để ẩn

13. samples/demo.py - Script demo tự động
    • Test tất cả tính năng
    • Verify file integrity
    • Hiển thị kết quả chi tiết

14. samples/create_sample.py - Utility tạo PDF mẫu
    • Tạo PDF không cần thư viện ngoài
    • Chạy khi cần tạo lại sample.pdfg lệnh
   - 3 sub-commands: hide, extract, check

3. gui.py: Graphical User Interface
   - Sử dụng Tkinter
   - 3 tabs: Ẩn File, Trích xuất File, Kiểm tra File
   - Log output realtime

4. requirements.txt: Danh sách dependencies

5. README.txt: File hướng dẫn (file này)

6. report.tex: Báo cáo kỹ thuật bằng LaTeX

KIỂM TRA HOẠT ĐỘNG
------------------
Để kiểm tra công cụ hoạt động đúng:

1. Tạo file test:
   echo "This is a secret message" > test.txt

2. Chuẩn bị một file PDF bất kỳ (hoặc dùng sample.pdf)

3. Ẩn file test:
   python cli.py hide sample.pdf test.txt output.pdf

4. Kiểm tra:
   python cli.py check output.pdf

5. Trích xuất:
   python cli.py extract output.pdf ./extracted/

6. So sánh file gốc và file trích xuất:
   - Windows: fc test.txt extracted\test.txt
   - Linux/Mac: diff test.txt extracted/test.txt

GIỚI HẠN KỸ THUẬT
-----------------
- Kích thước file tối đa: Phụ thuộc vào RAM
- Định dạng PDF hỗ trợ: Tất cả PDF tuân thủ chuẩn (có marker %%EOF)
- Không hỗ trợ PDF được mã hóa hoặc password-protected
- Không hỗ trợ PDF bị hỏng hoặc không đúng định dạng

TƯƠNG LAI PHÁT TRIỂN
--------------------
Các tính năng có thể phát triển thêm:
- Mã hóa dữ liệu ẩn với password
- Nén dữ liệu trước khi ẩn
- Hỗ trợ ẩn nhiều file cùng lúc
- Steganography vào các object trong PDF
- Tích hợp checksum để phát hiện sửa đổi
- Web interface
