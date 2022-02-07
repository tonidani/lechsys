<template>
    <div>
        <p>Number of completed questionnaires</p>
        <pie-chart :data="chartOneData" :colors="['#b00', '#686']" :donut="true" class="back-p"></pie-chart>
    </div>
</template>

<script>
export default {
    data() { 
        return { 
            chartOneData: {
                "Completed" : 79, 
                "No Completed" : 21 
            }
        }
    }
}
</script>

<style>
.back-p{ 
    background: linear-gradient(to bottom, #33ccff 0%, #ff99cc 100%);
    border-style: solid;
    border-color: black;
}

</style>