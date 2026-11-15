# Hướng dẫn chạy phần triển khai Lab 7

Trạng thái: đã có code và benchmark thật với Gemini 3.5 Flash-Lite; kết quả và nhãn do AI đối chiếu cần người học kiểm tra trước khi nộp. Test kế thừa Lab 6 có giới hạn tính độc lập.

## Cấu hình

Python 3.11+. Từ thư mục gốc Lab 7, dùng môi trường Python đã chạy Lab 6. Dependencies trong solution/requirements.txt. Model embedding và vector store dùng lại Lab 6; adapter chỉ đọc bảng chunks_b và kiểm tra ID/nội dung khớp dữ liệu lexical. Không sửa database.

Tạo `.env` tại thư mục gốc bằng editor, không commit:

```dotenv
DAY6_ROOT=D:/Lab/Lab6/K5-L3-Day06-DataIngestionEngineering
GEMINI_MODEL=gemini-3.5-flash-lite
GEMINI_API_KEY=
GEMINI_FREE_TIER_CONFIRMED=yes
```

Nhập key mới trực tiếp vào máy. Chỉ đặt GEMINI_FREE_TIER_CONFIRMED=yes sau khi kiểm tra dự án chứa key là Free Tier và chưa liên kết thanh toán. Cờ này ghi nhận xác nhận của bạn, không thể kiểm soát billing phía Google. Nếu đổi key/dự án, kiểm tra lại trước khi chạy. Không dùng key đã lộ trong chat. DATABASE_URL có thể đặt riêng hoặc lấy từ .env của Lab 6. Không in secret.

## Các lệnh từ thư mục gốc Lab 7

```powershell
python -X utf8 -m unittest discover -s tests -v
python solution/lab7.py --method tfidf --split dev --budget 800
python solution/lab7.py --method dense --split dev --budget 800
python solution/lab7.py --method hybrid --split dev --budget 800
python solution/lab7.py --method hybrid --split dev --budget 3200
python solution/lab7.py --method hybrid --split dev --budget 4800
python -m streamlit run solution/ui.py
```

Hai cấu hình budget 3200 và 4800 là hai thí nghiệm đề xuất: giữ nguyên ranking, đo ảnh hưởng tăng context. Phải chạy và phân tích trước/sau trên dev, không giả định tăng điểm.

Thêm `--agent` để chạy agent Gemini thật. Agent tối đa 3 lượt search, model điều phối bằng function calling; có giới hạn tổng context evidence qua các lượt. Lưu usage tokens, không tự nhận định chi phí bằng 0. Adapter bảo toàn nội dung trả về của model (bao gồm thought signatures). ID citation đúng chỉ là kiểm tra cú pháp; phải chấm hỗ trợ ngữ nghĩa thủ công.

Mỗi lần chạy tạo thư mục mới trong submission/results. Không ghi đè lần trước. Test yêu cầu `--frozen` trỏ tới config.json của lần dev cùng cấu hình và dữ liệu/code. Ví dụ (thay đường dẫn bằng file thật):

```powershell
python solution/lab7.py --method hybrid --split test --budget 3200 --agent --frozen <dev-config.json>
```

Phải chạy baseline trên test nữa, dùng config dev của chính baseline. Đã chạy cả retrieval và agent test cho baseline TF-IDF 800 và cấu hình chọn 3200. Nếu test Lab 6 đã dùng để chỉnh Lab 7, thay test trước khi benchmark và ghi lịch sử sử dụng.

## Kết quả và đánh giá

- traces.json: ranking query gốc, context, tool calls, câu trả lời và lỗi.
- summary.json: Hit@1, Hit@3, Context Evidence Rate (n/N); lỗi báo riêng, kiểm tra answerable_total để tránh bỏ sót mẫu số.
- config.json: fingerprint code/dữ liệu để chặn test với cấu hình khác dev.
- reviews_template.json: nhãn còn trống; điền context_grade, answer_grade 0–2, citation_support tương ứng từng citation, abstention_correct và reason sau khi đọc.
- Agent metrics: dùng starter/agent_metrics.py theo starter/README.md với cases/traces/reviews đã chuẩn bị; không suy ra nhãn thủ công từ hit string.

