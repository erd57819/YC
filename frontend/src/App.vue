<template>
  <div>
    <NavBar /> 

    <div class="container mt-4">
      <RouterView />
    </div>
    <ChatbotButton />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router';
import NavBar from '@/components/Nav.vue'; 
import ChatbotButton from '@/components/ChatbotButton.vue';
</script>

<style>

body {
  background-color: #f8f8f8; 
}

</style>