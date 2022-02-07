<template>
<v-card>
    <v-card-title class="blue-grey darken-3 white--text text-center">
      Players
      <v-spacer></v-spacer>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
  <v-data-table 
    v-model="selected"
    :headers="headers"
    :items="players"
    :search="search"
    item-key="id"
    show-select
    class="blue-grey darken-2 white--text text-center"
    @input="$emit('pass', selected)"
  >
  </v-data-table>
  </v-card>
</template>

<script>
  export default {
    name: 'Players',
    props: ['teamName'],
    data() {
      return {
        players: [],
        search: '',
        singleSelect: false,
        selected: [],
        expanded: [],
        //team: 'KKS LECH 1',
        headers: [
            {
              text: 'Name',
              align: 'start',
              sortable: false,
              value: 'name',
            },
            { text: 'Surname', value: 'surname' },
            { text: 'Role', value: 'role'},
            //{ text: 'Id', value: 'id'}
        ]
      }
    },
    mounted() {
        this.getPlayers();
    },
    methods: {
      async getPlayers(){
        //const res = await fetch('http://localhost:5000/api/users/q?team=' + this.teamName)
        const res = await fetch('api/users/q?team=' + this.teamName)
        const data = await res.json()
        const players = []
        for (var i = 0; i < data.length; i++) {
          const obj = {
            name: data[i].first_name,
            surname: data[i].last_name,
            role: data[i].roles[0].name,
            id: data[i].id
          }
          console.log(obj)
          players.push(obj)
        }

        this.players = players
      },
    }
  }
</script>