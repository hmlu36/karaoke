<template>
  <div>
    <ul>
      <li v-for="(song, index) in queue" :key="index">
        <span>{{ song.title }}</span>
        <button @click="deleteSong(index)">刪除</button>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'QueueList',
  props: ['queue'],
  methods: {
    deleteSong(index) {
      this.$emit('delete-song', index);
    }
  }
};
</script>

<style scoped>
h2 {
  margin-top: 20px;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px;
  margin-bottom: 5px;
  /* Default light theme styles */
  background-color: #f0f0f0;
  color: #2c3e50;
}

/* Dark theme styles */
[data-theme='dark'] li {
  background-color: #3a3a3a;
  color: #e0e0e0;
}

button {
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 2px 5px;
  cursor: pointer;
}

[data-theme='dark'] button {
  background-color: #ff7f7f;
}
</style>
