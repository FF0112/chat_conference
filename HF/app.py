import gradio as gr
import random
import time
from typing import List
from datetime import datetime

# 模擬模型回應的類
class Model:
    def __init__(self, name: str, is_authoritative: bool = False):
        self.name = name
        self.is_authoritative = is_authoritative

    def generate_response(self, question: str) -> str:
        return f"{self.name} 的回答：對於 '{question}'，我認為這是一個合理的觀點，基於我的知識..."

# 模擬 API 調用
def call_model_api(model: Model, question: str) -> str:
    time.sleep(random.uniform(0.1, 0.5))
    return model.generate_response(question)

# 權威模型統整
def authoritative_synthesis(responses: List[str], auth_model: Model, question: str) -> str:
    return f"{auth_model.name} 統整：基於問題 '{question}'，綜合分析如下：\n" + "\n".join(responses)

# 辯證過程
def debate_round(debater1: Model, debater2: Model, questioner: Model, recorder: Model, question: str, round_num: int) -> str:
    q = questioner.generate_response(f"針對 '{question}' 的第 {round_num} 輪提問")
    r1 = debater1.generate_response(q)
    r2 = debater2.generate_response(q)
    return recorder.generate_response(f"第 {round_num} 輪記錄：\n提問：{q}\n{debater1.name} 說：{r1}\n{debater2.name} 說：{r2}")

# 主流程
def collaborative_ai(question: str, num_models: int, num_rounds: int) -> str:
    if num_models < 4:
        return "錯誤：模型數量需至少為 4。"
    if num_rounds < 1:
        return "錯誤：辯證輪數需至少為 1。"
    
    # 初始化模型
    models = [Model(f"Model-{i}") for i in range(num_models)]
    authoritative_model = Model("Authoritative-Model", is_authoritative=True)

    # 第一階段：各模型回答
    responses = [call_model_api(model, question) for model in models]

    # 第二階段：權威模型統整
    initial_synthesis = authoritative_synthesis(responses, authoritative_model, question)

    # 第三階段：多輪辯證
    debate_records = []
    for round_num in range(1, num_rounds + 1):
        random.shuffle(models)
        debater1, debater2, questioner, recorder = models[:4]
        debate_record = debate_round(debater1, debater2, questioner, recorder, question, round_num)
        debate_records.append(debate_record)

    # 最終統整
    final_result = authoritative_model.generate_response(
        f"最終統整：\n初始回答：{initial_synthesis}\n辯論記錄：\n" + "\n".join(debate_records)
    )

    # 準備 Markdown 輸出
    markdown_content = f"# 問題：{question}\n\n"
    markdown_content += f"## 初始回答\n{initial_synthesis}\n\n"
    markdown_content += f"## 辯論記錄\n" + "\n\n".join(debate_records) + "\n\n"
    markdown_content += f"## 最終結論\n{final_result}\n\n"
    markdown_content += f"生成時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    return markdown_content

# Gradio 界面
iface = gr.Interface(
    fn=collaborative_ai,
    inputs=[
        gr.Textbox(label="問題", placeholder="輸入您的問題"),
        gr.Slider(minimum=4, maximum=10, step=1, value=4, label="模型數量"),
        gr.Slider(minimum=1, maximum=5, step=1, value=3, label="辯證輪數")
    ],
    outputs=gr.Markdown(label="結果"),
    title="多模型協作回答系統",
    description="輸入問題，選擇模型數量和辯證輪數，系統將模擬多模型協作並生成結果。"
)

if __name__ == "__main__":
    iface.launch()
