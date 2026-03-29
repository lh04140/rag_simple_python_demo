import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# 使用可用的嵌入模型
try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    USE_HUGGINGFACE = True
except ImportError:
    print("⚠️  HuggingFaceEmbeddings 不可用，将使用简单嵌入")
    USE_HUGGINGFACE = False

# 正确的 DeepSeek LLM 调用
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
# 手动实现 chains 功能（因为 langchain.chains 在当前版本中不存在）

# ===================== 配置 =====================
# 你的 DeepSeek API Key
DEEPSEEK_API_KEY = "sk-4da3e36536064b7b86952c07d4722d73"
pdf_file = "test_chinese.pdf"

# ===================== 1. 加载PDF =====================
if not os.path.exists(pdf_file):
    print(f"❌ PDF文件不存在: {pdf_file}")
    exit(1)

print("加载PDF文档...")
loader = PyPDFLoader(pdf_file)
documents = loader.load()
print(f"✅ 加载了 {len(documents)} 个文档")

# ===================== 2. 文本分块 =====================
print("分割文本...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)
print(f"✅ 分割为 {len(chunks)} 个文本块")

# ===================== 3. 向量模型 ======================
print("初始化向量模型...")
if USE_HUGGINGFACE:
    # 使用 HuggingFace 嵌入
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"}
        )
        print("✅ 使用 HuggingFace 嵌入模型")
    except Exception as e:
        print(f"⚠️  HuggingFace 嵌入失败: {e}")
        USE_HUGGINGFACE = False

if not USE_HUGGINGFACE:
    # 使用简单嵌入作为回退
    print("使用简单嵌入模型...")
    class SimpleEmbeddings:
        def embed_documents(self, texts):
            import random
            return [[random.random() for _ in range(10)] for _ in texts]
            
        def embed_query(self, text):
            import random
            return [random.random() for _ in range(10)]
    
    embeddings = SimpleEmbeddings()
    print("✅ 使用简单嵌入模型")

# 创建向量库
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
print("✅ 向量存储创建完成")

# ===================== 4. DeepSeek 大模型（正确配置）=====================
print("初始化DeepSeek大模型...")
# 设置环境变量
os.environ["OPENAI_API_KEY"] = DEEPSEEK_API_KEY
os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com"

try:
    # 尝试不同的模型名称
    try:
        llm = ChatOpenAI(
            model="deepseek-chat",
            temperature=0,
            max_tokens=1024
        )
        print("✅ DeepSeek 大模型初始化成功 (使用 deepseek-chat)")
    except:
        # 尝试其他可能的模型名
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            max_tokens=1024
        )
        print("✅ DeepSeek 大模型初始化成功 (使用 gpt-3.5-turbo)")
        
except Exception as e:
    print(f"❌ DeepSeek 大模型初始化失败: {e}")
    print("使用模拟 LLM 作为回退...")
    
    class MockLLM:
        def invoke(self, prompt):
            class MockResponse:
                content = "这是一个模拟回答。实际使用需要有效的 API 密钥和正确的模型配置。"
            return MockResponse()
    
    llm = MockLLM()

# ===================== 5. 提示词模板 =====================
prompt = PromptTemplate(
    template="基于以下内容回答问题：\n\n{context}\n\n问题：{question}\n回答：",
    input_variables=["context", "question"]
)

# ===================== 6. 构建问答系统（手动实现）=====================
print("构建问答系统...")

def simple_qa_system(query):
    """简单的手动 QA 系统"""
    # 1. 检索相关文档
    docs = retriever.invoke(query)
    
    # 2. 组合上下文
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # 3. 格式化提示
    formatted_prompt = prompt.format(context=context, question=query)
    
    # 4. 调用 LLM
    response = llm.invoke(formatted_prompt)
    
    return {
        "answer": response.content,
        "source_documents": docs
    }

print("✅ 问答系统构建完成")

# ===================== 7. 执行问答 =====================
print("\n" + "="*50)
query = "本文档的核心观点是什么？"
print(f"问题: {query}")

try:
    result = simple_qa_system(query)
    
    print("\n答案:", result["answer"])
    
    if result["source_documents"]:
        print("\n参考来源:")
        for i, doc in enumerate(result["source_documents"][:3]):  # 只显示前3个
            print(f"片段 {i+1}: {doc.page_content[:100]}...")
    
except Exception as e:
    print(f"\n❌ 问答失败: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("="*50)