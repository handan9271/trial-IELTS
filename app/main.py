from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.mount("/", StaticFiles(directory="static", html=True), name="static")

class IELTSRequest(BaseModel):
    question: str
    input: str

@app.post("/api/ielts-helper")
async def ielts_helper(req: IELTSRequest):
    prompt = f"""你是一位面向雅思6分以下考生的 AI 写作与口语助教，帮助学生将中文思路转化为结构清晰、语言丰富、逐步提升的英文表达，并引导他们掌握提分关键表达。你的任务包括以下五步：
1. 提出一个5.5分左右的英文回答；
2. 在每个句子后附上中文翻译；
3. 逐步优化语言（句式更丰富、词汇更高级）；
4. 拆解亮点词汇并给出例句；
5. 给出完整高分版本。
以下是学生的作答思路：
{req.input}
请根据上面的内容，输出完整5步反馈，尽量简洁，避免重复。"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"reply": response.choices[0].message.content}
