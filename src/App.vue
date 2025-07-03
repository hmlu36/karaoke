<template>
  <div id="app">
    <header>
      <h1>卡拉OK小幫手</h1>
    </header>
    <div class="container">
      <div class="player-section">
        <VideoPlayer :currentSong="currentSong" @ended="playNext" />
      </div>
      <div class="sidebar-section">
        <div class="queue-section">
          <div class="queue-header">
            <h2>待播清單</h2>
            <button @click="playNext" class="next-button" title="播放下一首">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 4 15 12 5 20 5 4"></polygon><line x1="19" y1="5" x2="19" y2="19"></line></svg>
            </button>
          </div>
          <QueueList :queue="queue" @delete-song="handleDeleteSong" />
        </div>
        <div class="search-section">
          <SearchBar @search="handleSearch" />
          <SongList :songs="filteredSongs" @add-song="addToQueue" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SearchBar from './components/SearchBar.vue';
import SongList from './components/SongList.vue';
import QueueList from './components/QueueList.vue';
import VideoPlayer from './components/VideoPlayer.vue';
import songs from './data/songs.js';

export default {
  name: 'App',
  components: {
    SearchBar,
    SongList,
    QueueList,
    VideoPlayer
  },
  data() {
    return {
      songs: songs,
      searchQuery: '',
      queue: [],
      currentSong: null
    };
  },
  computed: {
    filteredSongs() {
      if (!this.searchQuery) {
        return this.songs;
      }
      return this.songs.filter(song =>
        song.title.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  methods: {
    handleSearch(query) {
      this.searchQuery = query;
    },
    addToQueue(song) {
      this.queue.push(song);
      if (!this.currentSong) {
        this.playNext();
      }
    },
    handleDeleteSong(index) {
      this.queue.splice(index, 1);
    },
    playNext() {
      if (this.queue.length > 0) {
        this.currentSong = this.queue.shift();
      } else {
        this.currentSong = null;
      }
    }
  },
  mounted() {
    this.playNext();
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

header {
  text-align: center;
  margin-bottom: 20px;
}

.container {
  display: flex;
  gap: 20px;
  height: calc(100vh - 100px); /* Adjust height based on header */
}

.player-section {
  flex: 4; /* Takes up 80% of the space */
}

.sidebar-section {
  flex: 1; /* Takes up 20% of the space */
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.queue-section, .search-section {
  border: 1px solid #ccc;
  padding: 10px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.queue-section {
  flex-basis: 40%; /* Takes up 40% of the sidebar height */
}

.queue-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.queue-header h2 {
  margin: 0;
}

.next-button {
  background: none;
  border: none;
  color: #2c3e50;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.next-button:hover {
  color: #ff4d4d;
}

.next-button svg {
  width: 20px;
  height: 20px;
}

.search-section {
  flex-basis: 60%; /* Takes up 60% of the sidebar height */
}
</style>
