import axios from 'axios'

export const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
})

export const fetchTasks = async () => (await api.get('/tasks')).data
export const parseAssistant = async (message) => (await api.post('/assistant/parse', { message })).data
