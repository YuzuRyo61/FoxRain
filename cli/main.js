import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'

import App from './App'
import router from './router.js'
import store from './store'

// window.Vue = Vue;

Vue.config.productionTip = false

Vue.use(VueAxios, axios)

/* eslint-disable no-unused-vars */
const app = new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App)
})
