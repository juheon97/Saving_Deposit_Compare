<template>
  <v-container fluid class="pa-0 main-container">
    <v-sheet class="bg-background" width="100%" min-height="100vh">
      <v-container>
        <v-row justify="center">
          <v-col cols="12" lg="10">
            <!-- Error Alert -->
            <v-alert
              v-if="profileStore.error"
              type="error"
              variant="tonal"
              class="mb-4"
            >
              {{ profileStore.error }}
            </v-alert>

            <!-- Profile Section -->
            <v-row v-if="profileStore.user_info" class="mb-6">
              <!-- Profile Image Card -->
              <v-col cols="12" md="4">
                <v-card elevation="2" class="h-100">
                  <v-card-item class="text-center">
                    <v-avatar size="180" class="mb-4">
                      <v-img
  :src="profileStore.user_info.image + '?t=' + new Date().getTime()"
  :key="profileStore.user_info.image"
  alt="프로필 이미지"
  cover
  />
                    </v-avatar>
                    <v-file-input
                    ref="fileInput"
                      v-model="fileInput"
                      accept="image/*"
                      hide-input
                      class="d-none"
                      @change="handleImageChange"
                    />
                    <v-btn
                      color="primary"
                      block
                      @click="$refs.fileInput.click()"
                      prepend-icon="mdi-camera"
                    >
                      프로필 이미지 변경
                    </v-btn>
                  </v-card-item>
                </v-card>
              </v-col>

              <!-- Profile Info Card -->
              <v-col cols="12" md="8">
                <v-card elevation="2" class="h-100">
                  <v-card-item>
                    <v-card-title class="text-h5 mb-4">
                      {{ profileStore.user_info.first_name }}님의 프로필
                    </v-card-title>
                    <v-row dense>
                      <v-col cols="12" sm="6">
                        <v-list-item>
                          <template v-slot:prepend>
                            <v-icon color="primary">mdi-account</v-icon>
                          </template>
                          <v-list-item-title>아이디</v-list-item-title>
                          <v-list-item-subtitle>{{ profileStore.user_info.username }}</v-list-item-subtitle>
                        </v-list-item>
                      </v-col>
                      <v-col cols="12" sm="6">
                        <v-list-item>
                          <template v-slot:prepend>
                            <v-icon color="primary">mdi-email</v-icon>
                          </template>
                          <v-list-item-title>이메일</v-list-item-title>
                          <v-list-item-subtitle>{{ profileStore.user_info.email }}</v-list-item-subtitle>
                        </v-list-item>
                      </v-col>
                      <v-col cols="12" sm="6">
                        <v-list-item>
                          <template v-slot:prepend>
                            <v-icon color="primary">mdi-gender-male-female</v-icon>
                          </template>
                          <v-list-item-title>성별</v-list-item-title>
                          <v-list-item-subtitle>
                            {{ profileStore.user_info.gender === "M" ? "남성" : "여성" }}
                          </v-list-item-subtitle>
                        </v-list-item>
                      </v-col>
                      <v-col cols="12" sm="6">
                        <v-list-item>
                          <template v-slot:prepend>
                            <v-icon color="primary">mdi-calendar</v-icon>
                          </template>
                          <v-list-item-title>나이</v-list-item-title>
                          <v-list-item-subtitle>{{ profileStore.user_info.age }}</v-list-item-subtitle>
                        </v-list-item>
                      </v-col>
                      <v-col cols="12" sm="6">
                        <v-list-item>
                          <template v-slot:prepend>
                            <v-icon color="primary">mdi-bank</v-icon>
                          </template>
                          <v-list-item-title>예금</v-list-item-title>
                          <v-list-item-subtitle>{{ profileStore.user_info.balance_deposit }}</v-list-item-subtitle>
                        </v-list-item>
                      </v-col>
                      <v-col cols="12" sm="6">
                        <v-list-item>
                          <template v-slot:prepend>
                            <v-icon color="primary">mdi-piggy-bank</v-icon>
                          </template>
                          <v-list-item-title>적금</v-list-item-title>
                          <v-list-item-subtitle>{{ profileStore.user_info.balance_saving }}</v-list-item-subtitle>
                        </v-list-item>
                      </v-col>
                    </v-row>
                    <ProfileMoney />
                  </v-card-item>
                  <v-card-actions class="pa-4">
                    <v-spacer />
                    <v-btn
                      color= #cccccc
                      variant="elevated"
                      @click="openModal"
                      prepend-icon="mdi-pencil"
                    >
                      기본 정보 수정
                    </v-btn>
                    <v-btn
                      color= #cccccc
                      variant="elevated"
                      @click="openPasswordPage"
                      prepend-icon="mdi-lock"
                      class="ml-2"
                    >
                      비밀번호 변경
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>

            <!-- Products Section -->
            <v-row>
              <v-col cols="12">
                <ProfileContainList />
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
    </v-sheet>

    <ProfileChangeBasic :isOpen="isModalOpen" @close="closeModal" />
  </v-container>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useProfileStore } from "@/stores/profile";
