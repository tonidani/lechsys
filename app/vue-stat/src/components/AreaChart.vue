<template>
  <div> 
      <h1>Area Chart</h1>
      <area-chart :data="AreaData"></area-chart>
  </div>
</template>

<script>
export default {
    data() { 
        return { 
            AreaData: [ 
                {name: 'Idk', data: {'2021-11-01': 2, '2021-11-02': 4,'2021-11-03 ': 7,'2021-11-04 ': 1,'2021-11-05 ': 5}},
                {name: 'Idk', data: {'2021-11-01': 9,'2021-11-02 ': 7,'2021-11-03 ': 8,'2021-11-04 ': 0.5,'2021-11-05 ': 9}},
            ]
       
        }
    }

}
</script>

<style>


</style>