<template>
  <div>
    <v-card class="search-result-card">
      <v-data-table :headers="headers" :items="results" :loading="loading" item-key="id" class="custom-table">
        <template v-slot:item="{ item }">
          <tr class="data-row">
            <!-- 비교선택 체크박스 -->
            <td class="checkbox-cell">
              <div class="checkbox-container d-flex justify-center">
                <v-checkbox dense hide-details @click.stop @change="handleItemSelect(item)" :model-value="isItemSelected(item)" :disabled="isCheckboxDisabled(item)" class="custom-checkbox" />
              </div>
            </td>

            <!-- 금융회사 -->
            <td class="company-cell">
              <div class="company-info">
                <span class="company-name">{{ item.kor_co_nm }}</span>
              </div>
            </td>

            <!-- 상품명 -->
            <td class="product-cell">
              <div class="product-info">
                <span class="product-name">{{ item.fin_prdt_nm }}</span>
              </div>
            </td>

            <!-- 이자 계산방법 -->
            <td class="interest-cell">
              <v-chip size="small" :color="getInterestRateType(item) === '단리' ? 'info' : 'success'" class="interest-chip">
                {{ getInterestRateType(item) }}
              </v-chip>
            </td>

            <!-- 상세보기 버튼 -->
            <td class="action-cell">
              <v-btn variant="outlined" size="small" @click="toggleDetails(item.id)" :color="expandedItems.includes(item.id) ? 'primary' : 'grey'" class="detail-btn">
                <v-icon size="small" class="mr-1">
                  {{ expandedItems.includes(item.id) ? "mdi-chevron-up" : "mdi-chevron-down" }}
                </v-icon>
                {{ expandedItems.includes(item.id) ? "접기" : "상세보기" }}
              </v-btn>
            </td>

            <!-- 담기 버튼 (로그인 시) -->
            <td v-if="userStore.isLogin" class="action-cell">
              <v-btn :color="searchStore.isContained[searchStore.getUniqueProductId(item)] ? 'grey' : 'success'" size="small" @click="searchStore.toggleContainer(item)" class="save-btn">
                <v-icon size="small" class="mr-1">
                  {{ searchStore.isContained[searchStore.getUniqueProductId(item)] ? "mdi-cart-remove" : "mdi-cart-plus" }}
                </v-icon>
                {{ searchStore.isContained[searchStore.getUniqueProductId(item)] ? "담기 취소" : "담기" }}
              </v-btn>
            </td>
          </tr>

          <!-- 상세 정보 행 -->
          <tr v-if="expandedItems.includes(item.id)" class="detail-row">
            <td :colspan="userStore.isLogin ? 6 : 5">
              <v-card flat class="detail-card pa-4">
                <v-row>
                  <!-- 기본 정보 섹션 -->
                  <v-col cols="12">
                    <div class="info-section">
                      <h3 class="info-title mb-4" style="padding:1;">상품 기본 정보</h3>
                      <div class="info-item">
                        <v-icon color="primary" class="mr-2">mdi-account-group</v-icon>
                        <strong>가입대상:</strong>
                        <span>{{ item.join_member }}</span>
                      </div>
                      <div class="info-item">
                        <v-icon color="primary" class="mr-2">mdi-login</v-icon>
                        <strong>가입방법:</strong>
                        <span>{{ item.join_way }}</span>
                      </div>
                      <div class="info-item">
                        <v-icon color="primary" class="mr-2">mdi-star</v-icon>
                        <strong>우대조건:</strong>
                        <span>{{ item.spcl_cnd }}</span>
                      </div>
                      <div class="info-item">
                        <v-icon color="primary" class="mr-2">mdi-information</v-icon>
                        <strong>유의사항:</strong>
                        <span>{{ item.etc_note }}</span>
                      </div>
                    </div>

                    <!-- 금리 정보 컨테이너 -->
                    <div class="rates-container mt-4">
                      <h3 class="info-title">금리 정보</h3>
                      <div class="rates-content">
                        <!-- 차트 -->
                        <div class="graph-section">
                          <div class="graph-container">
                            <v-chart class="rate-chart" :option="getChartOptions(item)" autoresize />
                          </div>
                        </div>

                        <!-- 금리 테이블 -->
                        <div class="table-section">
                          <v-table class="rate-table">
                            <thead>
                              <tr>
                                <th class="text-center">기간</th>
                                <th class="text-center">저축 금리</th>
                                <th class="text-center">최고 우대 금리</th>
                              </tr>
                            </thead>
                            <tbody>
                              <tr v-for="term in [36, 24, 12, 6, 3, 1]" :key="term">
                                <td class="text-center">{{ term }}개월</td>
                                <td class="text-center">{{ getInterestRate(item, term, "intr_rate") }}</td>
                                <td class="text-center">{{ getInterestRate(item, term, "intr_rate2") }}</td>
                              </tr>
                            </tbody>
                          </v-table>
                        </div>
                      </div>
                    </div>
                  </v-col>
                </v-row>
              </v-card>
            </td>
          </tr>
        </template>
      </v-data-table>
    </v-card>

    <!-- 선택된 상품 비교 섹션 -->
    <v-card v-if="searchStore.selectedItems.length > 0" class="compare-card mt-4">
      <div class="d-flex align-center justify-space-between pa-4">
        <div class="selected-items">
          <v-chip-group>
            <v-chip v-for="item in searchStore.selectedItems" :key="item.uniqueId" closable class="selected-chip" color="primary" @click:close="searchStore.removeSelectedItem(item.uniqueId)">
              <v-icon size="small" class="mr-1">mdi-bank</v-icon>
              {{ item.kor_co_nm }} - {{ item.fin_prdt_nm }}
            </v-chip>
          </v-chip-group>
        </div>
        <v-btn :color="searchStore.isCompareButtonActive ? 'success' : 'grey'" :disabled="!searchStore.isCompareButtonActive" @click="openCompareModal" class="compare-btn">
          <v-icon left>mdi-compare</v-icon>
          비교하기
        </v-btn>
      </div>
    </v-card>

    <SearchCompare ref="compareModalRef" />
  </div>
