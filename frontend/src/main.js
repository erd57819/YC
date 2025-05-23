import { createApp } from 'vue';
import { createPinia } from 'pinia';

import App from './App.vue';
import router from './router';
import { useMapStore } from './stores/map'; 

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

const mapStore = useMapStore(); 

mapStore.loadKakaoMapSDK()
  .then(() => {
    console.log('Kakao Maps SDK successfully loaded and initialized via store in main.js.');
    app.mount('#app');
  })
  .catch(error => {
    console.error('Failed to initialize Kakao Maps SDK from store in main.js:', error);
    app.mount('#app');
  });