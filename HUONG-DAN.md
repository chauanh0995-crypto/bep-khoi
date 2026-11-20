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

## Đưa lên mạng

- Kho GitHub: https://github.com/chauanh0995-crypto/bep-khoi (nhánh `main`), GitHub Pages phục vụ thẳng từ nhánh này.
- Tên miền: suoncaykhonglo.vn (file `CNAME`). DNS tại iNET: 4 bản ghi A cho `@` trỏ 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153 và CNAME `www` trỏ `chauanh0995-crypto.github.io`.
- Cập nhật web: sửa file, rồi `git add -A`, `git commit`, `git push`. Khoảng 1 phút sau web tự cập nhật.

## Blog

- Trang danh sách: `blog/index.html`. Mỗi bài là một thư mục `blog/<duong-dan>/index.html` (đường dẫn trên web: `/blog/<duong-dan>/`).
- Thêm bài mới: sao chép một thư mục bài có sẵn, đổi tên thư mục, sửa tiêu đề, mô tả, nội dung, ảnh bìa và khối `BlogPosting` trong `<head>`. Sau đó thêm thẻ bài vào `blog/index.html`, thêm địa chỉ bài vào `sitemap.xml` và `llms.txt`.
- Chỉ viết thông tin đã xác nhận (giá theo menu, giờ, địa chỉ). Không bịa số liệu, đánh giá hay khuyến mãi.

## SEO và GEO đã làm (20/11/2026)

- Mỗi trang có tiêu đề, mô tả, `canonical`, ảnh chia sẻ 1200×630 (`images/og-*.jpg`).
- Dữ liệu có cấu trúc: `Restaurant` + `WebSite` + `FAQPage` (trang chủ), `Menu` có giá 47 món (thực đơn), `Restaurant` (địa chỉ), `BreadcrumbList` (trang con), `Blog`/`BlogPosting` (blog).
- `sitemap.xml`, `robots.txt`, `llms.txt` (tóm tắt cho AI), `404.html`.
- Mục Hỏi đáp trên trang chủ trả lời giá, cấp cay, giờ, đậu xe, đặt bàn.
- Đổi giá hay giờ thì sửa cả: trang, khối JSON-LD trong `<head>`, mục Hỏi đáp và `llms.txt`.

## Đăng blog tự động (30 bài, 21/11 – 20/12/2026)

- Hàng chờ: `_lich-dang/` (chỉ nằm trên máy này, không đẩy lên GitHub). Mỗi tệp là một bài, tên dạng `2026-12-05-ten-bai.html`, phần đầu tệp ghi ngày đăng, tiêu đề, mô tả, ảnh.
- Tác vụ Windows **BepKhoi-DangBai** chạy 08:00 và 13:00 mỗi ngày, và 3 phút sau khi đăng nhập Windows (máy bật muộn vẫn chạy bù). Nó gọi `tools/dang-bai.vbs` → `tools/dang-bai.sh` → `tools/dang_bai.py`.
- Mỗi lần chạy: bài nào tới ngày thì tạo trang `/blog/<ten-bai>/`, cập nhật trang Blog, `sitemap.xml`, `llms.txt`, `blog/bai-viet.json`, rồi commit + push và báo Bing qua IndexNow.
- Nhật ký: `tools/dang-bai.log`.
- Sửa bài trước ngày đăng: mở tệp trong `_lich-dang/` và sửa. Đổi ngày: sửa dòng `date:`.
- Sửa bài đã đăng: sửa thẳng `blog/<ten-bai>/index.html` rồi push.
- Chạy tay: mở Git Bash, gõ `bash /c/SEODALATNOW/bep-khoi/tools/dang-bai.sh`. Chạy thử không đẩy: `python -X utf8 tools/dang_bai.py --khong-push --ngay 2026-12-01` (chỉ chạy trên bản sao, vì lệnh này vẫn ghi tệp).
- Máy tính phải bật thì bài mới lên.
