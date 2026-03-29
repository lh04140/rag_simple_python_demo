from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def create_simple_chinese_pdf(filename):
    # 尝试使用黑体，macOS 系统通常有
    font_paths = [
        "/System/Library/Fonts/STHeiti Medium.ttc",  # 黑体
        "/System/Library/Fonts/Supplemental/Songti.ttc",  # 宋体
        "/System/Library/Fonts/PingFang.ttc",  # 苹方
    ]
    
    chinese_font = 'Helvetica'  # 默认
    font_registered = False
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font_name = os.path.basename(font_path).split('.')[0]
                pdfmetrics.registerFont(TTFont(font_name, font_path, subfontIndex=0))
                chinese_font = font_name
                font_registered = True
                print(f"使用字体: {font_name}")
                break
            except Exception as e:
                print(f"注册字体 {font_path} 失败: {e}")
                continue
    
    if not font_registered:
        print("警告：未找到合适的中文字体，将使用默认字体")
    
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # 标题
    c.setFont(chinese_font, 16)
    c.drawString(72, height - 72, "RAG技术概述")

    # 正文 - 使用更简单的文本避免复杂换行
    c.setFont(chinese_font, 12)
    y = height - 100
    
    # 分段绘制，每段单独处理
    paragraphs = [
        "RAG是一种将信息检索与大语言模型结合的技术框架。",
        "它通过从外部知识库中检索相关文档，作为生成答案的上下文。",
        "主要流程：文档加载、文本分块、向量化存储、检索、生成。",
        "应用场景：智能客服、企业知识库、学术研究。",
        "LangChain是RAG实现的常用框架。"
    ]
    
    for para in paragraphs:
        c.drawString(72, y, para)
        y -= 25
        if y < 72:
            c.showPage()
            y = height - 72
            c.setFont(chinese_font, 12)

    c.save()
    print(f"PDF已生成: {filename}")

if __name__ == "__main__":
    create_simple_chinese_pdf("test_simple.pdf")