</template>
<script setup>
import { ref, onMounted, watch } from "vue";
import { useSearchStore } from "@/stores/search";
import { useUserStore } from "@/stores/user";
import SearchCompare from "@/components/SearchCompare.vue";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart } from "echarts/charts";
import { GridComponent, TooltipComponent, LegendComponent } from "echarts/components";
import VChart from "vue-echarts";

use([CanvasRenderer, BarChart, GridComponent, TooltipComponent, LegendComponent]);

const getChartOptions = (item) => {
  const terms = [36, 24, 12, 6, 3, 1];
  const baseRates = terms.map((term) => parseFloat(getInterestRate(item, term, "intr_rate").replace("%", "") || 0));
  const specialRates = terms.map((term) => parseFloat(getInterestRate(item, term, "intr_rate2").replace("%", "") || 0));

  return {
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "shadow",
      },
      formatter: (params) => {
        return `${params[0].name}<br/>
                ${params[0].seriesName}: ${params[0].value}%<br/>
                ${params[1].seriesName}: ${params[1].value}%`;
      },
    },
    legend: {
      data: ["저축 금리", "최고 우대 금리"],
      bottom: "0%",
    },
    grid: {
      left: "3%",
      right: "4%",
      bottom: "15%",
      top: "3%",
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: terms.map((term) => `${term}개월`),
      axisLabel: {
        interval: 0,
      },
    },
    yAxis: {
      type: "value",
      name: "금리 (%)",
      nameTextStyle: {
        padding: [0, 0, 0, 30],
      },
      axisLabel: {
        formatter: "{value}%",
      },
    },
    series: [
      {
        name: "저축 금리",
        type: "bar",
        data: baseRates,
        color: "#4CAF50",
        barWidth: "20%",
        emphasis: {
          focus: "series",
        },
        animation: true,
      },
      {
        name: "최고 우대 금리",
        type: "bar",
        data: specialRates,
        color: "#2196F3",
        barWidth: "20%",
        emphasis: {
          focus: "series",
        },
        animation: true,
      },
    ],
  };
};

const searchStore = useSearchStore();
const userStore = useUserStore();
const compareModalRef = ref(null);
const expandedItems = ref([]);

