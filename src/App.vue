<template>
  <div id="app">
    <div class="container">
      <div class="player-section">
        <VideoPlayer :currentSong="currentSong" @song-ended="playNext" />
      </div>
      <div class="sidebar-section">
        <div class="queue-section">
          <div class="queue-header">
            <h2>待播清單</h2>
            <div class="header-buttons">
              <button @click="toggleTheme" class="theme-toggle-button" title="切換深淺色模式">
                <svg v-if="theme === 'dark'" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
              </button>
              <button @click="playNext" class="next-button" title="播放下一首">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 4 15 12 5 20 5 4"></polygon><line x1="19" y1="5" x2="19" y2="19"></line></svg>
              </button>
            </div>
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
      currentSong: null,
      theme: 'light'
    };
  },
  computed: {
    filteredSongs() {
      if (!this.searchQuery) {
        return this.songs;
      }
      return this.songs.filter(song =>
        song.title.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        song.artist.toLowerCase().includes(this.searchQuery.toLowerCase())
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
    playNext() {
      if (this.queue.length > 0) {
        this.currentSong = this.queue.shift();
      } else {
        this.currentSong = null;
      }
    },
    handleDeleteSong(index) {
      this.queue.splice(index, 1);
    },
    toggleTheme() {
      this.theme = this.theme === 'dark' ? 'light' : 'dark';
    }
  },
  mounted() {
    document.documentElement.setAttribute('data-theme', this.theme);
    this.playNext();
  },
  watch: {
    theme(newTheme) {
      document.documentElement.setAttribute('data-theme', newTheme);
    }
  }
};
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--primary-text);
  background-color: var(--primary-bg);
  position: relative;
  height: 100vh;
}

.theme-toggle-button {
  background: none;
  border: 2px solid var(--secondary-text); /* Thicker border */
  color: var(--primary-text);
  cursor: pointer;
  padding: 10px 15px; /* Increased padding */
  border-radius: 8px; /* Larger border-radius */
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5em; /* Larger icon/text */
}

.theme-toggle-button:hover {
  color: var(--accent-color); /* Use accent color for hover */
}

.container {
  display: flex;
  gap: 30px; /* Increased gap */
  height: 100%;
  padding: 20px; /* Added padding */
}

.player-section {
  flex: 4;
}

.sidebar-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 30px; /* Increased gap */
}

.queue-section,
.search-section {
  border: 2px solid var(--secondary-text); /* Thicker border */
  padding: 20px; /* Increased padding */
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  border-radius: 10px; /* Larger border-radius */
}

.queue-section {
  flex-basis: 40%;
}

.search-section {
  flex-basis: 60%;
}

.queue-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px; /* Increased margin */
}

.queue-header h2 {
  margin: 0;
  font-size: 2em; /* Larger heading */
}

.header-buttons {
  display: flex;
  gap: 10px;
}

.next-button {
  background: none;
  border: 2px solid var(--secondary-text); /* Thicker border */
  color: var(--primary-text);
  cursor: pointer;
  padding: 10px 15px; /* Increased padding */
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px; /* Larger border-radius */
}

.next-button:hover {
  color: var(--accent-color); /* Use accent color for hover */
}

.next-button svg {
  width: 32px; /* Larger icon */
  height: 32px; /* Larger icon */
}

.search-section input {
  background-color: var(--secondary-bg);
  color: var(--primary-text);
  padding: 12px; /* Increased padding */
  border: 1px solid var(--secondary-text);
  border-radius: 5px;
  font-size: 1.2em; /* Larger font size */
}

/* Dark theme styles */
[data-theme='dark'] {
  color: var(--primary-text);
  background-color: var(--primary-bg);
}


[data-theme='dark'] .search-section input {
  background-color: var(--secondary-bg);
  color: var(--primary-text);
}

[data-theme='dark'] .theme-toggle-button {
  border-color: var(--secondary-text);
  color: var(--primary-text);
}

[data-theme='dark'] .theme-toggle-button:hover {
  color: var(--accent-color);
}

[data-theme='dark'] .queue-section,
[data-theme='dark'] .search-section {
  border-color: var(--secondary-text);
}

[data-theme='dark'] .queue-header h2 {
  color: var(--primary-text);
}

[data-theme='dark'] .next-button {
  color: var(--primary-text);
  border-color: var(--secondary-text);
}

[data-theme='dark'] .next-button:hover {
  color: var(--accent-color);
}
</style>
