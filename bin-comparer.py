import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import os

def compare_files(file1_path, file2_path):
    with open(file1_path, 'rb') as f1, open(file2_path, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()

    len1, len2 = len(data1), len(data2)
    total_diff = 0
    diff_masks = []

    for i in range(len1):
        if i < len2:
            mask = data1[i] ^ data2[i]
        else:
            mask = 0xFF
        diff_masks.append(mask)
        total_diff += bin(mask).count('1')

    if len2 > len1:
        total_diff += (len2 - len1) * 8

    return data1, diff_masks, total_diff


def generate_html_report(data1, diff_masks, total_diff, file1_path, file2_path, save_path):
    html_lines = []
    html_lines.append("<!DOCTYPE html>")
    html_lines.append("<html>")
    html_lines.append("<head>")
    html_lines.append("    <meta charset='utf-8'>")
    html_lines.append("    <title>二进制文件比较结果</title>")
    html_lines.append("    <style>")
    html_lines.append("        body { font-family: 'Courier New', monospace; margin: 20px; font-size: 16px; }")
    html_lines.append("        .header { margin-bottom: 20px; }")
    html_lines.append("        .controls { margin: 15px 0; }")
    html_lines.append("        .controls button { padding: 6px 16px; font-size: 14px; cursor: pointer; }")
    html_lines.append("        .controls span { margin-left: 15px; font-weight: bold; font-size: 14px; }")
    html_lines.append("        .byte-row { font-size: 14px; line-height: 1.6; }")
    html_lines.append("        .byte-group { display: inline-block; margin-right: 12px; }")
    html_lines.append("        .diff { color: red; font-weight: bold; }")
    html_lines.append("        .same { color: black; }")
    html_lines.append("        .offset { color: #0066cc !important; font-weight: bold; margin-right: 20px; }")  # 强制蓝色
    html_lines.append("        .compact-mode .byte-row[data-has-diff='false'] { display: none; }")
    html_lines.append("    </style>")
    html_lines.append("</head>")
    html_lines.append("<body>")

    html_lines.append("    <div class='header'>")
    html_lines.append(f"        <h2>二进制文件比较结果</h2>")
    html_lines.append(f"        <p><strong>文件1：</strong>{file1_path}</p>")
    html_lines.append(f"        <p><strong>文件2：</strong>{file2_path}</p>")
    html_lines.append(f"        <p><strong>总不同位数：</strong>{total_diff}</p>")
    html_lines.append("    </div>")

    if total_diff == 0:
        html_lines.append("    <p>两个文件完全相同。</p>")
    else:
        html_lines.append("    <p>以下以第一个文件为基准，每行显示8个字节，红色位表示与文件2不同。</p>")
        html_lines.append("    <div class='controls'>")
        html_lines.append("        <button onclick='toggleMode()'>切换模式</button>")
        html_lines.append("        <span id='modeLabel'>当前：详细模式</span>")
        html_lines.append("    </div>")
        html_lines.append("    <div id='content'>")

        bytes_per_row = 8
        total_bytes = len(data1)
        for start in range(0, total_bytes, bytes_per_row):
            end = min(start + bytes_per_row, total_bytes)
            row_has_diff = False
            row_parts = []
            for i in range(start, end):
                byte = data1[i]
                mask = diff_masks[i]
                if mask != 0:
                    row_has_diff = True
                bit_spans = []
                for bit_pos in range(7, -1, -1):
                    bit_val = (byte >> bit_pos) & 1
                    is_diff = (mask >> bit_pos) & 1
                    cls = "diff" if is_diff else "same"
                    bit_spans.append(f"<span class='{cls}'>{bit_val}</span>")
                byte_html = "".join(bit_spans)
                row_parts.append(f"<span class='byte-group'>{byte_html}</span>")
            row_html = "".join(row_parts)
            offset_str = f"0x{start:04X}"
            html_lines.append(
                f"        <div class='byte-row' data-has-diff='{str(row_has_diff).lower()}'><span class='offset'>{offset_str}</span> {row_html}</div>"
            )

        html_lines.append("    </div>")

    # JavaScript 切换逻辑（利用class切换，极速响应）
    html_lines.append("    <script>")
    html_lines.append("        let isDetailed = true;")
    html_lines.append("        function toggleMode() {")
    html_lines.append("            const content = document.getElementById('content');")
    html_lines.append("            const label = document.getElementById('modeLabel');")
    html_lines.append("            if (isDetailed) {")
    html_lines.append("                content.classList.add('compact-mode');")
    html_lines.append("                label.textContent = '当前：精简模式';")
    html_lines.append("            } else {")
    html_lines.append("                content.classList.remove('compact-mode');")
    html_lines.append("                label.textContent = '当前：详细模式';")
    html_lines.append("            }")
    html_lines.append("            isDetailed = !isDetailed;")
    html_lines.append("        }")
    html_lines.append("    </script>")

    html_lines.append("</body>")
    html_lines.append("</html>")

    with open(save_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(html_lines))


def main():
    root = tk.Tk()
    root.withdraw()

    file1 = filedialog.askopenfilename(title="选择第一个二进制文件")
    if not file1:
        messagebox.showinfo("提示", "未选择文件，程序退出。")
        return

    file2 = filedialog.askopenfilename(title="选择第二个二进制文件")
    if not file2:
        messagebox.showinfo("提示", "未选择文件，程序退出。")
        return

    try:
        data1, diff_masks, total_diff = compare_files(file1, file2)
    except Exception as e:
        messagebox.showerror("错误", f"读取或比较文件时出错：{e}")
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".html",
        filetypes=[("HTML文件", "*.html"), ("所有文件", "*.*")],
        title="保存HTML报告"
    )
    if not save_path:
        messagebox.showinfo("提示", "未选择保存路径，程序退出。")
        return

    try:
        generate_html_report(data1, diff_masks, total_diff, file1, file2, save_path)
        # 询问是否打开
        if messagebox.askyesno("完成", f"HTML报告已保存至：\n{save_path}\n\n是否立即打开？"):
            webbrowser.open(save_path)
    except Exception as e:
        messagebox.showerror("错误", f"保存HTML文件时出错：{e}")


if __name__ == "__main__":
    main()