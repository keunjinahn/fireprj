import "@babel/polyfill"
import Vue from 'vue'
import moment from 'moment'
import VueMoment from 'vue-moment'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import utils from './plugins/utils';
import http from './plugins/http';
import router from './router'
import Highcharts from 'highcharts'
import HighchartsVue from 'highcharts-vue'
import CountUp from 'vue-countup-v2'

//import Control from '@/plugins/tra-client'
import Session from '@/plugins/session'
import MainLayout from '@/components/MainLayout'
import 'moment/locale/ko'
import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';
import AblDocument from "@/components/AblDocument";
Vue.config.productionTip = false

Highcharts.setOptions({
  lang: {
    thousandsSep: ','
  }
})

Vue.component('main-layout', MainLayout)
Vue.component('count-up', CountUp)
Vue.use(VueMoment, { moment })
Vue.use(utils)
Vue.use(http)
Vue.use(Session)
Vue.use(HighchartsVue)
Vue.use(VueSweetalert2)
Vue.use(AblDocument)
//Vue.prototype.$control = Control
Vue.prototype.$session = Session
Vue.filter("makeComma", val =>{
  return String(val).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
})
new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')
