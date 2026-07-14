<script setup>
import HomeHeader from '../components/HomeHeader.vue'
import HomeFooter from '../components/HomeFooter.vue'
import Button from 'primevue/button'
</script>

<template>
  <div class="layout">
    <HomeHeader />
    <div class="flex justify-center items-center h-screen">
      <Button label="Guardar" icon="pi pi-check" />
    </div>
    <main class="content">
      <h2>Bienvenido al Home</h2>
      <p>Este es el contenido principal</p>
    </main>

    <HomeFooter />
  </div>
</template>



<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content {
  flex: 1;
  padding: 20px;
}
</style>