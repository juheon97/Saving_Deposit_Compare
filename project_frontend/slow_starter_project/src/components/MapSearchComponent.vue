<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-container class="map-component-under">
          <v-row>
            <v-col>
            </v-col>
          </v-row>
          <div class="map_wrap">
            <div id="mapContainer" class="map-container"></div>
          </div>
          
          <!-- 검색 결과 섹션 -->
          <div class="results-section" v-if="resultCount > 0">
            <div class="results-header">
              <div class="results-title">
                <v-icon large color="primary" class="mr-2">mdi-bank</v-icon>
                검색된 은행 지점
                <v-chip class="ml-2 result-count-chip" color="primary" small>
                  {{ resultCount }}
                </v-chip>
              </div>
            </div>

            <!-- 결과 목록 -->
            <div class="results-content">
              <ul id="placesList" class="kakao-list"></ul>
              <div id="pagination" class="kakao-pagination"></div>
            </div>

            <!-- 선택된 은행 상세 정보 -->
            <v-expand-transition>
              <div v-if="selectedPlace" class="selected-place-details">
                <v-divider></v-divider>
                <div class="details-content">
                  <div class="details-header">
                    <v-icon large color="primary" class="mr-2">mdi-map-marker</v-icon>
                    <h3>{{ selectedPlace.place_name }}</h3>
                  </div>
                  
                  <div class="details-grid">
                    <div class="detail-item">
                      <v-icon small color="grey" class="mr-2">mdi-map</v-icon>
                      <span class="detail-label">도로명:</span>
                      <span class="detail-value">{{ selectedPlace.road_address_name || '정보 없음' }}</span>
                    </div>
                    
                    <div class="detail-item">
                      <v-icon small color="grey" class="mr-2">mdi-home</v-icon>
                      <span class="detail-label">지번:</span>
                      <span class="detail-value">{{ selectedPlace.address_name }}</span>
                    </div>
                    
                    <div class="detail-item">
                      <v-icon small color="grey" class="mr-2">mdi-phone</v-icon>
                      <span class="detail-label">전화:</span>
                      <span class="detail-value">{{ selectedPlace.phone || '정보 없음' }}</span>
                    </div>

                    <div class="detail-actions">
                      <v-btn 
                        small 
                        outlined 
                        color="primary"
                        class="action-button"
                        @click="copyAddress"
                      >
                        <v-icon small left>mdi-content-copy</v-icon>
                        주소 복사
                      </v-btn>
                      <v-btn 
                        small 
                        outlined 
                        color="primary"
                        class="action-button"
                        @click="openKakaoMap"
                      >
                        <v-icon small left>mdi-map-marker-radius</v-icon>
                        길찾기
                      </v-btn>
                    </div>
                  </div>
                </div>
              </div>
            </v-expand-transition>
          </div>
        </v-container>
      </v-col>
    </v-row>

    <!-- 주소 복사 완료 스낵바 -->
    <v-snackbar
      v-model="showCopySnackbar"
      :timeout="2000"
      color="success"
      centered
      top
    >
      주소가 클립보드에 복사되었습니다
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from "vue";

const props = defineProps({
  province: String,
  city: String,
  bank: String,
});

const emit = defineEmits(['update-selected-place']);

const map = ref(null);
const infowindow = ref(null);
const markers = ref([]);
const selectedPlace = ref(null);
const isMapReady = ref(false);
const ps = ref(null);
const resultCount = ref(0);
const showCopySnackbar = ref(false);

