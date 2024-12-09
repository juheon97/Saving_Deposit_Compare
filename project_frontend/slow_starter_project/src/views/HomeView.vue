<!-- HomeView.vue -->
<template>
  <div class="split-background">
    <v-container class="fill-height">
      <v-row class="fill-height">
        <v-col cols="12" class="d-flex align-center justify-center">
          <HomeWidgetComponent class="custom-widget"/>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import HomeWidgetComponent from '@/components/HomeWidgetComponent.vue';
</script>

<style scoped>
.split-background {
  min-height: 100vh;
  background: #ffd8b8;
  display: flex;
  align-items: center;
}

.custom-widget {
  width: 90%;
  height: 65vh;
  max-width: 200vh;
}

@media (max-width: 960px) {
  .custom-widget {
    height: 80vh;
  }
}
</style>