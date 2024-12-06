<template>
  <div>
    <input v-model="searchAuthor" @input="validateAuthor" placeholder="Buscar por autor" />
    Fecha inicio
    <input type="date" v-model="startDate" @input="validateDates" placeholder="Fecha de inicio" />
    Fecha fin
    <input type="date" v-model="endDate" @input="validateDates" placeholder="Fecha de fin" />
    <p v-if="loading">Cargando...</p>
    <p v-if="error">{{ error }}</p>
    <div class="card">
      <Fieldset v-for="item in actividadYnoticias" :key="item.id">
        <template #legend>
          <div class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24">
              <path
                fill="black"
                d="M12 4a4 4 0 0 1 4 4a4 4 0 0 1-4 4a4 4 0 0 1-4-4a4 4 0 0 1 4-4m0 10c4.42 0 8 1.79 8 4v2H4v-2c0-2.21 3.58-4 8-4"
              />
            </svg>
            <span class="font-bold p-2">{{ item.autor_nombre }}</span>
          </div>
        </template>
        <h1 class="mb-2 font-bold">{{ item.titulo }}</h1>
        <p class="m-2">{{ item.copete }}</p>
        <div class="flex justify-between items-center">
          <RouterLink
            :to="{ name: 'noticiaDetalle', params: { id: item.id } }"
            class="flex flex-row items-center justify-center mt-3 text-blue-500 hover:text-blue-700 transition duration-200 ease-in-out"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24">
              <path
                fill="blue"
                d="M12 9a3 3 0 0 1 3 3a3 3 0 0 1-3 3a3 3 0 0 1-3-3a3 3 0 0 1 3-3m0-4.5c5 0 9.27 3.11 11 7.5c-1.73 4.39-6 7.5-11 7.5S2.73 16.39 1 12c1.73-4.39 6-7.5 11-7.5M3.18 12a9.821 9.821 0 0 0 17.64 0a9.821 9.821 0 0 0-17.64 0"
              />
            </svg>
            Ver más
          </RouterLink>
          <p class="mt-2 text-gray-600 text-sm">{{ formatDate(item.fecha_publicacion) }}</p>
        </div>
      </Fieldset>
    </div>
  </div>
  <p v-if="!loading && !actividadYnoticias.length">No hay actividades y noticias para mostrar</p>
  <div v-if="totalPages > 1" class="pagination">
    <button @click="prevPage" :disabled="currentPage === 1">Anterior</button>

    <span>Página {{ currentPage }} de {{ totalPages }}</span>

    <button @click="nextPage" :disabled="currentPage === totalPages">Siguiente</button>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useActividadYNoticiasStore } from '../stores/actividadYnoticias.js'
import { storeToRefs } from 'pinia'

const store = useActividadYNoticiasStore()
const { loading, error, actividadYnoticias, totalPages } = storeToRefs(store)

var searchAuthor = ref('')
var startDate = ref('')
var endDate = ref('')
const today = new Date().toISOString().split('T')[0] // Fecha de hoy en formato YYYY-MM-DD

var currentPage = ref(1)
var itemsPerPage = ref(2)

const validateAuthor = () => {
  if (searchAuthor.value.length > 20) {
    searchAuthor.value = searchAuthor.value.slice(0, 20)
  }
  searchAuthor.value = searchAuthor.value.replace(/[^a-zA-Z0-9 ]/g, '')
}

const validateDates = () => {
  if (startDate.value && endDate.value) {
    if (new Date(startDate.value) > new Date(endDate.value)) {
      alert('La fecha de inicio no puede ser superior a la fecha de fin.')
      startDate.value = ''
      endDate.value = ''
    }
  }
  if (startDate.value && new Date(startDate.value) > new Date(today)) {
    alert('La fecha de inicio no puede ser una fecha futura.')
    startDate.value = ''
  }
  if (endDate.value && new Date(endDate.value) > new Date(today)) {
    alert('La fecha de fin no puede ser una fecha futura.')
    endDate.value = ''
  }
}

const fetchActividadYNoticias = async () => {
  const params = {
    author: searchAuthor.value,
    published_from: startDate.value,
    published_to: endDate.value,
    page: currentPage.value,
    per_page: itemsPerPage.value,
  }
  await store.fetchActividadYnoticias(params)
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    fetchActividadYNoticias()
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    fetchActividadYNoticias()
  }
}

onMounted(() => {
  fetchActividadYNoticias()
})

watch([searchAuthor, startDate, endDate, itemsPerPage], fetchActividadYNoticias)

const formatDate = (dateString) => {
  const options = { year: 'numeric', day: '2-digit', month: '2-digit',  }
  return new Date(dateString).toLocaleDateString('es-ES', options)
}
</script>

<style scoped>
h2 {
  text-align: center;
  margin-bottom: 20px;
}

.card {
  background-color: white;
  width: 100%;
  padding: 10px;
}
.input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.date-inputs {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

@media (min-width: 600px) {
  .date-inputs {
    flex-direction: row;
  }
}

.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.button {
  padding: 10px 20px;
  margin: 0 5px;
  border: none;
  border-radius: 4px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
}

.button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.button:not(:disabled):hover {
  background-color: #0056b3;
}
</style>
