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
}
</style>
