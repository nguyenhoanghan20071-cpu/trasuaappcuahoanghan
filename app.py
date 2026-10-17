import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# CẤU HÌNH TRANG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Hệ Thống Tính Tiền Trà Sữa",
    page_icon="🧋",
    layout="wide"
)

# Hiển thị hình ảnh
st.image("TRASUA.jpg", use_container_width=True)

# ---------------------------------------------------------
# THÔNG TIN NGƯỜI TẠO
# ---------------------------------------------------------
AUTHOR = "Nguyễn Hoàng Hân"

# ---------------------------------------------------------
# DANH SÁCH SẢN PHẨM VÀ GIÁ
# ---------------------------------------------------------
MENU_TEA = {
    "Trà Sữa Truyền Thống": 30000,
    "Trà Sữa Trân Châu Đường Đen": 35000,
    "Trà Sữa Thái Xanh": 32000,
    "Trà Sữa Ô Long": 35000,
    "Trà Sữa Matcha": 38000,
    "Trà Sữa Dâu Tây": 35000,
    "Trà Đào Cam Sả": 35000,
    "Trà Dâu Tằm": 32000,
}

SIZE_OPTIONS = {
    "S (Vừa)": 0,
    "M (Lớn)": 5000,
    "L (Đặc biệt)": 10000
}

TOPPING_OPTIONS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 7000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 8000,
    "Kem Cheese": 10000
}

SUGAR_LEVELS = [
    "100% (Bình thường)", "70%", "50%", "30%", "0% (Không đường)"
]

ICE_LEVELS = [
    "100% (Bình thường)", "70%", "50%", "30%", "0% (Không đá)"
]

# ---------------------------------------------------------
# KHỞI TẠO GIỎ HÀNG
# ---------------------------------------------------------
if "cart" not in st.session_state:
    st.session_state.cart = []

if "invoice_paid" not in st.session_state:
    st.session_state.invoice_paid = False

if "discount" not in st.session_state:
    st.session_state.discount = 0

# ---------------------------------------------------------
# HÀM TẠO HÓA ĐƠN TXT
# ---------------------------------------------------------
def create_txt_invoice(
    customer_name, cart, total_amount, discount, final_amount
):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    content = "=" * 45 + "\n"
    content += "HÓA ĐƠN BÁN HÀNG - BOBA TEA".center(45) + "\n"
    content += "=" * 45 + "\n"
    content += f"Ngày: {now}\n"
    content += f"Khách hàng: {customer_name or 'Khách vãng lai'}\n"
    content += f"Người tạo chương trình: {AUTHOR}\n"
    content += "-" * 45 + "\n"

    for idx, item in enumerate(cart, 1):
        content += f"{idx}. {item['Tên món']} (Size {item['Size']})\n"
        content += f"   Đường: {item['Đường']} | Đá: {item['Đá']}\n"

        if item["Topping"] != "Không":
            content += f"   Topping: {item['Topping']}\n"

        content += (
            f"   Số lượng: {item['Số lượng']} x "
            f"{item['Đơn giá']:,} = {item['Thành tiền']:,} VNĐ\n"
        )

    content += "-" * 45 + "\n"
    content += f"Tổng tiền món: {total_amount:,} VNĐ\n"
    content += f"Giảm giá: {discount}%\n"
    content += f"TỔNG THANH TOÁN: {final_amount:,} VNĐ\n"
    content += "=" * 45 + "\n"
    content += "Cảm ơn quý khách và hẹn gặp lại!".center(45) + "\n"

    return content

# ---------------------------------------------------------
# GIAO DIỆN CHÍNH
# ---------------------------------------------------------
st.title("🧋 QUÁN TRÀ SỮA MR BÌNH")
st.caption(f"Người thực hiện: {AUTHOR}")
st.markdown("---")

col_left, col_right = st.columns([1.1, 0.9])

