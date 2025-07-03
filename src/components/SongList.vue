<template>
  <ul>
    <li v-for="song in songs" :key="song.id">
      <span>{{ song.title }} - {{ song.artist }}</span>
      <button @click="addSong(song)" class="add-button" title="點歌">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
      </button>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'SongList',
  props: ['songs'],
  methods: {
    addSong(song) {
      this.$emit('add-song', song);
    }
  }
};
</script>

<style scoped>
ul {
  list-style: none;
  padding: 0;
}
li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ccc;
  /* Default light theme styles */
  background-color: #ffffff;
  color: #2c3e50;
}

/* Dark theme styles */
[data-theme='dark'] li {
  background-color: #2d2d2d;
  color: #e0e0e0;
  border-color: #555;
}

span {
  flex-grow: 1;
  margin-right: 10px;
  /* Default light theme styles */
  color: #2c3e50;
}

/* Dark theme styles */
[data-theme='dark'] span {
  color: #e0e0e0;
}
.add-button {
  background: none;
  border: none;
  color: #2c3e50;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
}

[data-theme='dark'] .add-button {
  color: white; /* White color for add icon in dark mode */
}
.add-button:hover {
  color: #66ffb3; /* Brighter hover color */
}

[data-theme='dark'] .add-button:hover {
  color: #90ee90; /* Even brighter hover color in dark mode */
}
.add-button svg {
  width: 18px;
  height: 18px;
}
</style>