import ProfileChangeBasic from "@/components/ProfileChangeBasic.vue";
import ProfileContainList from "@/components/ProfileContainList.vue";
import ProfileMoney from '@/components/ProfileMoney.vue';
import { useRouter } from "vue-router";

const router = useRouter();
const profileStore = useProfileStore();
const fileInput = ref(null);
const isModalOpen = ref(false);

const handleImageChange = async (event) => {
  console.log('File change event:', event);
  
  if (event && event.target && event.target.files) {
    const file = event.target.files[0];
    console.log('Selected file:', file);
    
    if (file) {
      try {
        await profileStore.updateProfileImage(file);
        console.log('Image update completed');
      } catch (error) {
        console.error('Error updating image:', error);
      }
    }
  }
};

const openModal = () => {
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
};

const openPasswordPage = () => {
  router.push('/password');
};

onMounted(() => {
  profileStore.getUser();
});
</script>

<style scoped>
.main-container {
  background-color: #ffd8b8;
}

.v-card {
  border-radius: 12px;
  background-color: white !important;
}

.v-avatar {
  border: 4px solid #fff;
  box-shadow: 0 2px 8px rgba(255, 216, 184, 0.2);
}

/* 텍스트 색상 통일 */
:deep(.v-card-title),
:deep(.v-list-item-title),
:deep(.v-list-item-subtitle) {
  color: #333333 !important;
}

/* 아이콘 색상 */
:deep(.v-icon.text-primary) {
  color: #333333 !important;
}

/* 버튼 스타일 */
:deep(.v-btn.text-primary) {
  background-color: #ffd8b8 !important;
  color: #333333 !important;
}

:deep(.v-btn.text-warning) {
  background-color: #fff0e6 !important;
  color: #333333 !important;
}

:deep(.v-btn:hover) {
  background-color: #ffe4d0 !important;
}

/* 프로필 이미지 변경 버튼 */
:deep(.v-btn.v-btn--block) {
  background-color: #ffd8b8 !important;
  color: #333333 !important;
}

:deep(.v-btn.v-btn--block:hover) {
  background-color: #ffe4d0 !important;
}

/* 알럿 스타일 */
:deep(.v-alert.bg-error) {
  background-color: #fff0e6 !important;
  color: #333333 !important;
}

/* 배경 시트 */
:deep(.bg-background) {
  background-color: #ffd8b8 !important;
}

/* 리스트 아이템 호버 효과 */
:deep(.v-list-item:hover) {
  background-color: #fff5ee !important;
}

/* 카드 액션 영역 */
:deep(.v-card-actions) {
  border-top: 1px solid #ffe4d0;
}

/* 파일 입력 관련 */
:deep(.v-file-input) {
  color: #333333 !important;
}

/* 컨테이너 배경 */
:deep(.v-container) {
  background-color: transparent;
}

/* 시트 배경 */
:deep(.v-sheet) {
  background-color: #ffd8b8 !important;
}

/* 카드 그림자 효과 */
:deep(.v-card.v-card--elevation-2) {
  box-shadow: 0 4px 12px rgba(255, 216, 184, 0.2) !important;
}
</style>