const props = defineProps({
  results: {
    type: Array,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

const headers = [
  { title: "비교선택", align: "center", sortable: false },
  { title: "금융회사", key: "kor_co_nm", align: "start", sortable: true },
  { title: "상품명", key: "fin_prdt_nm", align: "start", sortable: true },
  { title: "이자 계산", key: "intr_rate_type_nm", align: "start", sortable: true },
  { title: "상세정보", align: "center", sortable: false, width: "100px" },
  ...(userStore.isLogin ? [{ title: "담기", align: "center", sortable: false, width: "100px" }] : []),
];

const getInterestRateType = (item) => {
  if (item.Deposit_code === 1) {
    const option = searchStore.depositOptions.find((opt) => opt.deposit_product === item.id);
    return option ? option.intr_rate_type_nm : "-";
  } else {
    const option = searchStore.savingOptions.find((opt) => opt.saving_product === item.id);
    return option ? option.intr_rate_type_nm : "-";
  }
};

const getInterestRate = (item, term, rateType) => {
  if (item.Deposit_code === 1) {
    const option = searchStore.depositOptions.find((opt) => opt.deposit_product === item.id && opt.save_trm === term);
    return option ? `${option[rateType]}%` : "-";
  } else {
    const option = searchStore.savingOptions.find((opt) => opt.saving_product === item.id && opt.save_trm === term);
    return option ? `${option[rateType]}%` : "-";
  }
};

const handleItemSelect = (item) => {
  searchStore.toggleItemSelection(item); // 전체 item 객체를 전달
};

const isCheckboxDisabled = (item) => {
  if (searchStore.isItemSelected(item)) return false;
  return searchStore.selectedItems.length >= 4;
};

const isItemSelected = (item) => {
  return searchStore.isItemSelected(item);
};

const openCompareModal = () => {
  compareModalRef.value?.openModal();
};

const toggleDetails = (productId) => {
  const index = expandedItems.value.indexOf(productId);
  if (index === -1) {
    expandedItems.value.push(productId);
  } else {
    expandedItems.value.splice(index, 1);
  }
};

watch(
  () => userStore.isLogin,
  (newValue) => {
    if (newValue) {
      // 로그인 시 사용자의 담은 상품 목록 가져오기
      searchStore.fetchContainedProducts();
    } else {
      // 로그아웃 시 상태 초기화
      searchStore.clearContainedState();
    }
  }
);

onMounted(() => {
  if (userStore.isLogin) {
    searchStore.fetchContainedProducts();
  }
});
</script>

<style scoped>
/* 기본 카드 스타일링 */
.search-result-card {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.custom-table {
  background-color: white;
}

.data-row {
  transition: background-color 0.2s;
}

.data-row:hover {
  background-color: #f8f9fa;
}

.data-row td {
  padding: 12px;
  vertical-align: middle;
}

/* 셀 스타일링 */
.checkbox-cell {
  width: 60px;
  padding: 0 !important;
}

.company-cell {
  min-width: 120px;
}

.product-cell {
  min-width: 200px;
}

.interest-cell {
  width: 120px;
}

.action-cell {
  width: 120px;
}

.company-name {
  font-weight: 500;
  color: #2c3e50;
}

.product-name {
  color: #34495e;
}

.interest-chip {
  font-size: 0.85rem;
  font-weight: 500;
}

.detail-btn,
.save-btn {
  width: 100%;
  text-transform: none;
}

/* 상세 정보 스타일링 */
.detail-card {
  background-color: #f8f9fa;
  border-top: 1px solid #e9ecef;
}

.info-title {
  color: #2c3e50;
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.info-item {
  display: flex;
  align-items: start;
  margin-bottom: 1rem;
  gap: 8px;
}

.info-item strong {
  color: #2c3e50;
  min-width: 80px;
}

.info-item span {
  color: #495057;
  flex: 1;
}

/* 금리 정보 컨테이너 */
.rates-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
}

/* 그래프 섹션 */
.graph-container {
  width: 100%;
  height: 500px;
  background: white;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.rate-chart {
  width: 100%;
  height: 100%;
}

/* 테이블 섹션 */
.table-section {
  background: white;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.rate-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  overflow: hidden;
}

.rate-table th {
  background-color: #f1f3f5;
  color: #2c3e50;
  font-weight: 600;
  padding: 12px;
  border-bottom: 1px solid #e9ecef;
}

.rate-table td {
  padding: 12px;
  color: #495057;
  border-bottom: 1px solid #e9ecef;
}

.rate-table tr:last-child td {
  border-bottom: none;
}

/* 비교 섹션 스타일링 */
.compare-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.selected-chip {
  font-weight: 500;
  text-transform: none;
}

.compare-btn {
  text-transform: none;
  font-weight: 500;
}

/* ECharts 툴팁 스타일 커스터마이징 */
:deep(.echarts-tooltip) {
  background: rgba(255, 255, 255, 0.9) !important;
  backdrop-filter: blur(4px);
  border-radius: 4px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 8px;
}

/* 반응형 디자인 */
/* @media (max-width: 768px) {
  .info-item {
    flex-direction: column;
  }

  .info-item strong {
    min-width: auto;
  }

  .detail-card {
    padding: 12px !important;
  }

  .rates-container {
    padding: 1rem;
  }

  .graph-container {
    height: 250px;
  }
} */
.rates-container {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
}

.rates-content {
  display: flex;
  gap: 1.5rem;
  margin-top: 1rem;
}

.graph-section {
  flex: 1;
  min-width: 0; /* 플렉스 아이템 오버플로우 방지 */
}

.table-section {
  flex: 1;
  min-width: 0; /* 플렉스 아이템 오버플로우 방지 */
  background: white;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
/* 
.graph-container {
  width: 100%;
  height: 300px;
  background: white;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
} */

/* 반응형 디자인 수정 */
@media (max-width: 768px) {
  .rates-content {
    flex-direction: column;
  }
  
  .graph-container {
    height: 250px;
  }
  
  .graph-section,
  .table-section {
    width: 100%;
  }
}
</style>