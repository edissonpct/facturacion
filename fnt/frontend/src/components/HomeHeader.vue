<script setup>
import Login from '../views/Login.vue';
import { Toolbar, Button, Avatar } from 'primevue';


</script>
<template>
    <Toolbar style="border-radius: 3rem; padding: 1rem 1rem 1rem 1.5rem">
        <template #start>
            <div class="flex items-center gap-2">
                <img src="/src/assets/logo.png" alt="Logo" class="h-10 w-auto" />
                <router-link :to="{ name: 'Home' }">
                    <Button label="Inicio" text plain />
                </router-link>
                <router-link :to="{ name: 'Plan' }">
                    <Button label="Planes y precios" text plain />
                </router-link>
                <Button label="Acerca" text plain />
                
            </div>
        </template>

        <template #end>
            <div class="flex items-center gap-2">
                <router-link :to="{ name: 'Login' }">
                    <Button label="Iniciar sesión" severity="contrast" size="small" />
                </router-link>
                <Avatar image="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png" style="width: 32px; height: 32px" />
            </div>
        </template>
    </Toolbar>
</template>
<style scoped>
.header {
  background: #2c3e50;
  color: white;
  padding: 1rem;
}
nav a {
  margin-right: 10px;
  color: white;
  text-decoration: none;
}
</style>