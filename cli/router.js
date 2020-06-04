import Vue from 'vue'
import VueRouter from 'vue-router'

import Index from './pages/index.vue'
import NotFound from './pages/NotFound.vue'

Vue.use(VueRouter)

export default new VueRouter({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'Index',
            component: Index
        },
        {
            path: '*',
            component: NotFound
        }
    ]
})
