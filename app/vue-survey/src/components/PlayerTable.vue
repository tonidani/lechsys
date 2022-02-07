<template>
  <v-app>
    <v-main>
      <v-container>
        <p>{{ $t('PlayerTable') }}</p>
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
                loading-text="Wait for data ..."
                class="blue-grey darken-2 white--text text-center"
                ></v-data-table>
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
    mounted(){ 
      this.ll()
    },
    methods: {
      async ll(){ 
        let res4 = await fetch('/language')
        let data4 = await res4.text()

        if (data4 =='pl'){ 
          this.headers = [
            {text: "Data", value:"date"},
            {text: "Energia", value:"energy"},
            {text: "Zmęczenie", value:"fatigue"},
            {text: "Nastrój", value:"mood"},
            {text: "Ból mięśni", value:"muscle_soreness"},
            {text: "Jakość snu", value:"sleep_quality"},
            {text: "Rpe", value:"rpe"}
        ]
        } else { 
          this.headers = [
            {text: "Date", value:"date"},
            {text: "Energy", value:"energy"},
            {text: "Fatigue", value:"fatigue"},
            {text: "Mood", value:"mood"},
            {text: "Muscle soreness", value:"muscle_soreness"},
            {text: "Sleep quality", value:"sleep_quality"},
            {text: "Rpe", value:"rpe"}
        ]
        }
      }
    },
    data: () => ({
        search:"",
        headers:[
            {text: "Date", value:"date"},
            {text: "Energy", value:"energy"},
            {text: "Fatigue", value:"fatigue"},
            {text: "Mood", value:"mood"},
            {text: "Muscle soreness", value:"muscle_soreness"},
            {text: "Sleep quality", value:"sleep_quality"},
            {text: "Rpe", value:"rpe"}
        ] , 
        loading: true

    })

}
</script>

<style>
</style>