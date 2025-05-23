import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import { useMapStore } from './stores/map';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

useMapStore(); 
app.mount('#app');