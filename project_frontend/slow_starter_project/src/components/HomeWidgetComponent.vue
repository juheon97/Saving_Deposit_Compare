<!-- HomeWidgetComponent.vue -->
<template>
  <v-carousel
    height="100%"
    width="100%"
    cycle
    interval="4000" 
    :show-arrows="false"
    :continuous="true"
    class="custom-carousel"
  >
    <v-carousel-item
      v-for="(slide, i) in slides"
      :key="i"
      class="carousel-item"
    >
      <v-sheet
        class="carousel-sheet fill-height"
      >
        <div class="image-container">
          <img 
            :src="slide.image" 
            :alt="slide.title" 
            class="carousel-image"
            @click="navigate(slide.path)"
            style="cursor: pointer"
          />
        </div>
      </v-sheet>
    </v-carousel-item>
  </v-carousel>
</template>

<script>
import { useRouter } from 'vue-router';
import image1 from '@/assets/widgets/img1.png'
import image2 from '@/assets/widgets/img2.png'
import image3 from '@/assets/widgets/img3.png'

export default {
  setup() {
    const router = useRouter();

    const navigate = (path) => {
      router.push(path);
    };

    return {
      navigate
    };
  },

  data () {
    return {
      slides: [
        {
          image: image1,
          path: '/boards',
          title: 'Boards'
        },
        {
          image: image2,
          path: '/',
          title: 'Home'
        },
        {
          image: image3,
          path: '/search',
          title: 'Search'
        }
      ],
    }
  },
}
</script>

<style scoped>
.custom-carousel {
  height: 100% !important;
  background: transparent;
}

.carousel-item {
  height: 100%;
}

.carousel-sheet {
  background: transparent;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-container {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.carousel-image {
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
  transition: transform 0.3s ease;
}

.carousel-image:hover {
  transform: scale(1.01);
}

/* Vuetify carousel dots 스타일 수정 */
:deep(.v-carousel__controls) {
  background: transparent;
  margin-bottom: 8px;
}

:deep(.v-btn--icon.v-btn--density-default) {
  width: 6px !important;
  height: 6px !important;
  margin: 0 3px !important;
  padding: 0 !important;
}

:deep(.v-btn--icon.v-btn--density-default .v-btn__overlay) {
  background: #666;
  opacity: 0.3;
  border-radius: 50%;
}

:deep(.v-btn--icon.v-btn--density-default.v-btn--active .v-btn__overlay) {
  background: #666;
  opacity: 0.8;
}

:deep(.v-carousel__controls__item) {
  margin: 0 2px !important;
}

:deep(.v-btn--icon .v-btn__content) {
  display: none !important;
}

:deep(.v-btn--icon) {
  background-color: #666 !important;
  opacity: 0.3;
  border-radius: 50%;
}

:deep(.v-btn--icon.v-btn--active) {
  opacity: 0.8 !important;
}
</style>