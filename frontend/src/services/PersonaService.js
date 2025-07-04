import expressApi from '@/api/expressApi.js'

const API_URL = 'https://your-backend-api.com/api/personas' // später dynamisch setzen

export default {
  async getPersonas() {
    const res = await expressApi.get(API_URL)
    return res.data
  },

  async createPersona(persona) {
    const res = await expressApi.post(API_URL, persona)
    return res.data
  }
}
