<template>
  <body class="bg-white h-screen relative">
    <!-- Botón "Volver" -->
    <RouterLink to="/" class="absolute top-4 left-4 text-blue-600 hover:underline">
      <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24">
        <g fill="none">
          <path d="M24 0v24H0V0zM12.593 23.258l-.011.002l-.071.035l-.02.004l-.014-.004l-.071-.035q-.016-.005-.024.005l-.004.01l-.017.428l.005.02l.01.013l.104.074l.015.004l.012-.004l.104-.074l.012-.016l.004-.017l-.017-.427q-.004-.016-.017-.018m.265-.113l-.013.002l-.185.093l-.01.01l-.003.011l.018.43l.005.012l.008.007l.201.093q.019.005.029-.008l.004-.014l-.034-.614q-.005-.019-.02-.022m-.715.002a.02.02 0 0 0-.027.006l-.006.014l-.034.614q.001.018.017.024l.015-.002l.201-.093l.01-.008l.004-.011l.017-.43l-.003-.012l-.01-.01z" />
          <path fill="black" d="M3.283 10.94a1.5 1.5 0 0 0 0 2.12l5.656 5.658a1.5 1.5 0 1 0 2.122-2.122L7.965 13.5H19.5a1.5 1.5 0 0 0 0-3H7.965l3.096-3.096a1.5 1.5 0 1 0-2.122-2.121z" />
        </g>
      </svg>
    </RouterLink>

    <!-- Contenido centrado -->
    <div class="flex justify-center items-center h-full">
      <div
        v-if="noticia"
        class="flex flex-col justify-center items-center p-6 rounded-lg shadow-md bg-white w-auto relative"
        style="border: 4px solid transparent; background-image: linear-gradient(white, white), linear-gradient(to right, cyan, yellow); background-origin: border-box; background-clip: padding-box, border-box;"
      >
        <h1 class="text-3xl font-bold mb-4">{{ noticia.titulo }}</h1>
        <p class="text-2xl font-semibold mb-4">Copete: {{ noticia.copete }}</p>
        <p class="text-base mb-2">Contenido: {{ noticia.contenido }}</p>
        <p class="text-base mb-2">Autor: {{ noticia.autor_nombre }}</p>
        <div class="flex flex-row justify-center items-center space-x-4">
          <p class="text-gray-600">Publicado: {{ formatDate(noticia.fecha_publicacion) }}</p>
          <p class="text-gray-600">Creado: {{ formatDate(noticia.fecha_creacion) }}</p>
          <p class="text-gray-600">Actualizado: {{ formatDate(noticia.fecha_actualizacion) }}</p>
        </div>
      </div>
      <div v-else>
        <p class="text-red-600">Error en procesar la noticia.</p>
      </div>
    </div>
  </body>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useActividadYNoticiasStore } from '../stores/actividadYnoticias.js';

const route = useRoute();
const store = useActividadYNoticiasStore();
const noticia = ref(null);

onMounted(async () => {
  const id = parseInt(route.params.id);
  const fetchedNoticia = await store.fetchNoticiaById(id);
  if (fetchedNoticia) {
    noticia.value = fetchedNoticia;
  }
});

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
}

.back-link {
  position: absolute;
  top: 20px;
  left: 20px;
  color: #007bff;
  text-decoration: none;
}

.back-link:hover {
  text-decoration: underline;
}

.content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title {
  text-align: center;
  margin-bottom: 20px;
  font-size: 2em;
  color: #333;
}

.subtitle {
  font-size: 1.5em;
  font-weight: bold;
  margin-bottom: 10px;
}

.text {
  font-size: 1.2em;
  margin-bottom: 10px;
}

.dates {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.date {
  font-size: 1em;
  color: #555;
}

.text-red-600 {
  color: #e3342f;
}
</style>