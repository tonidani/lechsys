<template>
  <v-app>
    <v-content >
      <!--
      <v-row justify="space-between">
        <v-col xs12 md3 lg3>
          <time-line :get_data_table="get_data_table"></time-line>
        </v-col>
        <v-col xs12 md9 lg9>
          <player-table :data_table="data_table" :loading="loading"></player-table>
          <p>Wellness Chart</p>
          <column-chart :data="chart_column_data2" :colors="['#455A64']" ></column-chart>
          <p>Rpe Chart</p>
          <column-chart :data="chart_column_data" :colors="['#D84315']" ></column-chart>
        </v-col>

      </v-row>
      -->
      <v-container class="mb-1">
      <v-layout row wrap>
        <v-flex xs12 md3> 
          <time-line style="overflow-y: auto;height: 912px;" :get_data_table="get_data_table"></time-line>
        </v-flex>
        <v-flex xs12 md9>
          <player-table :data_table="data_table" :loading="loading"></player-table>
          <p>{{ $t('WellnessChart') }}</p>
          <column-chart :data="chart_column_data2" :colors="['#455A64']" ></column-chart>
          <p>{{ $t('RpeChart') }}</p>
          <column-chart :data="chart_column_data" :colors="['#D84315']" ></column-chart>
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
      chart_column_data: []
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
      this.getDataColumnChart2()
    },
        getDataColumnChart(){        
                this.chart_column_data = {}
                for (let t=0; t<this.data_table.length; t++){ 
                    this.chart_column_data[String(this.data_table[t].date)] = this.data_table[t].rpe
                    
                }
        },
        getDataColumnChart2(){        
                this.chart_column_data2 = {}
                let summ = 0 
                for (let t=0; t<this.data_table.length; t++){ 
                  summ = parseInt(this.data_table[t].energy) + parseInt(this.data_table[t].fatigue) + parseInt(this.data_table[t].mood) + parseInt(this.data_table[t].muscle_soreness) + parseInt(this.data_table[t].sleep_quality)
                    this.chart_column_data2[String(this.data_table[t].date)] = summ
                    
                }
                
        },
  }
}
</script>

<style>

</style>

<i18n>
{
  "en": {
    "hello": "Hello i18n in SFC!"
  }
}
</i18n>
