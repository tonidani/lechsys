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
                <p>{{ $t('TotalPlayerLoadChart') }}</p>
                <column-chart :data="chart_column_data" :colors="['#455A64']" ></column-chart>
                <p>{{ $t('Acceleration+DecelerationChart') }}</p>
                <bar-chart :data="chart_bar_data" :colors="['#455A64','#00838F']" :stacked="true"></bar-chart>
                <p>{{ $t('TotalDistaneChart') }}</p>
                <column-chart :data="chart_column_data2" :colors="['#455A64','#00838F','#D84315']" :stacked="true"></column-chart>
            </v-flex>
          </v-layout>
      </v-container>
   </v-content>
  </v-app>
</template>

<script>

//import PieChart from "./components/PieChart.vue";
//import LineChart from "./components/LineChart.vue";
//import TimeLineChart from "./components/TimeLineChart.vue";
//import AreaChart from "./components/AreaChart.vue";
import PlayerTable from "./components/PlayerTable.vue";
//import TrainingTable from "./components/TrainingTable.vue";
import TimeLine from "./components/TimeLine.vue";

export default {
  name: 'App',
  data(){ 
    return { 
      title: "Statistic Page", 
      loading: true,
      chart_bar_data: [],
      chart_column_data2: [],
      chart_column_data: []
    }
  },
  components: {
   // PieChart,
   // TimeLineChart,
   // AreaChart,
    PlayerTable,
   // TrainingTable,
    TimeLine
  }, 
  methods: { 
    get_data_table(data_table,loading){ 
      this.data_table = data_table
      this.loading = loading
      this.getDataBarChart()
      this.getDataColumnChart()
      this.getDataColumnChart2()
    },
          getDataBarChart(){

                  this.chart_bar_data = []
                  this.chart_bar_data[0] = {name:"Acceleration",data:[]}
                  for (let t=0; t<this.data_table.length; t++){ 
                      
                      this.chart_bar_data[0].data[t]=[String(this.data_table[t].date),(this.data_table[t].acceleration)]
                      
                  }
                  this.chart_bar_data[1] = {name:"Deceleration",data:[]}
                  for (let t=0; t<this.data_table.length; t++){ 
                      
                      this.chart_bar_data[1].data[t]=[String(this.data_table[t].date),(this.data_table[t].deceleration)]
                      
            }
        },
        getDataColumnChart(){        
                this.chart_column_data = {}
                for (let t=0; t<this.data_table.length; t++){ 
                    this.chart_column_data[String(this.data_table[t].date)] = this.data_table[t].total_player_load
                    
                }
        },
        getDataColumnChart2(){ 
            this.chart_column_data2= []
            this.chart_column_data2[0] = {name:"Total distance - Running and Sprint",data:[]}
            for (let t=0; t<this.data_table.length; t++){ 
                
                this.chart_column_data2[0].data[t]=[String(this.data_table[t].date),(this.data_table[t].total_distance - this.data_table[t].running - this.data_table[t].sprint)]
                
            }
            this.chart_column_data2[1] = {name:"Running",data:[]}
            for (let t=0; t<this.data_table.length; t++){ 
                
                this.chart_column_data2[1].data[t]=[String(this.data_table[t].date),(this.data_table[t].running)]
                
            }this.chart_column_data2[2] = {name:"Sprint",data:[]}
            for (let t=0; t<this.data_table.length; t++){ 
                
                this.chart_column_data2[2].data[t]=[String(this.data_table[t].date),(this.data_table[t].sprint)]
                
            }

        }
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
