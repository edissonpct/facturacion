<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

// Assets
import logo from '../assets/logo.png'

// PrimeVue
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Checkbox from 'primevue/checkbox'
import Button from 'primevue/button'
import Message from 'primevue/message'

const router = useRouter()

const email = ref('')
const password = ref('')
const remember = ref(false)
const loading = ref(false)
const errorMessage = ref('')

const handleLogin = async () => {
  errorMessage.value = ''

  if (!email.value || !password.value) {
    errorMessage.value = 'Ingresa tu usuario y contraseña.'
    return
  }

  try {
    loading.value = true

    // Aquí luego conectamos con Django JWT
    // const response = await axios.post('/auth/jwt/create/', {
    //   email: email.value,
    //   password: password.value
    // })

    console.log('Login:', {
      email: email.value,
      password: password.value,
      remember: remember.value
    })

    // Redirección temporal
    router.push({ name: 'Home' })
  } catch (error) {
    errorMessage.value = 'Credenciales incorrectas.'
    console.error(error)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="min-h-screen bg-slate-100 flex items-center justify-center p-4">
    <section class="w-full max-w-6xl bg-white rounded-3xl shadow-xl overflow-hidden grid grid-cols-1 lg:grid-cols-2">

      <!-- Panel izquierdo -->
      <div class="hidden lg:flex flex-col justify-between bg-slate-900 text-white p-10">
        <div>
          <img :src="logo" alt="Logo" class="h-12 w-auto mb-10" />

          <h1 class="text-4xl font-bold leading-tight mb-4">
            Bienvenido a tu sistema de facturación
          </h1>

          <p class="text-slate-300 text-lg">
            Gestiona empresas, usuarios, facturación y procesos administrativos desde una sola plataforma.
          </p>
        </div>

        <p class="text-sm text-slate-400">
          © 2026 FacturaERP. Todos los derechos reservados.
        </p>
      </div>

      <!-- Formulario -->
      <div class="p-6 sm:p-10 lg:p-14 flex items-center">
        <div class="w-full max-w-md mx-auto">
          
          <!-- Logo móvil -->
          <div class="lg:hidden flex justify-center mb-8">
            <img :src="logo" alt="Logo" class="h-14 w-auto" />
          </div>

          <div class="mb-8 text-center lg:text-left">
            <h2 class="text-3xl font-bold text-slate-900">
              Iniciar sesión
            </h2>
          </div>

          <Message 
            v-if="errorMessage" 
            severity="error" 
            class="mb-5"
          >
            {{ errorMessage }}
          </Message>

          <form class="flex flex-col gap-5" @submit.prevent="handleLogin">
            <div>
              <label for="email" class="block text-sm font-medium text-slate-700 mb-2">
                Usuario o correo electrónico
              </label>

              <InputText
                id="email"
                v-model="email"
                type="email"
                placeholder="usuario@correo.com"
                class="w-full"
              />
            </div>

            <div>
              <label for="password" class="block text-sm font-medium text-slate-700 mb-2">
                Contraseña
              </label>

              <Password
                id="password"
                v-model="password"
                placeholder="Ingresa tu contraseña"
                toggleMask
                :feedback="false"
                class="w-full"
                inputClass="w-full"
              />
            </div>

            <div class="flex items-center justify-between gap-4">
              <div class="flex items-center gap-2">
                <Checkbox 
                  v-model="remember" 
                  inputId="remember" 
                  binary 
                />
                <label for="remember" class="text-sm text-slate-600 cursor-pointer">
                  Recordarme
                </label>
              </div>

              <router-link
                :to="{ name: 'Home' }"
                class="text-sm text-primary hover:underline"
              >
                ¿Olvidaste tu contraseña?
              </router-link>
            </div>

            <Button
              type="submit"
              label="Ingresar"
              icon="pi pi-sign-in"
              class="w-full mt-2"
              :loading="loading"
            />

            <div class="text-center text-sm text-slate-500">
              ¿No tienes una cuenta?
               <router-link
                :to="{ name: 'Registro' }"
                class="font-medium text-primary hover:underline"
                >
                Crear una cuenta
               </router-link>
            </div>
          </form>
        </div>
      </div>

    </section>
  </main>
</template>