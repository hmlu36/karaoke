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
}
span {
  flex-grow: 1;
  margin-right: 10px;
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
.add-button:hover {
  color: #42b983;
}
.add-button svg {
  width: 18px;
  height: 18px;
}
</style>
