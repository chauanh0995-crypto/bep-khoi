# Website Bếp Khói – Sườn Cay Khổng Lồ

Web tĩnh 5 trang, không cần máy chủ riêng:

| Trang | Nội dung |
|---|---|
| `index.html` | Trang chủ: đầu trang, Signature 4 size, Thử thách cấp cay, tóm tắt thực đơn, khoảnh khắc, không gian, đặt bàn, địa chỉ |
| `thuc-don.html` | Thực đơn đầy đủ và ảnh menu gốc |
| `khoanh-khac.html` | 12 ảnh khách check-in và thư viện ảnh |
| `khong-gian.html` | Clip và ảnh sân vườn có mái che |
| `dia-chi.html` | Địa chỉ, bản đồ, form đặt bàn |

Thanh menu và chân trang lặp lại ở cả 5 file; sửa ở một trang thì sửa cả 4 trang còn lại. Tải nguyên thư mục `bep-khoi/` lên bất kỳ hosting nào (cPanel, Netlify, Cloudflare Pages, GitHub Pages…).

## Điền thông tin quán

Chỉ sửa `config.js`: số điện thoại, Zalo, địa chỉ, giờ mở cửa, link Google Maps, mạng xã hội, giá món.
Thông tin hiện có lấy từ Facebook, TikTok và Google Maps của quán (20/11/2026). Số 0394 452 784 dùng cho cả gọi điện và Zalo.
Ô nào để trống thì web hiện "Đang cập nhật" và tự ẩn nút tương ứng. Có địa chỉ thì bản đồ tự hiện.

## Nút liên hệ

3 nút nổi bên phải (Gọi, Zalo, Messenger) lấy số và link từ `config.js` (`phone`, `zalo`, `social.messenger`).

## Đặt bàn

Khách điền form, bấm gửi: web chép sẵn nội dung đặt bàn và mở Zalo của quán để khách dán và gửi.
Không lưu dữ liệu ở đâu cả.

## Sửa món

Thực đơn đầy đủ nằm trong `thuc-don.html` (trang chủ chỉ có combo bò chảo và 3 dòng tóm tắt), chép từ menu PDF của quán (BẾP KHÓI-5.pdf, 20/11/2026).
Ảnh 2 trang menu gốc: `images/menu-bep-khoi-trang-1.jpg`, `-trang-2.jpg`. Đổi menu thì sửa chữ trong `thuc-don.html`, giá 4 size ở mục Signature của `index.html`, và thay 2 ảnh này.

## Ảnh, clip

- Ảnh món và khách: bộ ảnh Drive của quán (IMG_8990–9046, chụp tại quán), đã chuyển HEIC sang JPG, cạnh dài 1200–1600px.
- `suon-cay-khong-lo-bep-khoi.mp4`: clip đầu trang, lấy từ banner Sườn Cay Khổng Lồ trên dalatnow.vn.
- `suon-cay-size-*.webp`: ảnh 4 size tách nền, lấy từ menu PDF.
- `khong-gian-bep-khoi.mp4` (8,8 giây, không tiếng): ghép clip IMG_8978, 8974 (Drive "Tháng 11.2026/Lệ/Video") và IMG_4687, 4688, 4686, 4674 (Drive "Tháng 11.2026/Uyên"), cả hai thư mục đều quay tại Bếp Khói. Các clip khác ở đó trên 10MB, cần tải tay.
- `kk-nhom-ban-*`, `kk-khach-ngoi-*`, `kk-hoi-ban-*`, `kk-ban-duoi-*`, `khong-gian-mai-che-cay-xanh.jpg`: khung hình cắt từ các clip trên.
- `kk-*.jpg` (mục Khoảnh khắc): ảnh khách và quán đăng trên Google Maps của quán (20/11/2026). Ảnh khách đăng thuộc quyền của người chụp; nếu ai yêu cầu gỡ thì xóa ảnh đó khỏi `index.html` và `khoanh-khac.html`.
- Thay ảnh thì giữ nguyên tên file.

## Xem thử trên máy

```
npx http-server bep-khoi -p 5510
```
