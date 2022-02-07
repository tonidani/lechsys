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
            {text: "Kinaza", value:"value"},
        ]
        } else { 
          this.headers = [
            {text: "Date", value:"date"},
            {text: "Kinase", value:"value"},
        ]
        }
      }
    },
    data: () => ({
        search:"",
        headers:[
            {text: "Date", value:"date"},
            {text: "Kinase", value:"value"},
        ] , 
        loading: true

    })

}
</script>

<style>

</style>