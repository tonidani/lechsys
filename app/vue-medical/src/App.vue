<template>
  <v-app>
    <v-content>
       <v-container class="mb-1">
          <v-layout row wrap>
            <v-flex xs12 md3> 
              <time-line style="overflow-y: auto;height: 912px;" :get_data_table="get_data_table"></time-line>
            </v-flex>
            <v-flex xs12 md9>
                <player-table :data_table="data_table" :loading="loading"></player-table>
                <p>{{ $t('KinaseChart') }}</p>
                <column-chart :data="chart_column_data" :colors="['#455A64']" ></column-chart>
            </v-flex>
          </v-layout>
      </v-container>
   </v-content>
  </v-app>
</template>

<script>

import PlayerTable from "./components/PlayerTable.vue";
import TimeLine from "./components/TimeLine.vue";

export default {
  name: 'App',
  data(){ 
    return { 
      title: "Statistic Page", 
      loading: true,
      chart_bar_data: [],
      chart_column_data2: [],
      chart_column_data: [],

    }
  },
  components: {
    PlayerTable,
    TimeLine
  }, 
  methods: { 
    get_data_table(data_table,loading){ 
      this.data_table = data_table
      this.loading = loading
      this.getDataColumnChart()
    },
        getDataColumnChart(){        
                this.chart_column_data = {}
                for (let t=0; t<this.data_table.length; t++){ 
                    this.chart_column_data[String(this.data_table[t].date)] = this.data_table[t].value
                    
                }
        },
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #000000;
}
.grid-container {
  display: grid;
  grid-template-columns: 50% 50% ;
  background: #ffffff;
  
}

.grid-container > div {
  
  text-align: center;
  font-size: 20px;
 
}

.item1 {
  grid-column: 1 / span 2;
  text-align: center;
  
  
}
</style>
