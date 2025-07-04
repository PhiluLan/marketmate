// src/api/expressApi.js
import axios from 'axios'

const expressApi = axios.create({
  baseURL: 'http://127.0.0.1:5001/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

export default expressApi
