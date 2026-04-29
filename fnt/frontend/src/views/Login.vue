<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const username = ref('')
const password = ref('')
const errorMsg = ref('')

async function iniciarSesion(){
    console.log('BOTON LOGIN')
    if (!username.value.trim() || !password.value.trim()) {
        errorMsg.value = 'Completa todos los campos'
        return
    }
    console.log(username.value)
    console.log(password.value)
    try{
        const respuesta = await axios.post('http://127.0.0.1:8000/auth/jwt/create', {
            username: username.value,
            password: password.value
        },
        {
            withCredentials: true
        })
        console.log(respuesta.data)
        if (respuesta.status === 200) {
            router.push({ name: 'Dashboard' })
        }
    }
    catch(err){
        console.error('Error de login', err.response?.data || err)
        errorMsg.value = 'Usuario o contraseña incorrectos'
    }
    
} 
</script>

<template>
    <h1>LOGIN PAGE</h1>
    <form @submit.prevent="iniciarSesion" class="form">
        <label for="username">Usuario</label>
        <input type="text" id="username" v-model="username">

        <label for="password">Contraseña</label>
        <input type="text" id="password" v-model="password">
        <button>Iniciar sesión</button>
    </form>
    <p v-if="errorMsg" style="color: red">{{ errorMsg }}</p>
</template>

<style>
    .form {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
</style>