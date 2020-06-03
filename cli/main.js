import Vue from 'vue'

import App from './App'
import router from './router.js'
import store from './store'

// window.Vue = Vue;

Vue.config.productionTip = false

const app = new Vue({
    el: '#app',
    router,
    store,
    template: "<App/>",
    components: { App }
})
