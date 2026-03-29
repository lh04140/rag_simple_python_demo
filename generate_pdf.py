from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_test_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # 标题
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, "RAG（检索增强生成）技术概述")

    # 正文
    c.setFont("Helvetica", 12)
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

    for line in text.split('\n'):
        c.drawString(72, y, line)
        y -= 15
        if y < 72:
            c.showPage()
            y = height - 72

    c.save()

create_test_pdf("test.pdf")
print("PDF 已生成：test.pdf")