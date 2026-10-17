import streamlit as datetime_mod  # để tránh trùng tên biến
from datetime import datetime
import streamlit as st

# Cấu hình giao diện trang
st.set_page_config(
    page_title="Hệ Thống Đặt Món Trà Sữa", page_icon="🧋", layout="wide"
)

# --- HEADER / THÔNG TIN CÁ NHÂN ---
st.title("🧋 Hệ Thống Đặt Món & Quản Lý Trà Sữa")
st.markdown(
    "Chào mừng bạn đến với ứng dụng quản lý, phát triển bởi: **Nguyễn Hoàng Hân**"
)
st.markdown("---")

# Khởi tạo giỏ hàng trong session state
if "cart" not in st.session_state:
    st.session_state.cart = []

# --- MENU & DỮ LIỆU SẢN PHẨM ---
menu_prices = {
    "Trà Sữa Thái Xanh": {"S": 39000, "M": 45000, "L": 52000},
    "Trà Sữa Thái Đỏ": {"S": 39000, "M": 45000, "L": 52000},
    "Trà Sữa Matcha": {"S": 43000, "M": 49000, "L": 56000},
    "Trà Sữa Ô Long": {"S": 40000, "M": 46000, "L": 53000},
}

# Layout 2 cột: Cột trái để chọn món, Cột phải hiển thị giỏ hàng & hóa đơn
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.subheader("Chọn món nước & Tùy chọn")

    # Thông tin khách hàng
    customer_name = st.text_input("Tên khách hàng", value="Khách lẻ")

    # Chọn loại trà sữa
    selected_tea = st.selectbox(
        "Loại trà sữa", list(menu_prices.keys()), key="tea_type"
    )

    # Các tùy chọn Size, Mức đường, Mức đá
    row_opt1, row_opt2, row_opt3 = st.columns(3)
    with row_opt1:
        size = st.selectbox("Size", ["S", "M", "L"])
    with row_opt2:
        sugar = st.selectbox(
            "Mức đường", ["100% (Bình thường)", "70%", "50%", "30%", "0%"]
        )
    with row_opt3:
        ice = st.selectbox(
            "Mức đá", ["100% (Bình thường)", "70%", "50%", "30%", "0%"]
        )

    # Topping
    toppings_list = [
        "Trân châu trắng",
        "Trân châu đen",
        "Thạch phô mai",
        "Pudding trứng",
        "Rau câu",
    ]
    selected_toppings = st.multiselect(
        "Loại Topping (có thể chọn nhiều)", toppings_list
    )

    # Số lượng và đơn giá tạm tính
    row_qty1, row_qty2 = st.columns([1, 2])
    with row_qty1:
        quantity = st.number_input("Số lượng", min_value=1, value=1, step=1)

    # Tính giá cơ bản theo size
    base_price = menu_prices[selected_tea][size]
    # Cộng thêm tiền topping (mỗi loại topping + 7,000 VND chẳng hạn)
    topping_price = len(selected_toppings) * 7000
    unit_price = base_price + topping_price

    with row_qty2:
        st.markdown(f"<br>**Đơn giá:** {unit_price:,} VND", unsafe_allow_html=True)

    # Nút thêm vào giỏ hàng
    if st.button("Thêm vào giỏ hàng", type="primary"):
        item = {
            "name": selected_tea,
            "size": size,
            "sugar": sugar,
            "ice": ice,
            "toppings": selected_toppings,
            "quantity": quantity,
            "unit_price": unit_price,
            "total_price": unit_price * quantity,
        }
        st.session_state.cart.append(item)
        st.success(f"Đã thêm {quantity}x {selected_tea} (Size {size}) vào giỏ!")

with col_right:
    st.subheader("🛒 Giỏ hàng của bạn")

    if not st.session_state.cart:
        st.info("Giỏ hàng đang trống. Vui lòng chọn món ở bên trái.")
    else:
        total_bill = 0
        for idx, cart_item in enumerate(st.session_state.cart):
            with st.container():
                st.markdown(
                    f"**{idx+1}. {cart_item['name']} (Size {cart_item['size']})**"
                )
                st.markdown(
                    f"- Đường: {cart_item['sugar']} | Đá: {cart_item['ice']}"
                )
                if cart_item["toppings"]:
                    st.markdown(
                        f"- Topping: {', '.join(cart_item['toppings'])}"
                    )
                st.markdown(
                    f"- SL: {cart_item['quantity']} x {cart_item['unit_price']:,} = **{cart_item['total_price']:,} VND**"
                )
                st.markdown("---")
                total_bill += cart_item["total_price"]

        st.markdown(f"### Tổng tiền: {total_bill:,} VND")

        # Nút thanh toán / xuất hóa đơn
        if st.button("💳 Xác nhận thanh toán"):
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            invoice_content = f"========================================\n"
            invoice_content += f"HÓA ĐƠN BÁN HÀNG - TRÀ SỮA\n"
            invoice_content += f"Ngày: {now_str}\n"
            invoice_content += (
                f"Thu ngân / Người quản lý hệ thống: Nguyễn Hoàng Hân\n"
            )
            invoice_content += f"Khách hàng: {customer_name}\n"
            invoice_content += f"========================================\n"

            for idx, c_item in enumerate(st.session_state.cart):
                invoice_content += (
                    f"{idx+1}. {c_item['name']} ({c_item['size']})\n"
                )
                invoice_content += (
                    f"   - Đường: {c_item['sugar']} | Đá: {c_item['ice']}\n"
                )
                if c_item["toppings"]:
                    invoice_content += (
                        f"   - Topping: {', '.join(c_item['toppings'])}\n"
                    )
                invoice_content += f"   - SL: {c_item['quantity']} x {c_item['unit_price']:,} = {c_item['total_price']:,} VND\n"

            invoice_content += f"----------------------------------------\n"
            invoice_content += f"TỔNG THANH TOÁN: {total_bill:,} VND\n"
            invoice_content += f"========================================\n"
            invoice_content += (
                f"Cảm ơn quý khách và hẹn gặp lại! (Dev: Nguyễn Hoàng Hân)"
            )

            st.success("Thanh toán thành công!")

            # Cung cấp nút tải hóa đơn dưới dạng text file (giống hệt dạng Notepad trong ảnh mẫu)
            st.download_button(
                label="📥 Tải xuống hóa đơn (.txt)",
                data=invoice_content,
                file_name=f"HoaDon_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
            )

        # Nút xóa giỏ hàng
        if st.button("Xóa giỏ hàng"):
            st.session_state.cart = []
            st.rerun()
