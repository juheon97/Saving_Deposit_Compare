<template>
  <div class="grid-container">
    <ExchangeCard v-for="item in cardGroup" :key="item.id" :exchange-data="item"/>
  </div>
</template>

<script setup>
import ExchangeCard from "./ExchangeCard.vue";

const props = defineProps({
  cardGroup: {
    type: Array,
    required: true,
  },
});
</script>

<style scoped>
.grid-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 28px; /* gap 증가 */
  padding: 28px; /* padding 증가 */
  width: 95%; /* 너비 증가 */
  margin: 0 auto;
  height: 100%;
  max-width: 1800px; /* 최대 너비 증가 */
}

@media (max-width: 960px) {
  .grid-container {
    grid-template-columns: 1fr;
    grid-template-rows: auto;
  }
}
</style>
