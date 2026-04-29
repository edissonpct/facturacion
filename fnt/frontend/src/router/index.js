import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/Login.vue";
import Home from "../views/Home.vue";
import Plan from "../views/Plan.vue";
import Dashboard from "../views/Dashboard.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/login", 
            name: "Login",
            component: Login
        },
        {
            path: "/", 
            name: "Home",
            component: Home
        },
        {
            path: "/plan", 
            name: "Plan",
            component: Plan
        },
        {
            path: "/dashboard", 
            name: "Dashboard",
            component: Dashboard
        }
    
    ]
})

export default router;