import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import VueTextareaAutosize from 'vue-textarea-autosize';
import i18n from './i18n'
/*import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';
import 'firebase/compat/firestore';*/

Vue.use(VueTextareaAutosize);

Vue.config.productionTip = false

/*firebase.initializeApp({
  apiKey: "AIzaSyD3NfuHB1hrTGiGL-g36McHbXjDtJXLmR4",
  authDomain: "vue-calendar-d3bf4.firebaseapp.com",
  projectId: "vue-calendar-d3bf4",
  storageBucket: "vue-calendar-d3bf4.appspot.com",
  messagingSenderId: "441256886636",
  appId: "1:441256886636:web:f298b9343b3944b90c3349"
});*/

/*export const db = firebase.firestore();*/

new Vue({
  vuetify,
  i18n,
  render: h => h(App)
}).$mount('#app-calendar')
