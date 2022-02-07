<template>
  <div>
      <h1>Time Line Chart</h1> 
      <timeline :data="[['Washington', '1789-04-29', '1797-03-03'], ['Adams', '1797-03-03', '1801-03-03']]" class="time-back"></timeline>
  </div>
</template>

<script>
export default {

}
</script>

<style>
.time-back{ 
  background: #464B6B;
}
</style>