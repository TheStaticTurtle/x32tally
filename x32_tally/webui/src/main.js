import { createApp } from 'vue'
import App from './App.vue'
import Home from "@/pages/Home.vue";

import { createRouter, createWebHistory  } from 'vue-router'
const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: Home },
    ],
})

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import '@mdi/font/css/materialdesignicons.css' // Ensure you are using css-loader


const vuetify = createVuetify({
    components,
    directives,
    icons: {
        defaultSet: 'mdi', // This is already the default value - only for display purposes
    },
})

const app = createApp(App)

app.use(vuetify)
app.use(router)

app.mount('#app')