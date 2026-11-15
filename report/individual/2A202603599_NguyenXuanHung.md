# Báo cáo Lab 7 — bản đang hoàn thiện

**Họ và tên:** Nguyễn Xuân Hùng

**Mã học viên:** `2A202603599`

**Lớp:** `L3A`

**Repo bài nộp:** https://github.com/XuanHung1703/K5-L3A-Day07-Retrieval-Context-Engineering

**Trạng thái:** Phần cơ bản đã có các lần chạy agent, retrieval, test và nhãn đối chiếu do AI thực hiện. Người học cần kiểm tra độc lập nhãn, quyền dữ liệu và giới hạn test kế thừa trước khi nộp. Bài đã được đưa lên repo cá nhân; cần kiểm tra lại nhãn trước khi nộp.

## Dữ liệu

Dùng 171 chunk B theo đoạn từ Lab 6, 59 trang từ hai giáo trình OpenStax/LibreTexts. Vector store PostgreSQL + pgvector, bảng chunks_b. Dense dùng google/embeddinggemma-2, 768 chiều, Document/SearchQuery prompt tương thích Lab 6. Adapter kiểm tra ID và nội dung database khớp corpus lexical trước khi chạy. Thông tin nguồn trong submission/data/source_manifest.json.

Benchmark: 15 câu có đáp án + 2 câu thiếu evidence ở dev; 5 + 2 ở test. q21–q24 mới có absence_reason. Bằng chứng không được truyền vào retriever hoặc model; gold chỉ dùng để chấm sau khi có kết quả.

Các câu test có đáp án được kế thừa từ Lab 6 và đã xuất hiện trong báo cáo Lab 6; đây là giới hạn tính độc lập. Không chỉnh Lab 7 dựa trên kết quả test trong phiên này. Nếu tiếp tục dùng test để chỉnh, phải tạo test mới.

## Kết quả retrieval đã chạy thật

| Cấu hình | Hit@1 | Evidence Hit@3 | Context Evidence Rate | Lỗi |
|---|---|---|---|---|
| tfidf-dev-3200 | 15/15 | 15/15 | 15/15 | 0 |
| tfidf-dev-800 | 15/15 | 15/15 | 0/15 | 0 |
| dense-dev-3200 | 14/15 | 15/15 | 15/15 | 0 |
| tfidf-dev-4800 | 15/15 | 15/15 | 15/15 | 0 |
| tfidf-test-800 | 4/5 | 5/5 | 1/5 | 0 |
| tfidf-test-3200 | 4/5 | 5/5 | 5/5 | 0 |
| hybrid-dev-3200 | 15/15 | 15/15 | 15/15 | 0 |

Kết quả mẫu số retrieval chỉ gồm câu có đáp án; hai câu thiếu evidence được tìm kiếm và lưu trace; abstention agent được báo riêng ở bảng agent bên dưới. Kết quả đời đầu 15 câu cũng được giữ trong results để tái lập lịch sử; bảng trên lấy lần có đủ 17 dev/7 test.

## Hai lỗi dev và thử nghiệm cải thiện

1. q01: tìm được đoạn đúng ở top-1 nhưng pack nguyên chunk và header nguồn không vừa budget 800; evidence không vào context. Tăng budget lên 3200 khôi phục evidence; trace lưu nội dung và context_ids.
2. q03: cũng tìm đúng top-1 nhưng budget 800 loại bỏ chunk chứa bằng chứng về Eleanor Roosevelt; với 3200, evidence còn trong context. Đây là hai câu lỗi cùng nguyên nhân context, không phải hai nguyên nhân khác nhau.

Hai cấu hình thử cải thiện: giữ nguyên TF-IDF/top-3, đổi budget 800 thành 3200 và 4800. Cả hai đạt 15/15 Context Evidence Rate dev; 4800 không tăng điểm trên bộ nhỏ này. Giới hạn: đánh giá bằng evidence nguyên văn không chứng minh câu trả lời của model đúng.

