<template>
    <v-dialog
      :model-value="show"
      @update:model-value="$emit('update:show', $event)"
      max-width="500"
      persistent
    >
      <v-card>
        <v-card-title class="text-h5 pa-6">
          비밀번호 변경 확인
        </v-card-title>
  
        <v-card-text class="pa-6">
          비밀번호를 변경하시겠습니까?
        </v-card-text>
  
        <v-card-actions class="pa-6">
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            @click="handleConfirm"
            :loading="loading"
          >
            확인
          </v-btn>
          <v-btn
            color="grey-lighten-1"
            @click="$emit('update:show', false)"
            :disabled="loading"
          >
            취소
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const props = defineProps({
    show: Boolean,
    passwords: {
      type: Object,
      required: true
    }
  });
  
  const emit = defineEmits(['update:show', 'confirmed']);
  const loading = ref(false);
  
  const handleConfirm = async () => {
    loading.value = true;
    emit('confirmed');
    loading.value = false;
    emit('update:show', false);
  };
  </script>
  