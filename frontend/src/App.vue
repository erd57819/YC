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
  background-color: #f5f6f7; /* Optional: Light background for the body */
}

</style>