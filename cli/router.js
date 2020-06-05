import Vue from 'vue'
import VueRouter from 'vue-router'

import Index from './pages/index.vue'
import NotFound from './pages/NotFound.vue'
import User from './pages/User.vue'

Vue.use(VueRouter)

export default new VueRouter({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'index',
            component: Index
        },
        {
            path: '/@:username',
            name: 'user',
            component: User
        },
        {
            path: '*',
            component: NotFound
        }
    ]
})
