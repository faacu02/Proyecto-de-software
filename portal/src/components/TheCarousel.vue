<template>
  <div class="relative w-full max-w-3xl mx-auto overflow-hidden">
    <div
      class="flex transition-transform duration-500"
      :style="{ transform: `translateX(-${currentIndex * 100}%)` }"
    >
      <div v-for="(item, index) in items" :key="index" class="w-full flex-shrink-0">
        <img :src="item" alt="Slide image" class="w-full h-80 object-fit" />
      </div>
    </div>
    <button
      @click="prev"
      class="absolute top-1/2 left-2 transform -translate-y-1/2 bg-gray-700 text-white p-2 rounded-full"
    >
      ‹
    </button>
    <button
      @click="next"
      class="absolute top-1/2 right-2 transform -translate-y-1/2 bg-gray-700 text-white p-2 rounded-full"
    >
      ›
    </button>
    <div class="flex justify-center space-x-2 mt-4">
      <span
        v-for="(item, index) in items"
        :key="index"
        @click="setCurrentIndex(index)"
        class="w-3 h-3 bg-gray-400 rounded-full"
        :class="{ 'bg-gray-800': currentIndex === index }"
      ></span>
    </div>
  </div>
</template>

<script>
import img1 from '@/assets/cedica_img1.jpeg'
import img2 from '@/assets/cedica_img2.jpeg'
import img3 from '@/assets/cedica_img3.jpeg'
export default {
  data() {
    return {
      currentIndex: 0,
      items: [img1, img2, img3],
    }
  },
  methods: {
    next() {
      this.currentIndex = (this.currentIndex + 1) % this.items.length
    },
    prev() {
      this.currentIndex = (this.currentIndex - 1 + this.items.length) % this.items.length
    },
    setCurrentIndex(index) {
      this.currentIndex = index
    },
  },
}
</script>
