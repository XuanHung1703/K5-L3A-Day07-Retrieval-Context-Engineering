# Cấu hình agent chốt trên dev, trước khi chạy agent test

Model Gemini 3.5 Flash-Lite, TF-IDF, top-3, budget 3200 ký tự, tối đa 3 lượt search. Baseline cùng model và retriever, budget 800. Cả hai cùng code và benchmark fingerprint; config tại results/20261115-103232/tfidf-dev-3200/config.json và results/20261115-103548/tfidf-dev-800/config.json.

Lý do: dev agent 3200 có nhiều câu trả lời đúng có citation hơn, trong khi 800 bỏ phần lớn evidence và từ chối phần lớn câu có đáp án. 3200 vẫn có citation ghép sai và từ chối nhầm; chưa kết luận tối ưu tổng quát. Người học cần kiểm tra lại nhãn do AI đối chiếu.

Không sử dụng kết quả agent test để sửa hoặc chọn cấu hình. Test Lab 6 đã xuất hiện trong báo cáo cũ, là hạn chế về tính độc lập.
