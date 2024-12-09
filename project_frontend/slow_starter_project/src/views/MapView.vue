<template>
  <div class="split-background">
    <v-container class="map-size">
      <v-card class="widget-wrapper" elevation="0">
        <v-row>
          <v-col cols="4">
            <v-select class="custom-select" v-model="province" :items="provinces" label="도/시" @change="updateCities"></v-select>
          </v-col>
          <v-col cols="4">
            <v-select class="custom-select" v-model="city" :items="cities" label="시/군/구"></v-select>
          </v-col>
          <v-col cols="4">
            <v-select class="custom-select" v-model="bank" :items="mapStore.banks" label="은행"></v-select>
          </v-col>
        </v-row>
        <MapSearchComponent 
          :province="province" 
          :city="city" 
          :bank="bank" 
          @update-selected-place="updateSelectedPlace"
        />
      </v-card>
    </v-container>
  </div>
 </template>
 
 <script setup>
 import { ref, watch, computed } from "vue";
 import MapSearchComponent from "@/components/MapSearchComponent.vue";
 import { useMapStore } from "@/stores/map";
 
 const mapStore = useMapStore();
 const cities = ref([]);
 const provinces = computed(() => mapStore.infos.map((info) => info.prov));
 
 const province = ref("선택해주세요");
 const city = ref("선택해주세요");
 const bank = ref("선택해주세요");

const updateCities = () => {
  const selectedInfo = mapStore.infos.find((info) => info.prov === province.value);
  cities.value = selectedInfo ? selectedInfo.city : [];
};

const updateSelectedPlace = (place) => {
  console.log('Selected place:', place);
};

watch(province, updateCities);
</script>

<style scoped>
.split-background {
  min-height: 100vh;
  background: #ffd8b8;
  padding: 20px;
}

.widget-wrapper {
  background: #fff0e5 100%;
  border-radius: 16px;
  padding: 30px;
  margin: 0 auto;
  width: 90%;
  max-width: 2000px;
}

.custom-select {
  background-color: white;
  color: #142A2A;
  font-weight: bold;
  box-shadow: 2px 2px 1px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.map-size {
  width: 95%;
  max-width: 2000px;
}

</style>
