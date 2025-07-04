<template>
  <div class="p-4">
    <h1 class="text-xl mb-4">Content-Kalender</h1>

    <form @submit.prevent="createPost" class="mb-6 space-y-2">
      <select v-model="form.channel" class="border p-2 rounded w-full">
        <option value="facebook">Facebook (organisch)</option>
        <option value="instagram">Instagram (organisch)</option>
        <option value="facebook_ads">Facebook Ads</option>
        <option value="email">E-Mail</option>
      </select>

       <select v-model="form.content_id" class="border p-2 rounded w-full" required>
       <option disabled value="">-- bitte Inhalt wählen --</option>
        <option 
          v-for="c in contents" 
          :key="c.id" 
          :value="c.id"
        >
          {{ c.title }}
        </option>
      </select>
      <p v-if="contents.length===0" class="text-red-500">
        Keine Inhalte vorhanden. Bitte erst Content anlegen!
      </p>

      <input 
        type="datetime-local" 
        v-model="form.scheduled_time" 
        class="border p-2 rounded w-full"
      />

      <button 
        type="submit" 
        class="bg-blue-500 text-white py-2 px-4 rounded"
      >
        Planen
      </button>
    </form>

    <ul class="space-y-2">
      <li 
        v-for="p in scheduled" 
        :key="p.id" 
        class="border p-2 rounded flex justify-between"
      >
        <span>{{ p.channel }} – {{ p.content.title }}</span>
        <span>{{ p.scheduled_time | formatDate }}</span>
        <span :class="statusClass(p.status)">{{ p.status }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
import { fetchContents, fetchScheduledPosts, createScheduledPost } from '@/services/schedulerService'
import api from '@/api/api'

export default {
  name: 'SchedulerView',
  data() {
    return {
      contents: [],
      scheduled: [],
      form: {
        channel: 'facebook',
        content_id: null,
        scheduled_time: ''
      }
    }
  },
  async created() {
    this.contents = (await fetchContents()).data
    this.fetchScheduled()
  },
  methods: {
    async fetchScheduled() {
      this.scheduled = (await fetchScheduledPosts()).data
    },
    async createPost() {
      if (!this.form.content_id) {
        return alert('Bitte zuerst einen Inhalt auswählen!')
      }
      try {
        // siehe nächsten Schritt: wir wandeln hier gleich in ISO um
        const dt = new Date(this.form.scheduled_time)
        await createScheduledPost({
          channel: this.form.channel,
          content: this.form.content_id,
          scheduled_time: dt.toISOString(),   // voller ISO-String
        })
        this.form.scheduled_time = ''
        this.fetchScheduled()
      } catch (error) {
        console.error('API-Fehler:', error.response.data)
        alert(`Fehler beim Anlegen: ${JSON.stringify(error.response.data)}`)
      }
    },
    
    statusClass(status) {
      return {
        pending: 'text-yellow-600',
        sent:    'text-green-600',
        failed:  'text-red-600'
      }[status] || ''
    }
  },
  filters: {
    formatDate(value) {
      return new Date(value).toLocaleString('de-CH')
    }
  }
}
</script>
