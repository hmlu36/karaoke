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
          <div class="search-bar-wrapper" style="justify-content: space-between;">
            <SearchBar @search="handleSearch" />
            <button @click="loadSongsFromPublicUrl" class="refresh-button" title="重新整理歌單">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"></polyline><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path></svg>
            </button>
          </div>
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

const ORIGINAL_SHEET_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTW4s1j9tfMCEq54uTO2ubmmv7GQxgfAKiBwnF-XYTdBPsP6m_W1YHKxrrVKmGXBzXiaU3Dd5L0DtdF/pub?output=csv';

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
      songs: [],
      searchQuery: '',
      queue: [],
      currentSong: null,
      theme: 'light',
    };
  },
  computed: {
    filteredSongs() {
      if (!this.searchQuery) {
        return this.songs;
      }
      return this.songs.filter(song =>
        (song.title && song.title.toLowerCase().includes(this.searchQuery.toLowerCase())) ||
        (song.artist && song.artist.toLowerCase().includes(this.searchQuery.toLowerCase()))
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
    },
    async loadSongsFromPublicUrl() {
      try {
        // 加上時間戳來防止快取
        const noCacheUrl = `${ORIGINAL_SHEET_URL}&_=${new Date().getTime()}`;
        const proxyUrl = `https://api.allorigins.win/raw?url=${encodeURIComponent(noCacheUrl)}`;
        
        const response = await fetch(proxyUrl);
        if (!response.ok) {
          throw new Error(`Network response was not ok: ${response.statusText}`);
        }
        const csvText = await response.text();
        this.parseCsvData(csvText);
      } catch (error) {
        console.error('Error fetching or parsing sheet data:', error);
      }
    },
    parseCsvData(csvText) {
      const lines = csvText.trim().split(/\r?\n/);
      if (lines.length < 2) {
        this.songs = [];
        return;
      }
      
      const header = lines[0].split(',').map(h => h.trim());
      const idIndex = header.indexOf('id');
      const titleIndex = header.indexOf('title');
      const artistIndex = header.indexOf('artist');

      if (idIndex === -1 || titleIndex === -1 || artistIndex === -1) {
        console.error("CSV header must contain 'id', 'title', and 'artist' columns.");
        return;
      }

      this.songs = lines.slice(1).map(line => {
        const columns = line.split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/);
        
        const id = columns[idIndex] ? columns[idIndex].trim().replace(/"/g, '') : '';
        const title = columns[titleIndex] ? columns[titleIndex].trim().replace(/"/g, '') : '';
        const artist = columns[artistIndex] ? columns[artistIndex].trim().replace(/"/g, '') : '';

        return { id, title, artist };
      }).filter(song => song.id);
    }
  },
  mounted() {
    document.documentElement.setAttribute('data-theme', this.theme);
    this.loadSongsFromPublicUrl();
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

.refresh-button,
.theme-toggle-button,
.next-button {
  background: none;
  border: 2px solid var(--secondary-text);
  color: var(--primary-text);
  cursor: pointer;
  padding: 10px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.refresh-button:hover,
.theme-toggle-button:hover,
.next-button:hover {
  color: var(--accent-color);
  border-color: var(--accent-color);
}

.refresh-button svg,
.theme-toggle-button svg,
.next-button svg {
  width: 24px;
  height: 24px;
}

.container {
  display: flex;
  gap: 30px;
  height: 100%;
  padding: 20px;
  @media (max-width: 768px) { /* 針對小螢幕 */
    flex-direction: column; /* 讓元素垂直排列 */
  }
}

.player-section {
  flex: 4;
}

.sidebar-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.queue-section,
.search-section {
  border: 2px solid var(--secondary-text);
  padding: 20px;
  overflow-y: auto;
  flex-direction: column;
  border-radius: 10px;
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
  margin-bottom: 15px;
}

.queue-header h2 {
  margin: 0;
  font-size: 2em;
}

.header-buttons {
  display: flex;
  gap: 10px;
}

.search-section input {
  background-color: var(--secondary-bg);
  color: var(--primary-text);
  padding: 12px;
  border: 1px solid var(--secondary-text);
  border-radius: 5px;
  font-size: 1.2em;
}

.search-bar-wrapper { /* 新增 */
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  justify-content: space-between; /* 新增 */
}

.search-bar-wrapper > input { /* 修改 */
  width: 80%;
}

.refresh-button {
  width: 20%;
  justify-content: center;
}
</style>
