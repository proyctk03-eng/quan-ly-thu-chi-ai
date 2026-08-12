# SCRIPT SINH SƠ ĐỒ QUY TRÌNH QUẢN LÝ THU CHI SINH VIÊN AI 🎓
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

def ve_so_do_quy_trinh_quan_ly_thu_chi():
    """Tạo sơ đồ luồng BPMN cho quy trình Quản lý Thu Chi Sinh viên AI sắc nét và chuyên nghiệp"""
    try:
        from graphviz import Digraph

        # Khởi tạo đồ thị Graphviz
        dot = Digraph(
            name="QuyTrinhQuanLyThuChi",
            comment="Sơ đồ BPMN - Quy trình Quản lý Thu Chi Sinh viên AI 🎓",
            format="png"
        )

        dot.attr(
            rankdir="TB",
            splines="ortho",
            nodesep="0.5",
            ranksep="0.7",
            bgcolor="white",
            label="Hình 1: Sơ đồ quy trình quản lý chi tiêu sinh viên AI 🎓",
            labelloc="b",
            fontsize="14",
            fontname="Arial"
        )

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

        dot.attr(
            "edge",
            color="#555555",
            fontname="Arial",
            fontsize="10",
            arrowsize="0.8"
        )

        dot.node("A", "Sinh viên mở Sổ Tay AI", shape="ellipse", fillcolor="#D9EAD3", color="#38761D")
        dot.node("B", "Nhập câu giao dịch / yêu cầu CSKH")
        dot.node("C", "Sử dụng Nút Tròn CSKH\n(FAB Popover Widget)?", shape="diamond", fillcolor="#FFF2CC", color="#BF9000")
        dot.node("D", "Nhập yêu cầu vào Popover CSKH\n(AI Agentic tự thực thi CRUD)", fillcolor="#D9EAF7")
        dot.node("E", "Nhập câu bóc tách tại Tab 2\nhoặc Form thủ công", fillcolor="#FCE5CD")
        dot.node("F", "Gemini Flash AI bóc tách tiền,\nquy đổi từ lóng & gán danh mục", fillcolor="#D9EAF7")
        dot.node("G", "Đánh giá Rủi ro Ví\n(warning_level)?", shape="diamond", fillcolor="#FFF2CC", color="#BF9000")
        dot.node("H", "Cảnh báo Báo động CRITICAL / WARNING\nTư vấn hệ lụy & tư tưởng tài chính", fillcolor="#F4CCCC", color="#990000")
        dot.node("I", "Xác nhận Chi tiêu SAFE\nAn toàn cho ngân sách sinh viên", fillcolor="#D9EAD3", color="#38761D")
        dot.node("J", "Lưu giao dịch & Hạn mức\nvào CSDL SQLite chi_tieu.db")
        dot.node("K", "Cập nhật UI Streamlit Metrics,\nTiến trình Hạn mức & Biểu đồ Plotly")
        dot.node("L", "Đồng bộ ví & Hoàn thành giao dịch", shape="ellipse", fillcolor="#D9EAD3", color="#38761D")

        dot.edge("A", "B")
        dot.edge("B", "C")
        dot.edge("C", "D", label="Có")
        dot.edge("C", "E", label="Không")
        dot.edge("D", "F")
        dot.edge("E", "F")
        dot.edge("F", "G")
        dot.edge("G", "H", label="Critical/Warning")
        dot.edge("G", "I", label="Safe")
        dot.edge("H", "J")
        dot.edge("I", "J")
        dot.edge("J", "K")
        dot.edge("K", "L")

        output_path = dot.render(filename="so_do_quy_trinh_quan_ly_thu_chi", cleanup=True)
        print(f"Đã tạo sơ đồ bằng Graphviz: {output_path}")

    except Exception:
        # High quality PIL rendering fallback with TrueType Arial font
        from PIL import Image, ImageDraw, ImageFont

        img = Image.new('RGB', (1000, 1300), color='#FFFFFF')
        draw = ImageDraw.Draw(img)

        font_path = 'C:/Windows/Fonts/arial.ttf'
        try:
            font_title = ImageFont.truetype(font_path, 20)
            font_node = ImageFont.truetype(font_path, 14)
            font_sm = ImageFont.truetype(font_path, 12)
        except Exception:
            font_title = font_node = font_sm = ImageFont.load_default()

        # Title
        draw.text((500, 40), 'Hình 1: Sơ đồ quy trình quản lý chi tiêu sinh viên AI 🎓', fill='#0F172A', font=font_title, anchor='mm')

        def draw_box(xy, text_str, bg='#FFFFFF', border='#2F5597', shape='rect', text_color='#0F172A'):
            x1, y1, x2, y2 = xy
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            if shape == 'ellipse':
                draw.ellipse(xy, fill=bg, outline=border, width=2)
            elif shape == 'diamond':
                draw.polygon([(cx, y1), (x2, cy), (cx, y2), (x1, cy)], fill=bg, outline=border, width=2)
            else:
                draw.rounded_rectangle(xy, radius=12, fill=bg, outline=border, width=2)

            lines = text_str.split('\n')
            line_height = 20
            start_y = cy - (len(lines) - 1) * (line_height / 2)
            for i, l in enumerate(lines):
                draw.text((cx, start_y + i * line_height), l, fill=text_color, font=font_node, anchor='mm')

        # Nodes
        draw_box([320, 90, 680, 150], 'Sinh viên mở ứng dụng Sổ Tay AI', bg='#D9EAD3', border='#38761D', shape='ellipse', text_color='#274E13')
        draw_box([300, 190, 700, 250], 'Nhập câu giao dịch hoặc yêu cầu CSKH')

        draw_box([280, 290, 720, 390], 'Sử dụng Nút Tròn CSKH\n(Floating Action Button)?', bg='#FFF2CC', border='#BF9000', shape='diamond', text_color='#7F6000')

        draw_box([80, 430, 420, 500], 'Nhập lệnh vào Popover CSKH\n(AI Agentic tự thực thi CRUD)', bg='#D9EAF7', border='#2F5597')
        draw_box([580, 430, 920, 500], 'Nhập tại Tab 2 Bóc Tách\nhoặc Form thủ công', bg='#FCE5CD', border='#E69138')

        draw_box([280, 540, 720, 610], 'Gemini Flash AI bóc tách tiền,\nquy đổi từ lóng & gán danh mục', bg='#D9EAF7', border='#2F5597')

        draw_box([280, 650, 720, 750], 'Đánh giá Rủi ro Ví\n(warning_level)?', bg='#FFF2CC', border='#BF9000', shape='diamond', text_color='#7F6000')

        draw_box([80, 790, 440, 860], 'Cảnh báo Báo động CRITICAL / WARNING\nTư vấn hệ lụy & tư tưởng tài chính', bg='#F4CCCC', border='#990000', text_color='#660000')
        draw_box([560, 790, 920, 860], 'Xác nhận Chi tiêu SAFE\nAn toàn cho ngân sách sinh viên', bg='#D9EAD3', border='#38761D', text_color='#274E13')

        draw_box([280, 900, 720, 960], 'Lưu giao dịch & Hạn mức vào CSDL\nSQLite chi_tieu.db')
        draw_box([280, 1000, 720, 1060], 'Cập nhật UI Streamlit Metrics,\nTiến trình Hạn mức & Biểu đồ Plotly')
        draw_box([320, 1100, 680, 1160], 'Đồng bộ ví & Hoàn thành giao dịch', bg='#D9EAD3', border='#38761D', shape='ellipse', text_color='#274E13')

        # Connectors
        def arrow(p1, p2, text_lbl=''):
            draw.line([p1, p2], fill='#555555', width=2)
            if text_lbl:
                mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
                draw.text((mx + 15, my - 10), text_lbl, fill='#555555', font=font_sm)

        arrow((500, 150), (500, 190))
        arrow((500, 250), (500, 290))

        arrow((280, 340), (250, 340))
        arrow((250, 340), (250, 430), 'Có')

        arrow((720, 340), (750, 340))
        arrow((750, 340), (750, 430), 'Không')

        arrow((250, 500), (250, 520))
        arrow((250, 520), (500, 520))
        arrow((500, 520), (500, 540))

        arrow((750, 500), (750, 520))
        arrow((750, 520), (500, 520))

        arrow((500, 610), (500, 650))

        arrow((280, 700), (260, 700))
        arrow((260, 700), (260, 790), 'Critical/Warning')

        arrow((720, 700), (740, 700))
        arrow((740, 700), (740, 790), 'Safe')

        arrow((260, 860), (260, 880))
        arrow((260, 880), (500, 880))
        arrow((500, 880), (500, 900))

        arrow((740, 860), (740, 880))
        arrow((740, 880), (500, 880))

        arrow((500, 960), (500, 1000))
        arrow((500, 1060), (500, 1100))

        out_img = os.path.join(os.path.dirname(__file__), "so_do_quy_trinh_quan_ly_thu_chi.png")
        img.save(out_img)
        print(f"Đã tạo sơ đồ quy trình sắc nét: {out_img}")

if __name__ == "__main__":
    ve_so_do_quy_trinh_quan_ly_thu_chi()
