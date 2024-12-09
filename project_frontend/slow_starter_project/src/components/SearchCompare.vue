<template>
  <v-dialog v-model="isOpen" max-width="1200px">
    <div class="overlay" @click="closeModal"></div>

    <v-card class="modal-content">
      <v-card-title class="d-flex justify-space-between align-center py-3 px-6">
        <span>금융상품 비교</span>
        <v-btn icon @click="closeModal">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text>
        <div v-for="product in searchStore.getSelectedProductsDetails" 
             :key="searchStore.getUniqueProductId(product)" 
             class="mb-6">
          <v-card outlined class="pa-4">
            <h3 class="mb-4">{{ product.kor_co_nm }} - {{ product.fin_prdt_nm }}</h3>
            
            <div class="mb-2">
              <strong>가입대상:</strong> {{ product.join_member }}
            </div>
            <div class="mb-2">
              <strong>가입방법:</strong> {{ product.join_way }}
            </div>
            <div class="mb-2">
              <strong>우대조건:</strong> {{ product.spcl_cnd }}
            </div>
            <div class="mb-4">
              <strong>유의사항:</strong> {{ product.etc_note }}
            </div>

            <!-- 금리 정보 테이블 -->
            <v-table>
              <thead>
                <tr>
                  <th></th>
                  <th v-for="term in [36, 24, 12, 6, 3, 1]" :key="term">
                    {{ term }}개월
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>저축 금리</strong></td>
                  <td v-for="term in [36, 24, 12, 6, 3, 1]" :key="term">
                    {{ getInterestRate(product, term, 'intr_rate') }}
                  </td>
                </tr>
                <tr>
                  <td><strong>최고 우대 금리</strong></td>
                  <td v-for="term in [36, 24, 12, 6, 3, 1]" :key="term">
                    {{ getInterestRate(product, term, 'intr_rate2') }}
                  </td>
                </tr>
              </tbody>
            </v-table>
          </v-card>
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref } from "vue";
import { useSearchStore } from "@/stores/search";

const searchStore = useSearchStore();
const isOpen = ref(false);

const getInterestRate = (product, term, rateType) => {
  const option = product.options.find(opt => opt.save_trm === term);
  return option ? `${option[rateType]}%` : '-';
};

const openModal = () => {
  isOpen.value = true;
};

const closeModal = () => {
  isOpen.value = false;
};

defineExpose({
  openModal,
  closeModal,
});
</script>