const loadKakaoMap = function () {
  return new Promise((resolve, reject) => {
    const script = document.createElement("script");
    const KAKAO_KEY = import.meta.env.VITE_KAKAO_MAP_API;
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_KEY}&autoload=false&libraries=services`;
    script.async = true;
    
    script.onload = () => {
      window.kakao.maps.load(() => {
        initializeKakaoMap()
          .then(() => {
            isMapReady.value = true;
            resolve();
          })
          .catch(reject);
      });
    };
    
    script.onerror = (error) => {
      console.error('Kakao 지도 API 로드 실패:', error);
      reject(error);
    };
    
    document.head.appendChild(script);
  });
};

const initializeKakaoMap = function () {
  return new Promise((resolve) => {
    let lat = 36.10706;
    let lon = 128.415494;
    
    const mapContainer = document.getElementById("mapContainer");
    const mapOption = {
      center: new window.kakao.maps.LatLng(lat, lon),
      level: 3,
    };

    map.value = new window.kakao.maps.Map(mapContainer, mapOption);
    infowindow.value = new window.kakao.maps.InfoWindow({ zIndex: 1 });
    ps.value = new window.kakao.maps.services.Places();
    resolve();
  });
};


// props 변경 감지를 위한 watch 추가
watch(
  [() => props.province, () => props.city, () => props.bank],
  async ([newProvince, newCity, newBank], [oldProvince, oldCity, oldBank]) => {
    // 모든 값이 존재하고, 이전 값과 다를 때만 검색 실행
    if (
      isMapReady.value && 
      newProvince && 
      newCity && 
      newBank &&
      (newProvince !== oldProvince || newCity !== oldCity || newBank !== oldBank)
    ) {
      await searchOnMap();
    }
  },
  { deep: true } // 깊은 감시 설정
);

// searchOnMap을 async 함수로 수정
const searchOnMap = async function () {
  if (!isMapReady.value || !map.value) {
    console.error('지도가 아직 초기화되지 않았습니다.');
    return;
  }
  
  // 모든 값이 있는지 확인
  if (!props.province || !props.city || !props.bank) {
    console.log('모든 값이 선택되지 않았습니다.');
    return;
  }

  const keyword = `${props.province} ${props.city} ${props.bank}`;
  await searchPlaces(keyword);
};




const searchPlaces = function (keyword) {
  if (!ps.value) return;
  ps.value.keywordSearch(keyword, placesSearchCB);
};

const placesSearchCB = function (data, status, pagination) {
  if (status === window.kakao.maps.services.Status.OK) {
    resultCount.value = data.length;
    removeAllMarkers();
    let bounds = new window.kakao.maps.LatLngBounds();

    const listEl = document.getElementById('placesList');
    const fragment = document.createDocumentFragment();
    
    removeAllChildNods(listEl);

    for (let i = 0; i < data.length; i++) {
      const placePosition = new window.kakao.maps.LatLng(data[i].y, data[i].x);
      const marker = displayMarker(data[i]);
      const itemEl = getListItem(i, data[i]);
      
      bounds.extend(placePosition);

      ((marker, title) => {
        window.kakao.maps.event.addListener(marker, 'mouseover', () => {
          displayInfowindow(marker, title);
        });

        window.kakao.maps.event.addListener(marker, 'mouseout', () => {
          infowindow.value.close();
        });

        itemEl.onmouseover = () => {
          displayInfowindow(marker, title);
        };

        itemEl.onmouseout = () => {
          infowindow.value.close();
        };
      })(marker, data[i].place_name);

      fragment.appendChild(itemEl);
    }

    listEl.appendChild(fragment);
    
    if (data.length > 0) {
      selectedPlace.value = data[0];
      emit('update-selected-place', data[0]);
    }

    map.value.setBounds(bounds);
    displayPagination(pagination);
  } else if (status === window.kakao.maps.services.Status.ZERO_RESULT) {
    resultCount.value = data.length;
    removeAllMarkers(); // 마커 제거 추가
    removeAllChildNods(document.getElementById('placesList')); // 리스트 초기화 추가
  } else if (status === window.kakao.maps.services.Status.ERROR) {
    resultCount.value = 0;
    alert('검색 중 오류가 발생했습니다.');
    removeAllMarkers(); // 마커 제거 추가
    removeAllChildNods(document.getElementById('placesList')); // 리스트 초기화 추가
  }
};

const copyAddress = async () => {
  if (selectedPlace.value) {
    const address = selectedPlace.value.road_address_name || selectedPlace.value.address_name;
    try {
      await navigator.clipboard.writeText(address);
      showCopySnackbar.value = true;
    } catch (err) {
      console.error('주소 복사 중 오류 발생:', err);
    }
  }
};

const openKakaoMap = () => {
  if (selectedPlace.value) {
    const lat = selectedPlace.value.y;
    const lng = selectedPlace.value.x;
    const name = encodeURIComponent(selectedPlace.value.place_name);
    window.open(`https://map.kakao.com/link/to/${name},${lat},${lng}`, '_blank');
  }
};

const displayPagination = (pagination) => {
  const paginationEl = document.getElementById('pagination');
  const fragment = document.createDocumentFragment();
  
  while (paginationEl.hasChildNodes()) {
    paginationEl.removeChild(paginationEl.lastChild);
  }

  for (let i = 1; i <= pagination.last; i++) {
    const el = document.createElement('a');
    el.href = "#";
    el.innerHTML = i;
    el.className = 'pagination-btn';

    if (i === pagination.current) {
      el.classList.add('current');
    } else {
      el.onclick = (() => {
        return () => {
          pagination.gotoPage(i);
        };
      })();
    }

    fragment.appendChild(el);
  }
  paginationEl.appendChild(fragment);
};

const getListItem = (index, place) => {
  const el = document.createElement('li');
  let itemStr = `
    <div class="kakao-list-item">
      <div class="place-info">
        <div class="place-name">
          ${place.place_name}
        </div>
        ${place.road_address_name ? 
          `<div class="place-address">
            <div class="road-address">${place.road_address_name}</div>
            <div class="jibun-address">${place.address_name}</div>
           </div>` : 
          `<div class="place-address">
            <div class="road-address">${place.address_name}</div>
           </div>`
        }
        ${place.phone ? 
          `<div class="place-phone">${place.phone}</div>` : 
          ''
        }
      </div>
    </div>
  `;

  el.innerHTML = itemStr;
  el.className = 'kakao-list-item-wrapper';
  
  el.onclick = () => {
    selectedPlace.value = place;
    emit('update-selected-place', place);
    
    const items = document.querySelectorAll('.kakao-list-item-wrapper');
    items.forEach(item => item.classList.remove('selected'));
    el.classList.add('selected');

    const moveLatLng = new window.kakao.maps.LatLng(place.y, place.x);
    map.value.panTo(moveLatLng);
  };

  return el;
};

