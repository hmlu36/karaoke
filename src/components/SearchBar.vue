<template>
  <div>
    <input
      type="text"
      placeholder="搜尋歌曲..."
      :value="searchQuery"
      @input="$emit('search', $event.target.value)"
    />
  </div>
</template>

<script>
export default {
  name: 'SearchBar',
  props: ['searchQuery']
};
</script>

<style scoped>
input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  /* Default light theme styles */
  background-color: #ffffff;
  color: #2c3e50;
  border: 1px solid #ccc;
}

/* Dark theme styles */
[data-theme='dark'] input {
  background-color: #2d2d2d;
  color: #e0e0e0;
  border-color: #555;
}
</style>
