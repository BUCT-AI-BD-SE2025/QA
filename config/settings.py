# config/settings_config.py

POSTGRES = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'qa',
    'USER': 'postgres',
    'PASSWORD': '1qaz2wsx',
    'HOST': 'localhost',
    'PORT': '5432',
}

NEO4J = {
    'URI': 'neo4j+s://32ed3653.databases.neo4j.io',
    'USER': 'neo4j',
    'PASSWORD': 'FEvyWPh7BVdppt5CeW-nBpyYRNd2HhYurBlfrXdoiDo',
}

MODEL_CONFIG = {
    'api_key': 'sk-qvqjsmokunbbhetkcvvmsxoanuoiyarxbqxlsjdkfhrzpebi',
    'base_url': 'https://api.siliconflow.cn/v1',
    'model': 'deepseek-ai/DeepSeek-V3',
    'max_tokens' : 512,
    'temperature': 0.7
}
