<template>
  <div class="video-container" ref="container"></div>
</template>

<script>
export default {
  name: "VideoPlayer",
  props: {
    currentSong: Object, // { id: 'xxxx' }
    // 新增一個事件，通知父層切換下一首
    onEnded: Function
  },
  data() {
    return {
      player: null,
      ytApiLoaded: false,
    };
  },
  watch: {
    currentSong: {
      handler(newSong) {
        if (this.player && newSong) {
          this.player.loadVideoById(newSong.id);
        }
      },
      immediate: true,
    },
  },
  mounted() {
    if (window.YT && window.YT.Player) {
      this.createPlayer();
    } else {
      // 動態載入 YouTube IFrame API
      const tag = document.createElement('script');
      tag.src = "https://www.youtube.com/iframe_api";
      document.body.appendChild(tag);
      window.onYouTubeIframeAPIReady = this.createPlayer;
    }
  },
  beforeUnmount() {
    if (this.player) {
      this.player.destroy();
    }
  },
  methods: {
    createPlayer() {
      this.player = new window.YT.Player(this.$refs.container, {
        width: '100%',
        height: '100%',
        videoId: this.currentSong ? this.currentSong.id : '',
        playerVars: {
          autoplay: 1,
        },
        events: {
          onStateChange: this.onPlayerStateChange,
        },
      });
    },
    onPlayerStateChange(event) {
      // 0 代表播放結束
      if (event.data === window.YT.PlayerState.ENDED) {
          this.$emit('song-ended');
        }
    }
  }
}
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
