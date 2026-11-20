(function () {
  var c = window.BEP_KHOI || {};
  var phone = (c.phone || "").replace(/\s+/g, "");
  var zalo = (c.zalo || c.phone || "").replace(/\s+/g, "");
  var zaloUrl = zalo ? "https://zalo.me/" + zalo : "";

  function all(sel) { return Array.prototype.slice.call(document.querySelectorAll(sel)); }
  function setText(sel, val) { if (val) all(sel).forEach(function (el) { el.textContent = val; }); }
  function setLink(sel, href) {
    all(sel).forEach(function (el) {
      if (href) el.href = href; else el.hidden = true;
    });
  }

  setText("[data-phone]", c.phone);
  setText("[data-address]", c.address);
  setText("[data-hours]", c.hours);
  setLink("[data-phone-link]", phone ? "tel:" + phone : "");
  setLink("[data-zalo-link]", zaloUrl);

  setText("[data-parking]", c.parking);
  setText("[data-email]", c.email);
  var social = c.social || {};
  ["facebook", "tiktok", "youtube", "messenger"].forEach(function (k) { setLink("[data-social-" + k + "]", social[k]); });

  var maps = c.mapsUrl || (c.address ? "https://www.google.com/maps/search/?api=1&query=" + encodeURIComponent("Bếp Khói " + c.address) : "");
  setLink("[data-maps-link]", maps);
  var q = c.mapQuery || (c.address ? "Bếp Khói " + c.address : "");
  var box = document.querySelector("[data-map-box]");
  if (q && box) {
    box.innerHTML = '<iframe title="Bản đồ Bếp Khói" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=' +
      encodeURIComponent(q) + '&z=17&output=embed"></iframe>';
  }

  document.getElementById("year").textContent = new Date().getFullYear();

  // Thanh menu: nền đặc khi cuộn khỏi đầu trang
  var nav = document.querySelector(".nav");
  var onScroll = function () { nav.classList.toggle("scrolled", window.scrollY > 40); };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // Nút menu trên điện thoại
  var toggle = document.querySelector(".nav-toggle");
  if (toggle) {
    var setOpen = function (open) {
      nav.classList.toggle("open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Đóng menu" : "Mở menu");
    };
    toggle.addEventListener("click", function () { setOpen(!nav.classList.contains("open")); });
    all(".nav-links a").forEach(function (a) { a.addEventListener("click", function () { setOpen(false); }); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") setOpen(false); });
  }

  // Hiện dần khi cuộn tới
  var reveals = all(".reveal");
  if ("IntersectionObserver" in window) {
    document.documentElement.classList.add("js");
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  }

  // Form đặt bàn (chỉ có ở trang chủ và trang Địa chỉ)
  var form = document.getElementById("bookForm");
  if (form) initForm(form);

  function initForm(form) {
  var d = new Date(), pad = function (n) { return (n < 10 ? "0" : "") + n; };
  form.ngay.value = d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
  form.ngay.min = form.ngay.value;

  var msg = document.getElementById("formMsg");
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!form.checkValidity()) { msg.textContent = "Bạn điền giúp tên, số người, ngày và giờ nhé."; form.reportValidity(); return; }
    var p = form.ngay.value.split("-");
    var text = "Đặt bàn Bếp Khói\n" +
      "Tên: " + form.ten.value.trim() + "\n" +
      "Số người: " + form.so_nguoi.value + "\n" +
      "Thời gian: " + form.gio.value + " ngày " + p[2] + "/" + p[1] + "/" + p[0] + "\n" +
      (form.size.value !== "Chưa chọn" ? "Đặt trước: sườn cay " + form.size.value + "\n" : "") +
      (form.ghi_chu.value.trim() ? "Ghi chú: " + form.ghi_chu.value.trim() : "");
    var done = function (copied) {
      var lead = copied ? "Đã chép nội dung đặt bàn. " : "Nội dung đặt bàn:\n" + text + "\n\n";
      if (zaloUrl) {
        msg.textContent = lead + "Dán vào Zalo rồi gửi cho quán nhé.";
        window.open(zaloUrl, "_blank", "noopener");
      } else {
        msg.textContent = lead + "Quán đang cập nhật số Zalo, bạn gọi điện giúp nhé.";
      }
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(false); });
    } else { done(false); }
  });
  }
})();
