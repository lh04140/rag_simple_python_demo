from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def create_chinese_pdf(filename):
    # 注册中文字体
    # 使用系统自带的宋体
    font_path = "/System/Library/Fonts/Supplemental/Songti.ttc"
    
    if os.path.exists(font_path):
        # 注册字体，Songti 是字体族名，0 表示常规字体
        pdfmetrics.registerFont(TTFont('Songti', font_path, subfontIndex=0))
        chinese_font = 'Songti'
    else:
        print("警告：未找到宋体字体，将使用默认字体（可能不支持中文）")
        chinese_font = 'Helvetica'
    
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # 标题 - 使用中文字体
    c.setFont(chinese_font, 16)
    c.drawString(72, height - 72, "RAG（检索增强生成）技术概述")

    # 正文
    c.setFont(chinese_font, 12)
    y = height - 100

    text = """RAG 是一种将信息检索与大语言模型（LLM）结合的技术框架。它通过从外部知识库中检索相关文档，作为生成答案的上下文，有效解决了 LLM 的幻觉问题，并能够利用私有或实时数据。

主要流程：
1. 文档加载：从各种数据源（如 PDF、网页、数据库）加载原始文档。
2. 文本分块：将长文档切分为语义完整的文本块。
3. 向量化与存储：使用嵌入模型将文本块转换为向量，存入向量数据库。
4. 检索：用户提问时，将问题向量化，在数据库中检索最相似的文本块。
5. 生成：将检索到的文本块与问题组合成提示词，送入 LLM 生成答案。

应用场景：
- 智能客服：基于产品手册回答用户问题。
- 企业知识库：快速检索内部文档，辅助员工决策。
- 学术研究：从论文库中提取信息，辅助写作。

LangChain 作为 RAG 实现的常用框架，提供了模块化的工具链，可以快速搭建原型并投入生产。"""

    # 更好的文本处理方法
    lines = []
    for paragraph in text.split('\n'):
        if paragraph.strip() == "":
            lines.append("")  # 空行
            continue
            
        # 简单的文本换行处理
        words = paragraph
        line = ""
        for char in words:
            line += char
            # 每行大约40个字符换行
            if len(line) >= 40 and char in '，。；：！？、':
                lines.append(line)
                line = ""
        if line:
            lines.append(line)
    
    # 绘制文本
    for line in lines:
        if line == "":
            y -= 10  # 空行间距小一些
        else:
            c.drawString(72, y, line)
            y -= 20  # 行间距
        
        if y < 72:
            c.showPage()
            y = height - 72
            c.setFont(chinese_font, 12)

    c.save()
    print(f"PDF 已生成：{filename}")

if __name__ == "__main__":
    create_chinese_pdf("test_chinese.pdf")