# =========================================================
# CỘT TRÁI: THÔNG TIN ĐƠN HÀNG
# =========================================================
with col_left:
    st.subheader("📝 Thông tin đơn hàng")

    customer_name = st.text_input(
        "Tên khách hàng:",
        placeholder="Nhập tên khách hàng..."
    )

    st.markdown("#### Chọn món nước và tùy chọn")

    col_item, col_qty = st.columns([3, 1])

    with col_item:
        selected_tea = st.selectbox(
            "Loại trà sữa:",
            list(MENU_TEA.keys())
        )

    with col_qty:
        quantity = st.number_input(
            "Số lượng:",
            min_value=1,
            value=1,
            step=1
        )

    c_size, c_sugar, c_ice = st.columns(3)

    with c_size:
        selected_size = st.selectbox(
            "Size:",
            list(SIZE_OPTIONS.keys())
        )

    with c_sugar:
        selected_sugar = st.selectbox(
            "Mức đường:",
            SUGAR_LEVELS
        )

    with c_ice:
        selected_ice = st.selectbox(
            "Mức đá:",
            ICE_LEVELS
        )

    selected_toppings = st.multiselect(
        "Loại topping (có thể chọn nhiều):",
        options=list(TOPPING_OPTIONS.keys())
    )

    # Tính đơn giá
    base_price = MENU_TEA[selected_tea]
    size_price = SIZE_OPTIONS[selected_size]
    topping_price = sum(
        TOPPING_OPTIONS[t] for t in selected_toppings
    )

    unit_price = base_price + size_price + topping_price
    item_total = unit_price * quantity

    st.info(
        f"💡 Đơn giá một ly: **{unit_price:,} VNĐ**"
    )
    st.write(f"**Thành tiền món đang chọn:** {item_total:,} VNĐ")

    if st.button(
        "➕ Thêm vào hóa đơn",
        type="primary",
        use_container_width=True
    ):
        item_data = {
            "Tên món": selected_tea,
            "Size": selected_size.split()[0],
            "Đường": selected_sugar.split()[0],
            "Đá": selected_ice.split()[0],
            "Topping": ", ".join(selected_toppings)
            if selected_toppings else "Không",
            "Đơn giá": unit_price,
            "Số lượng": quantity,
            "Thành tiền": item_total
        }

        st.session_state.cart.append(item_data)
        st.session_state.invoice_paid = False

        st.toast(
            f"Đã thêm {quantity} x {selected_tea} vào giỏ!",
            icon="✅"
        )
        st.rerun()

# =========================================================
# CỘT PHẢI: GIỎ HÀNG VÀ THANH TOÁN
# =========================================================
with col_right:
    st.subheader("🛒 Danh sách món đã gọi")

    if not st.session_state.cart:
        st.warning(
            "Giỏ hàng đang trống. "
            "Vui lòng chọn món ở cột bên trái."
        )

    else:
        df_cart = pd.DataFrame(st.session_state.cart)

        st.dataframe(
            df_cart[
                [
                    "Tên món", "Size", "Topping",
                    "Số lượng", "Đơn giá", "Thành tiền"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        if st.button("🗑️ Xóa tất cả món"):
            st.session_state.cart = []
            st.session_state.invoice_paid = False
            st.rerun()

        st.markdown("---")

        total_price = int(df_cart["Thành tiền"].sum())

        discount = st.number_input(
            "Giảm giá (%):",
            min_value=0,
            max_value=100,
            value=st.session_state.discount,
            step=5,
            key="discount"
        )

        final_price = int(total_price * (1 - discount / 100))

        st.markdown(f"### Tổng tiền: {total_price:,} VNĐ")

        if discount > 0:
            st.markdown(
                f"### Sau giảm giá: {final_price:,} VNĐ"
            )

        if st.button(
            "💳 XÁC NHẬN THANH TOÁN",
            type="primary",
            use_container_width=True
        ):
            st.session_state.invoice_paid = True
            st.balloons()
            st.rerun()

# =========================================================
# HÓA ĐƠN SAU KHI THANH TOÁN
# =========================================================
if st.session_state.invoice_paid and st.session_state.cart:
    st.markdown("---")
    st.success("🎉 Thanh toán thành công!")

    total_price = sum(
        item["Thành tiền"] for item in st.session_state.cart
    )
    discount = st.session_state.discount
    final_price = int(total_price * (1 - discount / 100))

    with st.container(border=True):
        st.markdown(
            "<h2 style='text-align:center; color:#FF4B4B;'>"
            "🧋 HÓA ĐƠN BÁN HÀNG - BOBA TEA</h2>",
            unsafe_allow_html=True
        )

        st.write(
            f"**Thời gian:** "
            f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        )
        st.write(
            f"**Khách hàng:** "
            f"{customer_name or 'Khách vãng lai'}"
        )
        st.write(f"**Người thực hiện:** {AUTHOR}")

        st.table(
            pd.DataFrame(st.session_state.cart)[
                [
                    "Tên món", "Size", "Đường", "Đá",
                    "Topping", "Số lượng", "Thành tiền"
                ]
            ]
        )

        st.write(f"**Tổng tiền món:** {total_price:,} VNĐ")
        st.write(f"**Giảm giá:** {discount}%")

        st.markdown(
            f"### TỔNG THANH TOÁN: {final_price:,} VNĐ"
        )

    # Tạo file hóa đơn
    txt_data = create_txt_invoice(
        customer_name,
        st.session_state.cart,
        total_price,
        discount,
        final_price
    )

    st.download_button(
        label="📥 Tải hóa đơn (.TXT)",
        data=txt_data,
        file_name=(
            f"HoaDon_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        ),
        mime="text/plain",
        use_container_width=True
    )

    if st.button(
        "🔄 Tạo đơn hàng mới",
        use_container_width=True
    ):
        st.session_state.cart = []
        st.session_state.invoice_paid = False
        st.session_state.discount = 0
        st.rerun()

# ---------------------------------------------------------
# CHÂN TRANG
# ---------------------------------------------------------
st.markdown("---")
st.caption(f"© 2026 | Chương trình thực hiện bởi {AUTHOR}")
