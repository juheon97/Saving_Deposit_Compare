<template>
    <v-dialog
      :model-value="show"
      @update:model-value="$emit('update:show', $event)"
      max-width="500"
      persistent
    >
      <v-card>
        <v-card-title class="text-h5 pa-6">
          임시 비밀번호가 생성되었습니다
        </v-card-title>
  
        <v-card-text class="pa-6" style="color:whilte">
          <p class="mb-4">아래의 임시 비밀번호로 로그인해 주세요.</p>
          <v-text-field
            :model-value="tempPassword"
            readonly
            variant="outlined"
            class="mb-4"
            append-inner-icon="mdi-content-copy"
            @click:append-inner="copyToClipboard"
          ></v-text-field>
          <p class="text-caption text-red">보안을 위해 로그인 후 반드시 비밀번호를 변경해 주세요.</p>
        </v-card-text>
  
        <v-card-actions class="pa-6">
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            @click="handleClose"
          >
            확인
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>
  
  <script setup>
  const props = defineProps({
    show: {
      type: Boolean,
      required: true
    },
    tempPassword: {
      type: String,
      required: true
    }
  })
  
  const emit = defineEmits(['update:show'])
  
  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(props.tempPassword)
      alert('클립보드에 복사되었습니다.')
    } catch (err) {
      console.error('클립보드 복사 실패:', err)
      alert('클립보드 복사에 실패했습니다.')
    }
  }
  
  const handleClose = () => {
    emit('update:show', false)
  }
  </script>