<template>
  <div class="p-4">
    <h1 class="text-2xl mb-4">Meine ToDos</h1>

    <!-- Formular zum neuen ToDo -->
    <form @submit.prevent="addToDo" class="mb-6">
      <input
        v-model="newTitle"
        type="text"
        placeholder="Titel"
        class="border p-2 mr-2"
        required
      />
      <input
        v-model="newDesc"
        type="text"
        placeholder="Beschreibung (optional)"
        class="border p-2 mr-2"
      />
      <input
        v-model="newDueDate"
        type="datetime-local"
        class="border p-2 mr-2"
      />
      <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">
        Hinzufügen
      </button>
    </form>

    <!-- Liste der ToDos -->
    <div v-if="todos.length">
      <div
        v-for="todo in todos"
        :key="todo.id"
        class="flex items-center justify-between bg-gray-100 p-3 mb-2 rounded"
      >
        <div class="flex items-center">
          <input
            type="checkbox"
            :checked="todo.is_completed"
            @change="toggleComplete(todo)"
            class="mr-2"
          />
          <div>
            <div :class="todo.is_completed ? 'line-through text-gray-500' : ''">
              {{ todo.title }}
            </div>
            <div v-if="todo.description" class="text-sm text-gray-600">
              {{ todo.description }}
            </div>
            <div v-if="todo.due_date" class="text-xs text-red-600">
              Fällig am: {{ formatDate(todo.due_date) }}
            </div>
          </div>
        </div>
        <button @click="removeToDo(todo.id)" class="text-red-500">
          Löschen
        </button>
      </div>
    </div>
    <div v-else class="text-gray-500">Noch keine ToDos vorhanden.</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import TodoService from "@/services/TodoService.js";
import { initialize } from "@/services/AuthService.js";
import dayjs from "dayjs"; // für Datum-Formatierung

const todos = ref([]);
const newTitle = ref("");
const newDesc = ref("");
const newDueDate = ref("");

async function loadToDos() {
  // Nochmal initialisieren, falls der Token verloren ging
  initialize();

  console.log(
    "🚀 Axios Default Headers vor fetchToDos():",
    TodoService.api?.defaults?.headers?.common
  );

  try {
    todos.value = await TodoService.fetchToDos();
  } catch (e) {
    console.error("Fehler beim Laden der ToDos", e);
    if (e.response && e.response.status === 401) {
      alert("Dein Token ist abgelaufen oder ungültig. Bitte melde dich neu an.");
      // Optional: router.push('/login');
    }
  }
}

async function addToDo() {
  if (!newTitle.value) return;
  try {
    const payload = {
      title: newTitle.value,
      description: newDesc.value || "",
      due_date: newDueDate.value ? newDueDate.value : null,
    };
    await TodoService.createToDo(payload);
    newTitle.value = "";
    newDesc.value = "";
    newDueDate.value = "";
    await loadToDos();
  } catch (e) {
    alert("Fehler beim Erstellen des ToDos!");
    console.error(e);
  }
}

async function toggleComplete(todo) {
  try {
    await TodoService.updateToDo(todo.id, {
      is_completed: !todo.is_completed,
    });
    await loadToDos();
  } catch (e) {
    alert("Fehler beim Aktualisieren des ToDos!");
    console.error(e);
  }
}

async function removeToDo(id) {
  if (!confirm("Wirklich löschen?")) return;
  try {
    await TodoService.deleteToDo(id);
    await loadToDos();
  } catch (e) {
    alert("Fehler beim Löschen des ToDos!");
    console.error(e);
  }
}

function formatDate(dt) {
  return dayjs(dt).format("DD.MM.YYYY HH:mm");
}

onMounted(() => {
  loadToDos();
});
</script>

<style scoped>
/* optional: ein bisschen Tailwind-Klassen reichen meistens */
</style>
