<template>
  <div class="home">
    <Dashboard/>
  </div>
</template>

<script>
// @ is an alias to /src
import Dashboard from '@/components/Dashboard/Dashboard.vue'

export default {
  name: 'Home',
  components: {
    Dashboard
  },
}
</script>