Lựa chọn retrieval trước test trong lượt thực hiện: TF-IDF budget 3200, vì đạt Hit@1 và giữ evidence tốt trên dev, không cần inference embedding, budget nhỏ hơn 4800. Baseline: TF-IDF budget 800. File ghi lựa chọn riêng chưa được tạo do lỗi đường dẫn ở lần đầu; quyết định và lệnh test đã có trong lịch sử thao tác. Không giả tạo timestamp khóa cấu hình. Config/fingerprint dev được kiểm tra bởi CLI trước test. Cấu hình agent sau đó được chọn trên dev và lưu tại submission/AGENT_SELECTION.md.

## Agent và giao diện

Code có Gemini 3.8 Flash function calling, tối đa 3 lần search, context budget tổng, kiểm tra citation ID, xử lý thiếu bằng chứng và lưu usage. Người dùng xác nhận Free Tier chưa liên kết thanh toán. Ba lần thử một câu dev: lần 1 lỗi 503 UNAVAILABLE; lần 2 và 3 lỗi 504 DEADLINE_EXCEEDED sau khoảng 120 giây. Trace lỗi nằm trong submission/results/*/gemini-probe*. Sau đó người dùng cho phép model Flash miễn phí khác; đã chạy Gemini 3.5 Flash-Lite thành công như mục bổ sung bên dưới. Không suy ra chi phí chính thức từ API usage. Có thể chạy web bằng `python -m streamlit run solution/ui.py`.

21/21 unit test đạt với `python -X utf8 -m unittest discover -s tests -v`. Chế độ Python mặc định Windows làm test gốc đọc UTF-8 lỗi; dùng -X utf8, không bỏ hay làm yếu test. Streamlit AppTest khởi tạo không lỗi, thao tác tìm kiếm TF-IDF trả 3 thẻ kết quả; chưa kiểm tra trực quan bằng trình duyệt.

## Các bước còn thiếu

- Người dùng đã cho phép dùng Gemini 3.5 Flash-Lite Free Tier sau các lỗi 503/504 của 3.8; ghi rõ model thực tế bên dưới.
- Đã chạy agent dev, chốt và chạy baseline/cấu hình chọn trên test; xem phần bổ sung bên dưới.
- Đã đối chiếu context, câu trả lời, từng citation và abstention trong reviews.json; người học cần kiểm tra độc lập.
- Đã tổng hợp thời gian, usage và agent metrics bên dưới; số tiền thực tế cần đối chiếu AI Studio.
- Người học kiểm tra câu thiếu evidence và quyền chia sẻ dữ liệu nguồn.

## Hướng dẫn tái lập

Xem HUONG_DAN_CHAY_LAB7.md và solution/versions-tested.json. Output mới không ghi đè lần trước. .env không được theo dõi trong Git. Repo bài nộp được ghi ở đầu báo cáo.

Lưu ý tái lập: code agent đã sửa sau các lần retrieval benchmark để tương thích SDK và kiểm soát retry. Fingerprint cũ không hợp lệ cho test mới; cần chạy dev lại sau mọi thay đổi code rồi mới chạy test với config tương ứng. Không xem retrieval test đã chạy là đánh giá độc lập của phiên bản agent mới.

## Đánh giá thủ công context retrieval test

Đã đọc 5 câu có đáp án của baseline 800 và cấu hình 3200; nhãn và lý do lưu tại submission/retrieval_test_context_review.json. Baseline: mức 0/1/2 lần lượt 3/1/1. Cấu hình 3200: 0/0/5. Đây là đánh giá context retrieval theo trace, chưa phải đánh giá context do agent tạo hoặc điểm trả lời/citation.

## Agent Gemini 3.5 Flash-Lite: kết quả chạy thật

Google công bố model `gemini-3.5-flash-lite` có Free Tier và hỗ trợ function calling. Người dùng xác nhận dự án Free Tier chưa liên kết thanh toán và cho phép đổi model sau lỗi 3.8. Chi phí dịch vụ theo xác nhận Free Tier là dự kiến 0 USD; số tiền thực tế chưa được xác nhận từ trang billing. Usage bao gồm prompt/candidate tokens trong trace, không thay thế hóa đơn. https://ai.google.dev/gemini-api/docs/pricing

| Cấu hình | Split | Tool use | Điểm trả lời 0/1/2, TB /2 | Citation hỗ trợ | Câu có citation | Abstention đúng | Từ chối nhầm | Thời gian tổng / TB giây |
|---|---|---|---|---|---|---|---|---|
| TF-IDF 800 | dev | 17/17 | 15/0/0; 0,00 | 0/0 N/A | 0/1 | 2/2 | 14/15 | 312,7 / 18,4 |
| TF-IDF 3200 | dev | 16/17 | 1/3/11; 1,67 | 30/38 | 14/14 | 2/2 | 1/15 | 176,9 / 10,4 |
| Dense 3200 | dev bổ sung | 17/17 | 0/2/13; 1,87 | 30/35 | 15/15 | 2/2 | 0/15 | 193,2 / 11,4 |
| Hybrid 3200 | dev bổ sung | 16/17 | 1/3/11; 1,67 | 28/37 | 14/14 | 2/2 | 1/15 | 216,8 / 12,8 |
| TF-IDF 800 | test | 7/7 | 3/1/1; 0,60 | 2/4 | 2/2 | 2/2 | 3/5 | 107,5 / 15,4 |
| TF-IDF 3200 | test | 7/7 | 0/1/4; 1,80 | 8/10 | 4/5 | 2/2 | 0/5 | 67,2 / 9,6 |

Nhãn do AI đối chiếu evidence, chưa được người học kiểm tra độc lập. Điểm trả lời đánh giá nội dung và sự hiện diện evidence; citation hợp lệ được chấm riêng. Ví dụ test q20 context có bằng chứng và nội dung đúng nhưng model không đưa citation; q19 thêm ví dụ retrovirus ngoài bằng chứng. Nhãn từng câu trong reviews.json bên cạnh traces.json; agent_metrics.json là kết quả tổng hợp. Context test baseline mức 0/1/2 là 3/1/1, 3200 là 0/0/5.

Bộ test 5 câu có đáp án kế thừa Lab 6 đã có kết quả công bố, vì vậy không khẳng định tính độc lập mạnh. Cấu hình agent TF-IDF 3200 được ghi trong submission/AGENT_SELECTION.md trước khi chạy test. Dense và hybrid dev được chạy bổ sung sau test, không dùng kết quả của chúng để chọn lại cấu hình test. Vì dense dev có kết quả cao hơn, đây là giới hạn lựa chọn; muốn chọn lại phải tạo test độc lập mới, không dùng lại test đã xem.

Ví dụ lỗi dev: q01 TF-IDF 3200 từ chối dù câu có đáp án sau các lượt search; q02 trả lời đúng ý chính nhưng thêm thông tin và citation gộp nhiều ID. Các câu q13 trích tài liệu có sự khác biệt vị trí 6/7; model thêm diễn giải chưa được chứng minh. Kiểm tra ID citation không thay thế việc đối chiếu nội dung.

Usage tokens (prompt / candidate): TF-IDF dev 800: 14.395 / 1.369; TF-IDF dev 3200: 14.540 / 2.199; dense dev: 14.596 / 2.109; hybrid dev: 15.324 / 2.318; test 800: 5.135 / 582; test 3200: 6.014 / 752. Token thinking tách riêng được SDK báo 0 trong các trace. Thời gian đo từng câu bao gồm inference, truy xuất và chờ giới hạn tốc độ, không bao gồm tải model ban đầu.
