import axios from 'axios'

const apiClient = axios.create({
  baseURL: '/api',
  timeout: 60000
})

export default {
  askSimpleQuestion(params) {
    return apiClient.get('/qa/simple', { 
      params: {
        entity: params.entity,
        attribute: params.attribute
      }
    })
  },
  
  askLLMQuestion(data) {
    return apiClient.post('http://localhost:8000/llm/chat/api/', data)
  }
}