<template>
  <v-card elevation="2">
    <v-card-title class="text-h5 pa-4">
      내가 담은 상품
    </v-card-title>
    <v-card-text>
      <v-row>
        <!-- 예금 상품 테이블 -->
        <v-col cols="12" md="6">
          <v-card variant="outlined">
            <v-card-title class="text-h6 bg-light-blue-lighten-5 py-3" style="radius:30">
              예금 상품
            </v-card-title>
            <v-expansion-panels>
              <v-expansion-panel
                v-for="product in depositProducts"
                :key="product.id"
              >
                <v-expansion-panel-title>
                  <v-row no-gutters>
                    <v-col cols="5">{{ product.kor_co_nm }}</v-col>
                    <v-col cols="7" class="text-truncate">
                      {{ product.fin_prdt_nm }}
                    </v-col>
                  </v-row>
                </v-expansion-panel-title>
                <v-expansion-panel-text>
                  <v-card-text>
                    <v-row>
                      <v-col cols="12">
                        <div class="text-subtitle-1 font-weight-bold mb-2">상품 정보</div>
                        <v-list>
                          <v-list-item>
                            <template v-slot:prepend>
                              <v-icon color="primary">mdi-account-group</v-icon>
                            </template>
                            <v-list-item-title>가입대상</v-list-item-title>
                            <v-list-item-subtitle>{{ product.join_member }}</v-list-item-subtitle>
                          </v-list-item>
                          <v-list-item>
                            <template v-slot:prepend>
                              <v-icon color="primary">mdi-login</v-icon>
                            </template>
                            <v-list-item-title>가입방법</v-list-item-title>
                            <v-list-item-subtitle>{{ product.join_way }}</v-list-item-subtitle>
                          </v-list-item>
                          <v-list-item>
                            <template v-slot:prepend>
                              <v-icon color="primary">mdi-star</v-icon>
                            </template>
                            <v-list-item-title>우대조건</v-list-item-title>
                            <v-list-item-subtitle>{{ product.spcl_cnd }}</v-list-item-subtitle>
                          </v-list-item>
                        </v-list>

                        <div class="text-subtitle-1 font-weight-bold my-2">금리 정보</div>
                        <v-table density="compact">
                          <thead>
                            <tr>
                              <th class="text-left">기간</th>
                              <th class="text-right">기본금리</th>
                              <th class="text-right">우대금리</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="month in [36, 24, 12, 6, 3, 1]" :key="month">
                              <td>{{ month }}개월</td>
                              <td class="text-right">{{ getRate(product.options, month, 'intr_rate') }}</td>
                              <td class="text-right">{{ getRate(product.options, month, 'intr_rate2') }}</td>
                            </tr>
                          </tbody>
                        </v-table>
                      </v-col>
                    </v-row>
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                      color="error"
                      variant="outlined"
                      size="small"
                      prepend-icon="mdi-delete"
                      @click="handleDeleteDeposit(product.id)"
                    >
                      삭제
                    </v-btn>
                    <v-btn
                      :color="isDepositRunning(product.id) ? 'success' : 'primary'"
                      variant="tonal"
                      size="small"
                      class="ml-2"
                      prepend-icon="mdi-run"
                      @click="toggleRunningDeposit(product.id, product.options)"
                    >
                      {{ isDepositRunning(product.id) ? '달리는중' : '달리기' }}
                    </v-btn>
                  </v-card-actions>
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-card>
        </v-col>

        <!-- 적금 상품 테이블 -->
        <v-col cols="12" md="6">
          <v-card variant="outlined">
            <v-card-title class="text-h6 bg-light-blue-lighten-5 py-3">
              적금 상품
            </v-card-title>
            <v-expansion-panels>
              <v-expansion-panel
                v-for="product in savingProducts"
                :key="product.id"
              >
                <v-expansion-panel-title>
                  <v-row no-gutters>
                    <v-col cols="5">{{ product.kor_co_nm }}</v-col>
                    <v-col cols="7" class="text-truncate">
                      {{ product.fin_prdt_nm }}
                    </v-col>
                  </v-row>
                </v-expansion-panel-title>
                <v-expansion-panel-text>
                  <v-card-text>
                    <v-row>
                      <v-col cols="12">
                        <div class="text-subtitle-1 font-weight-bold mb-2">상품 정보</div>
                        <v-list>
                          <v-list-item>
                            <template v-slot:prepend>
                              <v-icon color="primary">mdi-account-group</v-icon>
                            </template>
                            <v-list-item-title>가입대상</v-list-item-title>
                            <v-list-item-subtitle>{{ product.join_member }}</v-list-item-subtitle>
                          </v-list-item>
                          <v-list-item>
                            <template v-slot:prepend>
                              <v-icon color="primary">mdi-login</v-icon>
                            </template>
                            <v-list-item-title>가입방법</v-list-item-title>
                            <v-list-item-subtitle>{{ product.join_way }}</v-list-item-subtitle>
                          </v-list-item>
                          <v-list-item>
                            <template v-slot:prepend>
                              <v-icon color="primary">mdi-star</v-icon>
                            </template>
                            <v-list-item-title>우대조건</v-list-item-title>
                            <v-list-item-subtitle>{{ product.spcl_cnd }}</v-list-item-subtitle>
                          </v-list-item>
                        </v-list>

                        <div class="text-subtitle-1 font-weight-bold my-2">금리 정보</div>
                        <v-table density="compact">
                          <thead>
                            <tr>
                              <th class="text-left">기간</th>
                              <th class="text-right">기본금리</th>
                              <th class="text-right">우대금리</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="month in [36, 24, 12, 6, 3, 1]" :key="month">
                              <td>{{ month }}개월</td>
                              <td class="text-right">{{ getRate(product.options, month, 'intr_rate') }}</td>
                              <td class="text-right">{{ getRate(product.options, month, 'intr_rate2') }}</td>
                            </tr>
                          </tbody>
                        </v-table>
                      </v-col>
                    </v-row>
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                      color="error"
                      variant="outlined"
                      size="small"
                      prepend-icon="mdi-delete"
                      @click="handleDeleteSaving(product.id)"
                    >
                      삭제
                    </v-btn>
                    <v-btn
                      :color="isSavingRunning(product.id) ? 'success' : 'primary'"
                      variant="tonal"
                      size="small"
                      class="ml-2"
                      prepend-icon="mdi-run"
                      @click="toggleRunningSaving(product.id, product.options)"
                    >
                      {{ isSavingRunning(product.id) ? '달리는중' : '달리기' }}
                    </v-btn>
                  </v-card-actions>
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-card>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useProfileStore } from '@/stores/profile';

