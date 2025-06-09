// 使用 ES 模块导入方式
import express from 'express';
import cors from 'cors';
// 引入 node-fetch，这里使用动态导入以适配 ES 模块环境
import fetch from 'node-fetch';

// 创建 Express 应用实例
const app = express();

// 新增中间件，用于解析 JSON 请求体
app.use(express.json());

// 允许跨域请求
app.use(cors());

// 新增大模型路由（放在其他路由之前）
app.post('/llm/chat', async (req, res) => {
    const { messages } = req.body;
    console.log('[DEBUG] 请求头:', req.headers);
    console.log('[DEBUG] 请求体:', JSON.stringify(req.body, null, 2));
    try {
        const response = await fetch('https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer sk-66875e3305a646e0a72a05312024c9ce' // 替换真实 KEY
            },
            body: JSON.stringify({
                model: "qwen-max",
                input: {
                    messages: [
                        {
                            role: "system",
                            content: "你是一个中国文物知识专家，请用中文回答关于海外藏中国文物的问题"
                        },
                        ...messages
                    ]
                }
            })
        });

        const data = await response.json();
        console.log('[DEBUG] 原始响应:', JSON.stringify(data, null, 2));
        res.json({
            code: 200,
            data: {
              answer: data.output.text || '未获得有效回答',
              source: '通义千问'
            }
          });
    } catch (error) {
      // +++ 增强错误日志 +++
        console.error('[ERROR] 完整错误信息:', {
        message: error.message,
        stack: error.stack,
        request: {
          url: req.originalUrl,
          body: req.body
    }
  });
        res.status(500).json({ error: '模型服务异常' });
    }
});

// Mock 数据（模拟知识图谱数据）
const mockData = {
    '清明上河图': {
        作者: '张择端',
        收藏地: '故宫博物院',
        时代: '北宋'
    },
    '曾侯乙编钟': {
        时代: '战国',
        出土地点: '湖北随州'
    }
};

// 简单问答接口
app.get('/qa/simple', (req, res) => {
    const { entity, attribute } = req.query;

    // 检查请求参数是否缺失
    if (!entity || !attribute) {
        return res.status(400).json({
            error: '请求参数缺失，请提供 entity 和 attribute',
            status: 400
        });
    }

    const answer = mockData[entity]?.[attribute] || '未找到相关信息';

    res.json({
        answer: `${entity}的${attribute}是：${answer}`,
        source: '知识图谱数据库',
        status: 200
    });
});

// 错误处理中间件
app.use((err, req, res, next) => {
    console.error('发生错误:', err);
    res.status(500).json({
        error: '服务器内部错误',
        status: 500
    });
});

// 启动服务
const port = 3000;
app.listen(port, () => {
    console.log(`Mock 服务已启动：http://localhost:${port}`);
});