<template>
  <v-app>
    <v-content>
      <!--
      <v-row justify="space-between">
        <v-col cols="3">
          <time-line :get_data_table="get_data_table" :get_data_table2="get_data_table2"></time-line>
        </v-col>
        <v-col cols="9">
          
          <player-table :data_table="data_table" :loading="loading"></player-table>
          <p>Total Player Load Chart</p>
          <column-chart :data="chart_column_data" :colors="['#455A64']" ></column-chart>
          <p>Acceleration + Deceleration Chart</p>
          <bar-chart :data="chart_bar_data" :colors="['#455A64','#00838F']" :stacked="true"></bar-chart>
          <p>Total Distane Chart</p>
          <column-chart :data="chart_column_data2" :colors="['#455A64','#00838F','#D84315']" :stacked="true"></column-chart>
          <div id="chart">
            <apexchart type="line" height="350" :options="chartOptions" :series="series"></apexchart>
          </div>
          <div id="chart">
            <apexchart type="line" height="350" :options="chartOptions2" :series="series2"></apexchart>
          </div>
        </v-col>
          </v-row>
-->
         <v-container class="mb-1">
          <v-layout row wrap>
            <v-flex xs12 md3> 
              <time-line style="overflow-y: auto;height: 912px;" :get_data_table="get_data_table" :get_data_table2="get_data_table2"></time-line>
            </v-flex>
            <v-flex xs12 md9 style="z-index: 0">
                <div id="chart">
                  <p>{{ $t('TreningEff') }}</p>
                  <apexchart  type="line" height="350" :options="chartOptions" :series="series"></apexchart>
                </div>
                <div id="chart" style="z-index: 0">
                  <p>{{ $t('Acwr') }}</p>
                  <apexchart  type="line" height="350" :options="chartOptions2" :series="series2"></apexchart>
                </div>
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
//import PlayerTable from "./components/PlayerTable.vue";
//import TrainingTable from "./components/TrainingTable.vue";
import TimeLine from "./components/TimeLine.vue";

export default {
  name: 'App',
  data(){ 
    return { 
      title: "Statistic Page", 
      loading: true,
       series: [{
            name: 'Traning Efficiency',
            type: 'column',
            data: []
          }, {
            name: 'Average Tei',
            type: 'line',
            data: []
      }],
      chartOptions: {
        chart: {
          height: 350,
          type: 'line',
        },
        stroke: {
          width: [0, 4]
        },
        title: {
          text: 'Traning Efficiency - Time'
        },
        dataLabels: {
          enabled: true,
          enabledOnSeries: [1]
        },
        labels: ["2021-05-23", "2021-05-24"],
        xaxis: {
          type: 'datetime'
        },
        yaxis: [{
          title: {
            text: 'Traning Efficiency',
          },
        
        }, {
          opposite: true,
          title: {
            text: 'Average Tei'
          }
        }]
      },

      series2: [{
            name: 'Acwr',
            type: 'column',
            data: []
          }, {
            name: 'Acwr',
            type: 'line',
            data: []
      }],
      chartOptions2: {
        chart: {
          height: 350,
          type: 'line',
        },
        stroke: {
          width: [0, 4]
        },
        title: {
          text: 'Acwr - Time'
        },
        dataLabels: {
          enabled: true,
          enabledOnSeries: [1]
        },
        labels: ["2021-05-23", "2021-05-24"],
        xaxis: {
          type: 'datetime'
        },
        yaxis: [{
          title: {
            text: 'Acwr',
          },
        
        }, {
          opposite: true,
          title: {
            text: 'Acwr'
          }
        }]
      },
    }
  },
  components: {
   // PieChart,
   // TimeLineChart,
   // AreaChart,
   // PlayerTable,
   // TrainingTable,
    TimeLine
  }, 
  methods: { 
    get_data_table(data_table,loading){ 
      this.data_table = data_table
      this.loading = loading
      this.getDataSummaryDate()

    },
    get_data_table2(data_table,loading,month_id){ 
      this.data_table = data_table
      this.loading = loading
      this.month_id = month_id
      this.getDataSummaryDateMonth()
     
    },
         
        getDataSummaryDate(){ 
          let dateE = [],surveyY = [],sum = 0,acwr=[],sum2 = 0, sum3 = 0
          for (let t=0; t<this.data_table.length; t++){ 
                    dateE.push(this.data_table[t].date)
                    sum = (parseFloat(this.data_table[t].rpe) + parseFloat(this.data_table[t].energy) + parseFloat(this.data_table[t].fatigue) + parseFloat(this.data_table[t].mood) + parseFloat(this.data_table[t].muscle_soreness) + parseFloat(this.data_table[t].sleep_quality))
                    if (sum == 0){ 
                      surveyY.push(parseFloat(this.data_table[t].total_player_load))
                  } else { 
                    surveyY.push(parseFloat(this.data_table[t].total_player_load)/sum)
                  }
                  sum2 = sum + parseFloat(this.data_table[t].total_player_load)
                  


                   if (sum2 == 0){ 
                      acwr.push(sum2)
                  } else { 
                    
                    acwr.push(sum2)
                  }     
                }

                   for (let aa=0; aa<acwr.length; aa++){ 
                    sum3 += acwr[aa]
                    
                  }
                  sum3 = 1.1 * (sum3/ acwr.length)

                  for (let aa=0; aa<acwr.length; aa++){ 
                    
                    acwr[aa] = sum3 / acwr[aa]
                  }

         
                this.series = [{
                  data: surveyY
                }, {
                  data: surveyY
                }]

                this.chartOptions = {
                  labels: dateE
                }

                
                this.series2 = [{
                  data: acwr
                }, {
                  data: acwr
                }]

                this.chartOptions2 = {
                  labels: dateE
                }


                
        },
        getDataSummaryDateMonth(){
          let monthData = []

          for (let j=0; j<this.data_table.length; j++){
            for (let jj=0; jj<this.data_table[j].length; jj++){
              if (this.data_table[j][jj].date.slice(5,7) == this.month_id + 1){
                monthData.push(this.data_table[j][jj])
              }
            }
          }

          let dateE = [],surveyY = [],sum = 0,acwr=[],sum2 = 0, sum3 = 0
          for (let t=0; t<monthData.length; t++){ 
                    dateE.push(monthData[t].date)
                    sum = (parseFloat(monthData[t].rpe) + parseFloat(monthData[t].energy) + parseFloat(monthData[t].fatigue) + parseFloat(monthData[t].mood) + parseFloat(monthData[t].muscle_soreness) + parseFloat(monthData[t].sleep_quality))
                    if (sum == 0){ 
                      surveyY.push(parseFloat(monthData[t].total_player_load))
                  } else { 
                    surveyY.push(parseFloat(monthData[t].total_player_load)/sum)
                  }
                  sum2 = sum + parseFloat(monthData[t].total_player_load)
                  


                   if (sum2 == 0){ 
                      acwr.push(sum2)
                  } else { 
                    
                    acwr.push(sum2)
                  }     
                }

                   for (let aa=0; aa<acwr.length; aa++){ 
                    sum3 += acwr[aa]
                    
                  }
                  sum3 = 1.1 * (sum3/ acwr.length)

                  for (let aa=0; aa<acwr.length; aa++){ 
                    
                    acwr[aa] = sum3 / acwr[aa]
                  }

         
                this.series = [{
                  data: surveyY
                }, {
                  data: surveyY
                }]

                this.chartOptions = {
                  labels: dateE
                }

                
                this.series2 = [{
                  data: acwr
                }, {
                  data: acwr
                }]

                this.chartOptions2 = {
                  labels: dateE
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
