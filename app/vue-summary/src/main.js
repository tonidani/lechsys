import App from './App.vue'
import Vue from 'vue'
import Chartkick from 'vue-chartkick'
import Chart from 'chart.js'
import vuetify from './plugins/vuetify'
import VueApexCharts from 'vue-apexcharts'
import i18n from './i18n'



Vue.use(Chartkick.use(Chart));
Vue.use(VueApexCharts);

Vue.component('apexchart', VueApexCharts)

Vue.config.productionTip = false

new Vue({
  vuetify,
  i18n,
  render: h => h(App)
}).$mount('#app-userpage')
