<div align="center">

# 🔍 bin-comparer

[English](./README.en.md) | [简体中文](./README.md)

A lightweight binary file comparison tool with a graphical interface, enabling bit-level analysis of two files and generating intuitive HTML reports.

</div>

## ✨ Features

- 🖱️ **Graphical Operation** – Based on `tkinter`, select two binary files via dialogs, no command line required.
- 📊 **Difference Statistics** – Accurately count total differing bits (including all extra bits when file lengths differ).
- 🔴 **Highlight Display** – Using the first file as reference, mark differing bits in red and identical bits in black within the HTML report.
- 🚀 **Two View Modes**:
  - **Detailed Mode** – Shows all bytes for comprehensive review.
  - **Compact Mode** – Automatically hides rows with no differences (all 8 bytes identical), helping you focus on changed areas.
- ⚡ **Performance Optimized** – Leverages CSS `content-visibility` for on‑demand rendering, ensuring smooth mode switching even with hundreds of thousands of rows.
- 📁 **Easy Export** – Save as an HTML file with one click, and optionally open it immediately in your default browser.

## 📁 Project Structure

```markdown
bin-comparer/
├── bin_comparer.py    # Main program (Python script)
└── README.md          # Chinese documentation
└── README.en.md       # English documentation (this file)
```

- **Single‑file program** – All logic is contained in one Python script, no extra dependencies, copy and run.

## 🚀 How to Use

### Requirements

- Python 3.6 or higher
- Standard library modules (no extra installation needed):
  - `tkinter` (usually bundled with Python)
  - `webbrowser`
  - `os`

### 1. Run the Program

In your terminal:

```bash
python bin_comparer.py
```

### 2. Select Files

- A dialog appears to choose the first binary file (used as the reference).
- Then a second dialog appears to choose the second file for comparison.

### 3. Save the Report

- After comparison, a “Save HTML Report” dialog appears; specify the save path and filename (default extension `.html`).
- Upon successful save, you are asked whether to open it immediately in your default browser.

### 4. Interactive Viewing

- The HTML page shows both file paths and the total number of differing bits at the top.
- Each row displays 8 bytes, with each byte's 8 bits shown from most significant to least significant; the offset (in blue) is at the start of each row.
- Click the **“Toggle Mode”** button to switch between Detailed and Compact modes. The label updates instantly, and the UI responds smoothly without lag.

## 📄 Report Example (Partial)

```
0x0000  10101010 11110000 00001111 11111111 00000000 01010101 10101010 01010101
0x0008  11001100 00110011 10101010 01010101  ....................   (red bits indicate differences)
```

- All red bits differ from the second file; black bits are identical.
- In Compact mode, rows with no red bits are hidden to help pinpoint differences.

## 🎨 Customization & Extension

- **Change bytes per row**: Locate `bytes_per_row = 8` inside the `generate_html_report` function and modify it (keeping it a multiple of 8 is recommended for alignment).
- **Adjust font size**: Edit the `font-size` property for `body` or `.byte-row` in the HTML template's `<style>` section.
- **Change offset color**: Modify the `color` value for `.offset` (default is `#0066cc`).
- **Add more features**: Extend the `compare_files` function, for example to generate statistical charts.

## 🌐 Browser Compatibility

The generated HTML report works in all modern browsers (Chrome, Firefox, Safari, Edge). For best performance with `content-visibility`, we recommend Chrome 85+ or Firefox 109+.

## 🧠 Technical Highlights

- **Bit‑wise Comparison** – Compares byte by byte using XOR to generate difference masks, enabling efficient statistics.
- **HTML Rendering Optimization** – Uses `content-visibility: auto` and `contain-intrinsic-size` to render only visible rows, so mode switching only recalculates styles for the viewport, drastically reducing reflow time.
- **Instant Feedback** – The mode label updates immediately upon button click, while style changes are applied asynchronously in the next frame for a snappy feel.

## ⚠️ Limitations

- The program reads both files entirely into memory. For very large files (>500 MB), this may cause memory exhaustion. It is best suited for files of moderate size (e.g., firmware, logs, small databases).
- If there are many differences, the generated HTML file can become large, but modern browsers handle it without issues.

## 📄 License

This project is open‑source under the [MIT License](https://opensource.org/licenses/MIT). You are free to use, modify, and distribute it.

## 🤝 Contributing

Issues and Pull Requests are welcome!

---

**Enjoy comparing! 🎉**
