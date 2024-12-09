<template>
     <div class="page-container">
    <div class="profile-container">
      <PasswordPage />
    </div>
  </div>
</template>

<script setup>

import PasswordPage from '@/components/PasswordPage.vue';

</script>

<style scoped>

.page-container {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 2rem;
  padding-top: 5rem;  /* Navbar와의 간격 추가 */
}

.profile-container {
  max-width: 1200px;
  margin: 0 auto;
}

</style>