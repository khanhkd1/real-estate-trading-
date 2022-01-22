<template>
  <div class="LayoutDeliveryBill">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'LayoutDeliveryBill',
}
</script>

<style lang="scss" scoped>
  .LayoutDeliveryBill {
    min-height: 100vh;
    overflow: auto;
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
    display: flex;
    justify-content: center;
    justify-content: center;
    background-color: white;
  }
</style>
