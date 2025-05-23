<template>
  <div>
    <NavBar /> 

    <div class="container mt-4">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router';
import NavBar from '@/components/Nav.vue'; 
</script>

<style>

body {
  background-color: #dde1e6; /* Optional: Light background for the body */
}

</style>