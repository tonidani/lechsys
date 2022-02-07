<template>
<v-card>
  <!-- wyszukiwarka
    <v-card-title>
      Teams
      <v-spacer></v-spacer>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
      
    </v-card-title>
    -->
  <v-data-table
    v-model="selected"
    :headers="headers"
    :items="teams"
    :search="search"
    :expanded.sync="expanded"
    show-expand
    item-key="name"
    class="elevation-1"
  >
  <template v-slot:expanded-item="{ headers, item }">
      <td :colspan="headers.length">
        <Players :teamName="item.name" @pass="update" @input="$emit('pass2', parentvariable)"/>
      </td>
    </template>
  
  </v-data-table>
  </v-card>
</template>

<script>
import Players from './Players.vue'

  export default {
    name: 'Teams',
    components: {
        Players,
    },
    data() {
      return {
        parentvariable: '',
        teams: [],
        teamsHeaders: [],
        search: '',
        singleSelect: false,
        //selected: [],
        expanded: [],
        headers: [
            {
              text: 'Name',
              align: 'start',
              sortable: false,
              value: 'name',
            },
            //{ text: '', value: 'data-table-expand' }
        ]
      }
    },
    mounted() {
        this.getTeams();
    },
    methods: {
      async getTeams(){
        //const res = await fetch('http://localhost:5000/api/teams')
        const res = await fetch('api/teams')
        const data = await res.json()
        this.teams = data
        this.teamsHeaders = Object.keys(data[0])
      },
      update(variable2) {
        this.parentvariable = variable2
        this.$emit('pass', this.parentvariable)
      },
    
    }
  }
</script>