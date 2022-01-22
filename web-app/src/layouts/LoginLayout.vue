<template>
  <div class="d-flex flex-column flex-root">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'LoginLayout',
}
</script>

<style lang="scss" scoped>
@import "../assets/styles/login/login-2.css";

.flex-column{
  height: 100vh;
}
</style>
