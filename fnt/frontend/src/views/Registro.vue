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

const username = ref('')
const firstName = ref('')
const lastName = ref('')
const password = ref('')
const confirmPassword = ref('')
const acceptTerms = ref(false)

const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const handleRegister = async () => {
  errorMessage.value = ''
  successMessage.value = ''

  if (
    !username.value ||
    !firstName.value ||
    !lastName.value ||
    !password.value ||
    !confirmPassword.value
  ) {
    errorMessage.value = 'Completa todos los campos obligatorios.'
    return
  }

  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'Las contraseñas no coinciden.'
    return
  }

  if (!acceptTerms.value) {
    errorMessage.value = 'Debes aceptar los términos y condiciones.'
    return
  }

  try {
    loading.value = true

    // Aquí luego conectamos con Django / Djoser
    // Ejemplo:
    // await axios.post('/auth/users/', {
    //   email: username.value,
    //   first_name: firstName.value,
    //   last_name: lastName.value,
    //   password: password.value,
    //   re_password: confirmPassword.value
    // })

    console.log('Registro:', {
      username: username.value,
      firstName: firstName.value,
      lastName: lastName.value,
      password: password.value,
      confirmPassword: confirmPassword.value,
      acceptTerms: acceptTerms.value
    })

    successMessage.value = 'Usuario registrado correctamente.'

    setTimeout(() => {
      router.push({ name: 'Login' })
    }, 800)
  } catch (error) {
    errorMessage.value = 'No se pudo registrar el usuario.'
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
            Crea tu cuenta
          </h1>

          <p class="text-slate-300 text-lg">
            Regístrate para acceder al sistema y comenzar a gestionar tus empresas, usuarios y procesos administrativos.
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
              Registro de usuario
            </h2>
            <p class="text-slate-500 mt-2">
              Completa tus datos para crear una cuenta.
            </p>
          </div>

          <Message 
            v-if="errorMessage" 
            severity="error" 
            class="mb-5"
          >
            {{ errorMessage }}
          </Message>

          <Message 
            v-if="successMessage" 
            severity="success" 
            class="mb-5"
          >
            {{ successMessage }}
          </Message>

          <form class="flex flex-col gap-5" @submit.prevent="handleRegister">

            <div>
              <label for="username" class="block text-sm font-medium text-slate-700 mb-2">
                Usuario o correo electrónico
              </label>

              <InputText
                id="username"
                v-model="username"
                placeholder="usuario@correo.com"
                class="w-full"
              />
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
              <div>
                <label for="firstName" class="block text-sm font-medium text-slate-700 mb-2">
                  Nombres
                </label>

                <InputText
                  id="firstName"
                  v-model="firstName"
                  placeholder="Tus nombres"
                  class="w-full"
                />
              </div>

              <div>
                <label for="lastName" class="block text-sm font-medium text-slate-700 mb-2">
                  Apellidos
                </label>

                <InputText
                  id="lastName"
                  v-model="lastName"
                  placeholder="Tus apellidos"
                  class="w-full"
                />
              </div>
            </div>

            <div>
              <label for="password" class="block text-sm font-medium text-slate-700 mb-2">
                Contraseña
              </label>

              <Password
                id="password"
                v-model="password"
                placeholder="Ingresa una contraseña"
                toggleMask
                :feedback="false"
                class="w-full"
                inputClass="w-full"
              />
            </div>

            <div>
              <label for="confirmPassword" class="block text-sm font-medium text-slate-700 mb-2">
                Repetir contraseña
              </label>

              <Password
                id="confirmPassword"
                v-model="confirmPassword"
                placeholder="Repite la contraseña"
                toggleMask
                :feedback="false"
                class="w-full"
                inputClass="w-full"
              />
            </div>

            <div class="flex items-start gap-3">
              <Checkbox
                v-model="acceptTerms"
                inputId="acceptTerms"
                binary
                class="mt-1"
              />

              <label for="acceptTerms" class="text-sm text-slate-600 leading-6 cursor-pointer">
                Acepto los terminos y condiciones y la política de privacidad.
              </label>
            </div>

            <Button
              type="submit"
              label="Crear cuenta"
              icon="pi pi-user-plus"
              class="w-full mt-2"
              :loading="loading"
            />

            <div class="text-center text-sm text-slate-500">
              ¿Ya tienes una cuenta?
              <router-link
                :to="{ name: 'Login' }"
                class="font-medium text-primary hover:underline"
              >
                Iniciar sesión
              </router-link>
            </div>
          </form>
        </div>
      </div>

    </section>
  </main>
</template>