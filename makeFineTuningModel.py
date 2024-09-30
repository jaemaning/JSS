import json
import tiktoken
from openai import OpenAI
import dotenv

dotenv_path = dotenv.find_dotenv()
APIKEY = dotenv.get_key(dotenv_path, "GPT_SECRET_KEY")
print(APIKEY)
client = OpenAI(api_key=APIKEY)

# tiktoken 인코딩 설정 (예: GPT-3.5를 위한 인코딩 사용)
encoding = tiktoken.get_encoding("cl100k_base")
print(encoding)

# # JSONL 파일 경로
file_path = './data/data_conversational.jsonl'
tokenCnt = 0

# # JSONL 파일을 열고 각 줄을 읽어서 처리
with open(file_path, 'r', encoding='utf-8') as file:
    for line_number, line in enumerate(file, start=1):
        try:
            # 각 줄을 JSON 객체로 변환
            data = json.loads(line.strip())
            
            # prompt 값 가져오기
            messages = data.get('messages', '')
            
            # 인코딩하여 길이 계산
            messages_length = 0
            for i in range(3):
              messages_length += len(encoding.encode(messages[i]['content']))
            
            tokenCnt += messages_length

            # 결과 출력
            print(f"Line {line_number}: Prompt 길이 = {messages_length} 토큰")

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON on line {line_number}: {e}")
            
print(f"모든 토큰 합 : {tokenCnt} 토큰")
# Gpt-4o-mini 의 경우 Fine-tuning training 비용은 3$ / 1M training token
print(f"발생 예상 비용 : $ {tokenCnt*3 / int(1e6)}")

# resId = 'file-ELe7pw9YshCihQN17vmG3CVS'
# res = client.files.create(
#   file=open("data/data_conversational.jsonl", "rb"),
#   purpose="fine-tune"
# )

# resId = res.id
# print(f"trained file id : {resId}")

# response = client.fine_tuning.jobs.create(
#   training_file=resId,
#   model="gpt-4o-mini-2024-07-18", 
#   hyperparameters={
#     "n_epochs":5,
#     "batch_size": 1
#   }
# )

# print(response)