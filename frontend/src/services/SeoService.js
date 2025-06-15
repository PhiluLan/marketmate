// src/services/SeoService.js
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api/seo',
  headers: { 'Content-Type': 'application/json' }
})

export async function getRecommendation(website_name, website_topic) {
  const res = await api.post('/recommendations/', {
    website_name,
    website_topic
  })
  return res.data  // z.B. { "meta_description": "..."}
}