## Những mục còn thiếu trước khi nộp

1. questions.json hiện có 24 câu: 15+2 dev, 5+2 test. q21–q24 được bổ sung với absence_reason. Cần người học đối chiếu phạm vi nguồn trước khi nộp. Các kết quả ban đầu dùng bộ 20 câu được giữ lại, không giả nhận là benchmark đủ 24 câu.
2. Đã chạy cả ba phương pháp trên dev và lưu số liệu Lab 7; xem báo cáo cá nhân.
3. Đã chạy dev, chốt cấu hình và chạy test bằng Gemini 3.5 Flash-Lite Free Tier; xem báo cáo.
4. Kiểm tra độc lập các nhãn ngữ nghĩa, citation, abstention và phân tích lỗi dev do AI đã đối chiếu.
5. Kiểm tra báo cáo cá nhân và quyền chia sẻ nguồn trước khi nộp.

## Nguồn / quyền

Corpus trong submission/data là bản chuyển từ OpenStax/LibreTexts của Lab 6. Giữ data/manifest.json và thông tin nguồn của Lab 6 khi chia sẻ. Hai tài liệu theo báo cáo Lab 6: World History II: From 1400, General Biology, CC BY 4.0. Không kèm PDF lớn hoặc secret. Cần đối chiếu bản gốc khi chấm.

API reference đã kiểm tra: https://ai.google.dev/gemini-api/docs/generate-content/function-calling?authuser=0&hl=en
Model: https://ai.google.dev/gemini-api/docs/latest-model

Không commit, push hoặc đổi remote tự động. Khi xem Source Control, kiểm tra submission/data và submission/results được theo dõi; starter/data và starter/results vẫn bị ignore theo đề gốc.

.env cũng được đọc từ thư mục cha D:/Lab/Lab7 nếu chưa có biến ở thư mục gốc repo. Không đưa .env lên Git. Người dùng chỉ cho phép quota miễn phí và đã xác nhận Free Tier chưa liên kết thanh toán. Chạy smoke test trước khi benchmark; nếu API lỗi quota/model, dừng và lưu lỗi, không đổi model hoặc bật thanh toán tự động.

## Chạy agent trên Free Tier

Trong PowerShell tại thư mục gốc Lab 7:

```powershell
$env:GEMINI_FREE_TIER_CONFIRMED="yes"
python -X utf8 solution/lab7.py --method tfidf --split dev --budget 3200 --agent
```

Không sử dụng config retrieval-only để chạy agent test: cần config từ dev có --agent cùng model/cấu hình và code fingerprint. Các bản code sửa sau lần benchmark cũ sẽ đòi chạy lại dev trước khi test.

Mở giao diện bằng CHAY_WEB.bat. Nút agent yêu cầu checkbox đồng ý gửi query/evidence; script không tự thay đổi billing phía Google.

## Trạng thái API ngày 15/11/2026

Ba lần thử Gemini 3.8 Flash cho q01 trên Free Tier: 503, 504, 504; chưa có phản hồi agent thành công. Lỗi được lưu trong submission/results/*/gemini-probe*. Sau đó đã chạy benchmark bằng Gemini 3.5 Flash-Lite theo cho phép của người dùng; không chuyển sang gói tính phí.

## Kết quả sau khi người dùng cho phép model thay thế

Đã chạy Gemini 3.5 Flash-Lite Free Tier trên dev, khóa cấu hình TF-IDF 3200, chạy baseline và cấu hình chọn trên test. Dense/hybrid agent dev chạy bổ sung sau test và không được dùng để chọn lại test. Chi tiết, hạn chế và nhãn do AI đối chiếu nằm trong báo cáo cá nhân và `reviews.json`. Người học cần tự kiểm tra lại.

Nhấp đúp `CHAY_WEB.bat` để mở web với model 3.5 Flash-Lite. Lệnh benchmark cần đặt `$env:GEMINI_MODEL="gemini-3.5-flash-lite"` và `$env:GEMINI_FREE_TIER_CONFIRMED="yes"` trong PowerShell. Nếu dùng model khác phải chạy lại dev và khóa cấu hình trước test.
