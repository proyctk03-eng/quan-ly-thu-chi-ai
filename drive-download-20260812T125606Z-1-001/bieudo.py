from graphviz import Digraph


def ve_so_do_quy_trinh_ban_hang():
    # Khởi tạo đồ thị
    dot = Digraph(
        name="QuyTrinhBanHang",
        comment="Sơ đồ BPMN - Quy trình bán hàng",
        format="png"
    )

    # Thiết lập hướng vẽ từ trên xuống dưới
    dot.attr(
        rankdir="TB",
        splines="ortho",
        nodesep="0.5",
        ranksep="0.7",
        bgcolor="white",
        label="Hình 1: Sơ đồ quy trình bán hàng",
        labelloc="b",
        fontsize="14",
        fontname="Arial"
    )

    # Thiết lập kiểu mặc định cho các nút
    dot.attr(
        "node",
        shape="box",
        style="rounded,filled",
        fillcolor="white",
        color="#2F5597",
        fontname="Arial",
        fontsize="11",
        margin="0.15"
    )

    # Thiết lập kiểu mặc định cho các đường nối
    dot.attr(
        "edge",
        color="#555555",
        fontname="Arial",
        fontsize="10",
        arrowsize="0.8"
    )

    # Các bước xử lý
    dot.node("A", "Khách đến cửa hàng", shape="ellipse",
             fillcolor="#D9EAD3", color="#38761D")

    dot.node("B", "Nhân viên tiếp nhận\nnhu cầu")

    # Nút quyết định
    dot.node("C", "Dùng AI\ntư vấn?", shape="diamond",
             fillcolor="#FFF2CC", color="#BF9000")

    dot.node("D", "Nhập nhu cầu vào\nChatbot AI",
             fillcolor="#D9EAF7")

    dot.node("E", "Nhân viên tự tra cứu\nsản phẩm",
             fillcolor="#FCE5CD")

    dot.node("F", "AI gợi ý sản phẩm",
             fillcolor="#D9EAF7")

    dot.node("G", "Khách chọn sản phẩm")
    dot.node("H", "Nhân viên tạo hóa đơn")
    dot.node("I", "Hệ thống kiểm tra\ntồn kho")

    # Nút quyết định tồn kho
    dot.node("J", "Tồn kho\nđủ?", shape="diamond",
             fillcolor="#FFF2CC", color="#BF9000")

    dot.node("K", "Thông báo hết hàng",
             fillcolor="#F4CCCC", color="#990000")

    dot.node("L", "Tính tổng tiền\nvà giảm giá")
    dot.node("M", "Khách thanh toán")
    dot.node("N", "Lưu hóa đơn\nTrừ tồn kho")
    dot.node("O", "In hóa đơn")

    dot.node("P", "Giao hàng - Kết thúc",
             shape="ellipse",
             fillcolor="#D9EAD3", color="#38761D")

    # Các luồng xử lý
    dot.edge("A", "B")
    dot.edge("B", "C")

    dot.edge("C", "D", label="Có")
    dot.edge("C", "E", label="Không")

    dot.edge("D", "F")
    dot.edge("F", "G")
    dot.edge("E", "G")

    dot.edge("G", "H")
    dot.edge("H", "I")
    dot.edge("I", "J")

    dot.edge("J", "K", label="Không")
    dot.edge("J", "L", label="Có")

    dot.edge("L", "M")
    dot.edge("M", "N")
    dot.edge("N", "O")
    dot.edge("O", "P")

    # Xuất file PNG
    output_path = dot.render(
        filename="so_do_quy_trinh_ban_hang.png",
        cleanup=True
    )

    print(f"Đã tạo sơ đồ: {output_path}")


if __name__ == "__main__":
    ve_so_do_quy_trinh_ban_hang()