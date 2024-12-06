import './assets/style.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { VueReCaptcha } from 'vue-recaptcha-v3'
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';
import Carousel from 'primevue/carousel';
import Button from 'primevue/button';
import Fieldset  from 'primevue/fieldset';

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            prefix: 'p',
            darkModeSelector: false,
            cssLayer: false
        }
    }
 });
app.component('Carousel', Carousel)
app.component('Button', Button)
app.component('Fieldset', Fieldset)
app.use(VueReCaptcha, {siteKey: "6Ld-3YIqAAAAANCuGw89oroqKS8X56VosaVHbEBE"})
app.mount('#app')
