<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Encabezado y otras secciones permanecen igual -->

    <!-- Sección de Contacto actualizada -->
    <section class="mb-8">
      <h2 class="text-xl font-semibold mb-4 flex items-center">Contacto</h2>
      <form @submit.prevent="submitForm" class="bg-white p-6 rounded-lg shadow-md">
        <div class="mb-4">
          <label for="nombre" class="block text-sm font-medium text-gray-700 mb-1"
            >Nombre *</label
          >
          <input
            v-model="form.nombre"
            type="text"
            id="nombre"
            name="nombre"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div class="mb-4">
          <label for="apellido" class="block text-sm font-medium text-gray-700 mb-1"
            >Apellido *</label
          >
          <input
            v-model="form.apellido"
            type="text"
            id="apellido"
            name="apellido"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div class="mb-4">
          <label for="email" class="block text-sm font-medium text-gray-700 mb-1"
            >Dirección de correo electrónico *</label
          >
          <input
            v-model="form.email"
            type="email"
            id="email"
            name="email"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <p v-if="!isValidEmail && form.email" class="text-red-500 text-sm mt-1">
            Por favor, introduce una dirección de correo electrónico válida.
          </p>
        </div>
        <div class="mb-4">
          <label for="message" class="block text-sm font-medium text-gray-700 mb-1"
            >Mensaje *</label
          >
          <textarea
            v-model="form.message"
            id="message"
            name="message"
            rows="4"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          ></textarea>
        </div>
        <div v-if="formError" class="mb-4 text-red-500">
          {{ formError }}
        </div>
        <button
          type="submit"
          class="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Enviar mensaje
        </button>
      </form>
    </section>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import { useReCaptcha } from 'vue-recaptcha-v3'

const { executeRecaptcha, recaptchaLoaded } = useReCaptcha()

const captcha = async () => {
  await recaptchaLoaded()
  const token = await executeRecaptcha('submit_form')
  return token
}

const form = ref({
  nombre: '',
  apellido: '',
  email: '',
  message: '',
})

const formError = ref('')

const isValidEmail = computed(() => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(form.value.email)
})

const submitForm = async () => {
  formError.value = ''

  if (!form.value.nombre || !form.value.email || !form.value.message || !form.value.apellido) {
    formError.value = 'Por favor, completa todos los campos obligatorios.'
    return
  }

  if (!isValidEmail.value) {
    formError.value = 'Por favor, introduce una dirección de correo electrónico válida.'
    return
  }
  try {
    var apiBaseUrl = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:5000/api'
    : 'https://admin-grupo20.proyecto2024.linti.unlp.edu.ar/api';
    const token = await await captcha()
    const response = await axios.post(`${apiBaseUrl}/contacto/register`, {
      nombre: form.value.nombre,
      apellido: form.value.apellido,
      email: form.value.email,
      mensaje: form.value.message,
      recaptcha_token: token,
    })
    console.log('Formulario enviado:', response.data)
    alert('Mensaje enviado con éxito. Gracias por contactarnos.')

    // Reiniciar el formulario
    form.value = {
      nombre: '',
      apellido: '',
      email: '',
      message: '',
    }
  } catch (error) {
    formError.value = 'Hubo un error al enviar el formulario. Inténtalo de nuevo más tarde.'
    console.error('Error al enviar el formulario:', error)
  }
}
</script>
