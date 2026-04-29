<script setup>
import Login from '../views/Login.vue';

</script>
<template>
    <header class="header">
        <h1>Nunaq</h1>
        <nav>
            <a href="/">Inicio</a>
            <a> 
                <router-link :to = "{name: 'Plan'}">Planes y precios</router-link>
            </a>
            <a> 
                <router-link :to = "{name: 'Login'}">Iniciar Sesión</router-link>
            </a>
        </nav>
    </header>
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