// غيّر رقم واتساب هنا (مثال الجزائر: 213xxxxxxxxx)
const WHATSAPP_NUMBER = "213556440987";

const yearEl = document.getElementById("year");
yearEl.textContent = new Date().getFullYear();

const orderListEl = document.getElementById("orderList");
const orderTotalEl = document.getElementById("orderTotal");
const clearOrderBtn = document.getElementById("clearOrder");

const sendOrderWhats = document.getElementById("sendOrderWhats");
const whatsFloat = document.getElementById("whatsFloat");
const whatsBtnTop = document.getElementById("whatsBtnTop");

let order = []; // {item, price}

function formatMessage(text){
  return encodeURIComponent(text);
}

function calcTotal(){
  return order.reduce((sum, x) => sum + Number(x.price || 0), 0);
}

function renderOrder(){
  orderListEl.innerHTML = "";
  order.forEach((x, idx) => {
    const li = document.createElement("li");
    li.innerHTML = `
      ${x.item} — <strong>${x.price} دج</strong>
      <button data-idx="${idx}" class="removeBtn" style="margin-right:10px; background:transparent; border:1px solid rgba(255,255,255,.2); color:#fff; border-radius:10px; padding:4px 8px; cursor:pointer;">
        حذف
      </button>
    `;
    orderListEl.appendChild(li);
  });

  orderTotalEl.textContent = calcTotal();

  document.querySelectorAll(".removeBtn").forEach(btn => {
    btn.addEventListener("click", (e) => {
      const i = Number(e.target.getAttribute("data-idx"));
      order.splice(i, 1);
      renderOrder();
    });
  });
}

document.querySelectorAll(".addToOrder").forEach(btn => {
  btn.addEventListener("click", () => {
    order.push({
      item: btn.dataset.item,
      price: btn.dataset.price
    });
    renderOrder();
  });
});

clearOrderBtn.addEventListener("click", () => {
  order = [];
  renderOrder();
});

function openWhatsApp(message){
  const url = `https://wa.me/${WHATSAPP_NUMBER}?text=${formatMessage(message)}`;
  window.open(url, "_blank");
}

sendOrderWhats.addEventListener("click", (e) => {
  e.preventDefault();

  if(order.length === 0){
    alert("سلة الطلب فارغة. أضف أطباقًا أولاً.");
    return;
  }

  const lines = order.map((x, i) => `${i+1}) ${x.item} - ${x.price} دج`).join("\n");
  const total = calcTotal();

  const msg =
`طلب جديد من الموقع:
${lines}

المجموع: ${total} دج
الاسم: (اكتب اسمك هنا في الرسالة)
العنوان: (اكتب عنوان التوصيل هنا)`;

  openWhatsApp(msg);
});

// زر واتساب عام
function bindGeneralWhats(btn){
  btn.addEventListener("click", (e) => {
    e.preventDefault();
    openWhatsApp("مرحبًا، أريد الاستفسار/الطلب من مطعم النكهة.");
  });
}
bindGeneralWhats(whatsFloat);
bindGeneralWhats(whatsBtnTop);

// نموذج الحجز
const reserveForm = document.getElementById("reserveForm");
reserveForm.addEventListener("submit", (e) => {
  e.preventDefault();

  const name = document.getElementById("name").value.trim();
  const phone = document.getElementById("phone").value.trim();
  const date = document.getElementById("date").value;
  const time = document.getElementById("time").value;
  const people = document.getElementById("people").value;
  const notes = document.getElementById("notes").value.trim();

  const msg =
`حجز طاولة:
الاسم: ${name}
الهاتف: ${phone}
التاريخ: ${date}
الوقت: ${time}
عدد الأشخاص: ${people}
ملاحظات: ${notes || "—"}`;

  openWhatsApp(msg);
});