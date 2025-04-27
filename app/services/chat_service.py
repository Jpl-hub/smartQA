import requests
from typing import Dict

class ChatService:
    def __init__(self):
        self.api_key = "sk-owciyggqpjmjgqnnhhbganzfayhyhpqnllgefajgoipbuidz"
        self.api_url = "https://api.siliconflow.cn/v1/chat/completions"
        self.model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
    
    def get_ai_response(self, user_message: str) -> str:
        """
        调用硅基流动平台API获取AI回答
        """
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "stream": False,
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(self.api_url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            raise Exception(f"API调用失败: {response.text}")