import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";
import '@mdi/font/css/materialdesignicons.css' ;
import vuetify from './plugins/vuetify';
import axios from 'axios'
axios.defaults.withCredentials = true
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.withCredentials = true
const app = createApp(App);
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)
app.use(router);
app.use(vuetify);
app.mount("#app");

