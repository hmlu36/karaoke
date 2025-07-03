<template>
  <div class="video-container">
    <iframe
      v-if="videoUrl"
      :src="videoUrl"
      frameborder="0"
      allow="autoplay; encrypted-media"
      allowfullscreen
    ></iframe>
  </div>
</template>

<script>
export default {
  name: 'VideoPlayer',
  props: ['currentSong'],
  computed: {
    videoUrl() {
      if (this.currentSong) {
        return `https://www.youtube.com/embed/${this.currentSong.id}?autoplay=1`;
      }
      return '';
    }
  }
};
</script>

<style scoped>
.video-container {
  width: 100%;
  height: 100%;
  background: #000;
}

.video-container iframe {
  width: 100%;
  height: 100%;
}
</style>
