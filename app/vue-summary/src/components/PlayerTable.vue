<template>
  <v-app>
    <v-main>
      <v-container>
        <p>Player Table</p>
        <v-row>
          <v-col md="6">
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
            <v-col>
                <v-data-table
                :headers="headers"
                :items="data_table"
                :items-per-page="14"
                :search="search"
                height ="78vh"
                dark
                loading = {{loading}}
                loading-text="Chose your data ..."
                class="blue-grey darken-2 white--text text-center"
                >
            </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
    props: 
      ["data_table",
      "loading"]
    ,
    data: () => ({
        search:"",
        headers:[
            {text: "Date", value:"date"},
            {text: "Acceleration", value:"acceleration"},
            {text: "Deceleration", value:"deceleration"},
            {text: "Field time", value:"field_time"},
            {text: "Hsr", value:"hsr"},
            {text: "m per min", value:"meterage_per_minute"},
            {text: "Running", value:"running"},
            {text: "Sprint", value:"sprint"},
            {text: "Total distance", value:"total_distance"},
            {text: "Total player load", value:"total_player_load"},
            
        ] , 
        loading: true

    })

}
</script>

<style>
</style>