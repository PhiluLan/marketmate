<template>
  <div class="flex flex-col h-full max-w-2xl mx-auto p-4">
    <!-- Chat-Log -->
    <div class="flex-1 overflow-auto mb-4">
      <div
        v-for="(m, i) in messages"
        :key="i"
        :class="m.sender === 'user' ? 'text-right' : 'text-left'"
        class="my-2"
      >
        <div
          :class="[
            'inline-block rounded-lg px-3 py-2 whitespace-pre-wrap',
            m.sender === 'user'
              ? 'bg-blue-500 text-white text-left'
              : 'bg-gray-200 text-gray-900 text-left'
          ]"
          v-html="renderMessage(m.text)"
        />
      </div>
    </div>

    <!-- Eingabe- & Send-Button -->
    <div class="flex items-center space-x-2">
      <input
        v-model="draft"
        @keyup.enter="send"
        class="flex-1 border rounded px-3 py-2"
        placeholder="Schreibe hier…"
        :disabled="awaiting"
      />
      <button
        class="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
        @click="send"
        :disabled="awaiting || !draft"
      >
        Send
      </button>
    </div>

    <!-- OK-Button für Kampagnenfreigabe -->
    <div v-if="readyForSubmit" class="mt-4 text-center">
      <button
        class="bg-green-600 text-white px-6 py-2 rounded"
        @click="confirm"
      >
        Ja, erstelle die Kampagne
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import ChatService from '@/services/ChatService.js'

const messages       = ref([])  // { sender: 'user'|'bot', text: string }
const draft          = ref('')
const awaiting       = ref(false)
const readyForSubmit = ref(false)

/**
 * Rendert einen Chat-Text:
 * - JSON-Objekte in String umwandeln
 * - Markdown → HTML via marked
 * - HTML säubern via DOMPurify
 */
function renderMessage(raw) {
  let text = typeof raw === 'string'
    ? raw
    : JSON.stringify(raw, null, 2)

  // Marked benötigt einen String
  const unsafeHtml = marked.parse(text)
  return DOMPurify.sanitize(unsafeHtml)
}

async function send() {
  if (!draft.value) return

  // 1) Benutzer-Nachricht anzeigen
  messages.value.push({ sender: 'user', text: draft.value })
  const text = draft.value
  draft.value = ''
  awaiting.value = true

  try {
    // 2) Antwort von ChatService (liefert reinen String)
    const botText = await ChatService.sendMessage(text)

    // 3) Bot-Nachricht anzeigen
    messages.value.push({ sender: 'bot', text: botText })

    // 4) Falls Lenny um Freigabe bittet, OK-Button anzeigen
    if (
      botText.includes('mit deinem okay') ||
      botText.includes('erstelle die Kampagne')
    ) {
      readyForSubmit.value = true
    }
  } catch (err) {
    messages.value.push({ sender: 'bot', text: '⚠️ Fehler: ' + err })
  } finally {
    awaiting.value = false
  }
}

async function confirm() {
  // User bestätigt: sende "OK" nochmal
  readyForSubmit.value = false
  draft.value = 'OK'
  await send()
}
</script>

<style scoped>
/* Damit Zeilenumbrüche erhalten bleiben */
.whitespace-pre-wrap {
  white-space: pre-wrap;
}

/* Optische Scrollbar */
.flex-1::-webkit-scrollbar {
  width: 6px;
}
.flex-1::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}
</style>
