// frontend/src/services/ChatService.js
import api from '@/api/api.js'

export default {
  /**
   * Senden einer einzelnen Chat-Nachricht.
   * Antwort: { response: string, ... }
   */
  async sendMessage(message) {
    const res = await api.post("/chat/", { message });
    // Hier holen wir uns nur noch den String under data.response
    // egal ob das vorher ein String oder ein Objekt war.
    const payload = res.data.response;
    // Wenn’s schon ein String ist, zurück damit
    if (typeof payload === "string") {
      return payload;
    }
    // Falls Payload doch ein Objekt ist (ältere Fälle),
    // versuchen wir, daraus den Content rauszuziehen:
    if (payload?.content && typeof payload.content === "string") {
      return payload.content;
    }
    // Falls es Choices aus der OpenAI API sind:
    if (payload?.choices?.length) {
      const choice = payload.choices[0].message?.content;
      if (choice) return choice;
    }
    // Fallback: stringify (sollte aber nie passieren)
    return JSON.stringify(payload);
  },

  /**
   * Streaming-Endpoint (falls du das brauchst)
   */
  sendStream(message) {
    return api.post('/chat/stream/', { message })
  }
}