const removeAllChildNods = (el) => {
  while (el.hasChildNodes()) {
    el.removeChild(el.lastChild);
  }
};

const removeAllMarkers = function () {
  for (let i = 0; i < markers.value.length; i++) {
    markers.value[i].setMap(null);
  }
  markers.value = [];
};

const displayInfowindow = (marker, title) => {
  const content = '<div style="padding:5px;z-index:1;">' + title + '</div>';
  infowindow.value.setContent(content);
  infowindow.value.open(map.value, marker);
};

const displayMarker = function (place) {
  if (!map.value || !window.kakao || !window.kakao.maps) {
    console.error('지도가 초기화되지 않았거나 Kakao 지도 API가 로드되지 않았습니다.');
    return;
  }

  const marker = new window.kakao.maps.Marker({
    map: map.value,
    position: new window.kakao.maps.LatLng(place.y, place.x),
  });

  window.kakao.maps.event.addListener(marker, "click", () => {
    selectedPlace.value = place;
    emit('update-selected-place', place);
    displayInfowindow(marker, place.place_name);
  });

  markers.value.push(marker);
  return marker;
};

onMounted(async () => {
  try {
    await loadKakaoMap();
    window.addEventListener("resize", () => {
      if (map.value) {
        map.value.relayout();
      }
    });
  } catch (error) {
    console.error('맵 초기화 중 오류 발생:', error);
  }
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", () => {
    if (map.value) {
      map.value.relayout();
    }
  });
});
</script>

<style>
.map-container {
  width: 100%;
  height: 500px;
  position: relative;
}

.map_wrap {
  position: relative;
  width: 100%;
  height: auto;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.results-section {
  background: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  overflow: hidden;
  margin-top: 24px;
}

.results-header {
  padding: 15px 20px;
  background: #ffd8b8;
  border-bottom: 1px solid #ddd;
}

.results-title {
  font-size: 16px;
  font-weight: bold;
  color: #333333;
  display: flex;
  align-items: center;
}

.results-content {
  padding: 0;
}

.kakao-list {
  padding: 0;
  margin: 0;
  background-color: #fff;
  width: 100%;
  max-height: 300px;
  overflow-y: auto;
}

.kakao-list-item-wrapper {
  width: 100%;
  padding: 12px 20px;
  border-bottom: 1px solid #e6e6e6;
  cursor: pointer;
}

.kakao-list-item-wrapper:hover {
  background-color: #ffe4d1;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.kakao-list-item-wrapper.selected {
  background-color: #ffe4d1;
  box-shadow: 0 4px 12px rgba(255, 216, 184, 0.1);
}

.kakao-list-item-wrapper:hover::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background-color: #ffd8b8;
}

.place-name {
  color: #333333;
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 8px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.place-address {
  font-size: 12px;
  color: #333333;
  margin-bottom: 5px;
}

.road-address {
  color: #333333;
  font-size: 12px;
  font-weight: 400;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 6px;
}

.jibun-address {
  color: #333333;
  font-size: 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.place-phone {
  color: #333333;
  font-size: 13px;
  margin-top: 6px;
  font-weight: 500;
}

.selected-place-details {
  background-color: #fff1e6;
  padding: 24px;
}

.details-header h3 {
  font-size: 18px;
  color: #333333;
  margin: 0;
}

.detail-label {
  color: #333333;
  font-size: 14px;
  min-width: 60px;
}

.detail-value {
  color: #333333;
  font-size: 14px;
  font-weight: 500;
}

.kakao-pagination {
  padding: 16px;
  display: flex;
  justify-content: center;
  gap: 8px;
  background-color: #ffd8b8;
}

.pagination-btn {
  min-width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  color: #333333;
  text-decoration: none;
  transition: all 0.2s ease;
  font-size: 14px;
}

.pagination-btn:hover {
  background-color: #ffe4d1;
  color: #333333;
}

.pagination-btn.current {
  background-color: #ffe4d1;
  color: #333333;
  font-weight: bold;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.search-button {
  background-color: #ffe4d1 !important;
  color: #333333 !important;
  padding: 0 28px !important;
  height: 48px !important;
  font-size: 16px !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
  border-radius: 12px !important;
  box-shadow: 0 4px 6px rgba(255, 216, 184, 0.2) !important;
}

.search-button:hover {
  background-color: #ffe9d9 !important;
  box-shadow: 0 6px 8px rgba(255, 216, 184, 0.3) !important;
}

.kakao-list::-webkit-scrollbar-thumb {
  background: #ffd8b8;
  border-radius: 3px;
}

.kakao-list::-webkit-scrollbar-thumb:hover {
  background: #ffe4d1;
}

.kakao-list-item-wrapper:hover .place-name {
  color: #333333;
}
</style>