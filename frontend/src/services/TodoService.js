import api from "@/api/api.js"; // dein generischer Axios-Client mit BaseURL und Credentials

export default {
  async fetchToDos() {
    const res = await api.get("/todos/");
    return res.data; // Array von ToDo-Objekten
  },
  async createToDo(data) {
    // data: { title, description, due_date? }
    const res = await api.post("/todos/", data);
    return res.data;
  },
  async updateToDo(id, data) {
    const res = await api.patch(`/todos/${id}/`, data);
    return res.data;
  },
  async deleteToDo(id) {
    await api.delete(`/todos/${id}/`);
    return;
  },
};
