<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Encabezado -->
    <header class="bg-[#6eb4d3] text-white p-4">
      <h1 class="text-2xl font-bold">{{ institucion.nombre }}</h1>
    </header>

    <!-- Contenido principal -->
    <main class="container mx-auto px-4 py-8 text-black">
      <div>
        <Carousel />
      </div>
      <!-- Información básica -->
      <section class="mb-8">
        <h1 class="text-xl font-semibold mb-4 flex items-center">Información Básica</h1>
        <p>{{ institucion.descripcion }}</p>
      </section>

      <!-- Tareas -->
      <section class="mb-8">
        <h1 class="text-xl font-semibold mb-4 flex items-center">Tareas que Desarrollamos</h1>
        <ul class="list-disc pl-5">
          <li v-for="(tarea, index) in institucion.tareas" :key="index">
            {{ tarea }}
          </li>
        </ul>
      </section>
      <!-- Noticias -->
      <section class="mb-8">
        <h2 class="text-xl font-semibold mb-4 flex items-center">Noticias</h2>
        <ActividadesNoticiasList />
      </section>
      <!-- Contacto -->
      <section class="mb-8">
        <ContactForm></ContactForm>
      </section>
      
    </main>

    <!-- Pie de página -->
    <footer class="bg-gray-800 text-white p-4 mt-8">
      <p class="text-center">
        &copy; {{ new Date().getFullYear() }} {{ institucion.nombre }}. Todos los derechos
        reservados.
      </p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ContactForm from '../components/ContactForm.vue'
import Carousel from './TheCarousel.vue'
import ActividadesNoticiasList from './ActividadesNoticiasList.vue'

const institucion = ref({
  nombre: 'Cedica',
  descripcion:
    'Somos una institución dedicada a mejorar la calidad de vida de nuestra comunidad a través de diversos programas y servicios.',
  tareas: [
    '🐴♿Clases de Tacas/Equinoterapia',
    '🖥️ Cursos on line y presenciales',
    '🕹️ Desarrollo de tecnología adaptada',
    ' La Plata, Buenos Aires, Argentina',
  ],
  contacto: {
    email: 'contacto@institucion.ejemplo',
    telefono: '+1 234 567 8900',
    direccion: 'Calle Principal 123, Ciudad Ejemplo, País',
  },
})
</script>
