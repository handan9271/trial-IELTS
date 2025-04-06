from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class IELTSRequest(BaseModel):
    question: str
    input: str

@app.post("/api/ielts-helper")
async def ielts_helper(request: IELTSRequest):
    prompt = f"""你是一位面向雅思6分以下考生的 AI 写作与口语助教，帮助学生将中文思路转化为结构清晰、语言丰富、逐步提升的英文表达，并引导他们掌握提分关键表达。你的任务包括以下五步：

【第1步：主动提问】
题目如下：{request.question}
学生中文思路：{request.input}

请从【第2步】开始逐步输出。每一步都用 Markdown 清晰标注标题，例如“【第2步：TEEL结构英文表达（逐句输出 + 中文翻译 + 高亮表达）】”，并按以下规则格式输出：

【第2步：TEEL结构英文表达（逐句输出 + 中文翻译 + 高亮表达）】
T: ...
👉 中文翻译：...
✨ 高亮表达：**高亮内容**

【第3步：词汇讲解】
英文词汇：...
中文释义：...
例句：...

【第4步：AI评分 + 中文建议】
🎯 模拟分数：Band X.X
✅ 优点：
🔧 建议：

【第5步：高分参考段落】
T: ...
👉 中文翻译：...
✨ 高亮表达：...

请严格遵循上方五个步骤依次输出。"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"reply": response.choices[0].message.content}