const profileStore = useProfileStore();
const runningDepositId = ref(null);
const runningSavingId = ref(null);

const isDepositRunning = (productId) => runningDepositId.value === productId;
const isSavingRunning = (productId) => runningSavingId.value === productId;

const depositProducts = computed(() => 
  profileStore.userProducts?.filter(product => product.Deposit_code === 1) || []
);

const savingProducts = computed(() => 
  profileStore.userProducts?.filter(product => product.Saving_code === 2) || []
);

const getRate = (options, month, rateType) => {
  const option = options.find(opt => opt.save_trm === month);
  return option ? `${option[rateType]}%` : '-';
};

const handleDeleteDeposit = (productId) => {
  if (confirm('정말 삭제하시겠습니까?')) {
    profileStore.deleteUserProduct('deposit', productId);
  }
};

const handleDeleteSaving = (productId) => {
  if (confirm('정말 삭제하시겠습니까?')) {
    profileStore.deleteUserProduct('saving', productId);
  }
};

const toggleRunningDeposit = (productId, options) => {
  if (runningDepositId.value === productId) {
    runningDepositId.value = null;
    profileStore.setSelectedRates({ deposit: null });
  } else {
    runningDepositId.value = productId;
    profileStore.setSelectedRates({ deposit: options });
  }
};

const toggleRunningSaving = (productId, options) => {
  if (runningSavingId.value === productId) {
    runningSavingId.value = null;
    profileStore.setSelectedRates({ saving: null });
  } else {
    runningSavingId.value = productId;
    profileStore.setSelectedRates({ saving: options });
  }
};

onMounted(() => {
  profileStore.getUserProducts();
});
</script>

<style scoped>
/* 기존 카드 스타일 */
.v-card {
  color: #333333 !important;
}

/* 카드 제목 배경색 변경 */
:deep(.v-card-title.bg-light-blue-lighten-5) {
  background-color: #ffd8b8 !important;
  color: #333333 !important;
}

/* 확장 패널 스타일 */
:deep(.v-expansion-panel-title) {
  color: #333333 !important;
}

:deep(.v-expansion-panel) {
  background-color: white !important;
}

:deep(.v-expansion-panel-text) {
  color: #333333 !important;
}

/* 리스트 아이템 스타일 */
:deep(.v-list-item-title),
:deep(.v-list-item-subtitle) {
  color: #333333 !important;
}

/* 테이블 스타일 */
:deep(.v-table) {
  color: #333333 !important;
}

/* 버튼 스타일 변경 */
:deep(.v-btn.v-btn--variant-tonal) {
  background-color: #fff0e6 !important;
  color: #333333 !important;
}

:deep(.v-btn.v-btn--variant-tonal.success) {
  background-color: #ffd8b8 !important;
  color: #333333 !important;
}

:deep(.v-btn.v-btn--variant-outlined) {
  border-color: #ffd8b8 !important;
  color: #333333 !important;
}

:deep(.v-btn.v-btn--variant-outlined.error) {
  border-color: #ef5350 !important;
  color: #ef5350 !important;
}

/* 아이콘 색상 */
:deep(.v-icon.text-primary) {
  color: #333333 !important;
}

/* 텍스트 스타일 */
.text-subtitle-1,
.font-weight-bold {
  color: #333333 !important;
}

/* 확장 패널 호버 효과 */
:deep(.v-expansion-panel-title--active) {
  background-color: #fff0e6 !important;
}

:deep(.v-expansion-panel-title:hover) {
  background-color: #fff0e6 !important;
}
</style>