
from config.settings import MODEL_CONFIG


class ModelConfig:
    def __init__(self, base_url: str, api_key: str = None, model: str = "deepseek-ai/DeepSeek-V3",max_tokens: int = 512,temperature: float = 0.7):

        self.model = model
        self.base_url = base_url
        self.api_key = api_key
        self.max_tokens = max_tokens
        self.temperature = temperature

    def bulid_model_data(self):
        """
        构建模型数据
        除去api_key的敏感信息
        :return: dict
        """
        model_data = {
            "base_url": self.base_url,
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
        return model_data
    

model_config1 = ModelConfig(
    api_key=MODEL_CONFIG['api_key'],
    base_url=MODEL_CONFIG['base_url'],
    model=MODEL_CONFIG['model'],
    max_tokens=MODEL_CONFIG['max_tokens'],
    temperature=MODEL_CONFIG['temperature']
)
