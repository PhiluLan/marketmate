// services/CalendarService.js
import api from '@/api/api'

export default {
  async fetchEvents() {
    return (await api.get('calendar-events/')).data
  },

  async addEvent(event) {
    return (await api.post('calendar-events/', event)).data
  }
}
