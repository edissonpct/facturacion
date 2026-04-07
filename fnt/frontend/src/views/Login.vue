<script setup>

const handleSubmit = () => {} 
</script>

<template>
    <h1>LOGIN PAGE</h1>
    <form @submit.prevent="handleSubmit" class="form">
        <label for="username">Usuario</label>
        <input type="text" id="username">

        <label for="password">Contraseña</label>
        <input type="text" id="password">
        <button>Iniciar sesión</button>
    </form>
</template>

<style>
    .form {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
</style>