import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import SuiVue from 'semantic-ui-vue'

import App from './App'
import router from './router.js'
import store from './store'

import 'semantic-ui-css/semantic.min.css'

// window.Vue = Vue;

Vue.config.productionTip = false

Vue.use(VueAxios, axios)

Vue.use(SuiVue)

/* eslint-disable no-unused-vars */
const app = new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App)
})
