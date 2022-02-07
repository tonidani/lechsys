<template>
<v-app> 
    <v-content
    style="z-index: 0">
   <v-card
    class="mx-auto text-center"
    max-width="550"
  >
    <v-card-title
      class="blue-grey darken-2 white--text text-center"
    >
    <div class="text-center">
       <v-row align="center"
      justify="center"
      class="ms-10">
          <v-col cols="auto">
               <v-btn @click="minus_year()"
                class="mx-2 pa-2"
                fab
                dark
                small
                color="black"
              >
                <v-icon dark>
                  mdi-minus
                </v-icon>
              </v-btn>
          </v-col>
           <v-col cols="auto" class="text-subtitle-2 text-center" >
             <v-card min-width="120px" >
             {{year_timeline}}
             </v-card>
          </v-col>
           <v-col cols="auto">
             <v-btn @click="plus_year()"
                class="mx-2"
                fab
                dark
                small
                color="black"
              >
                <v-icon dark>
                  mdi-plus
                </v-icon>
              </v-btn>
          </v-col>
        </v-row>
        <v-row align="center"
      justify="center"
      class="ms-10">
          <v-col cols="auto">
              <v-btn @click="minus_month()"
                class="mx-2"
                fab
                dark
                small
                color="black"
              >
                <v-icon dark>
                  mdi-minus
                </v-icon>
              </v-btn>
          </v-col>
           <v-col cols="auto" class="text-subtitle-2 text-center">
             <v-card min-width="120px" >
              {{month_timeline}}
             </v-card>
          </v-col>
           <v-col cols="auto">
              <v-btn @click="plus_month()"
                class="mx-2"
                fab
                dark
                small
                color="black"
              >
                <v-icon dark>
                  mdi-plus
                </v-icon>
              </v-btn>
          </v-col>
        </v-row>
    </div>
    <v-btn justify="center"  class="mt-2" block @click="get_data_table2(motoric[month_id],loading,month_id)">{{ $t('MonthData') }}</v-btn>
      <v-spacer></v-spacer>
    </v-card-title>
    <v-card-text class="py-0">


    <v-timeline
      class="witdh"
      dense
      clipped
    >
    
      <v-timeline-item v-for="event in show_month" :key="event.match_id"
        class="mb-4"
        :color="event.color"
        small
      >
        <v-row justify="space-between">
          <v-col cols="7">
           <p> {{event.description}} </p>
           <p> {{event.name}} </p>
           <p> {{event.start}} </p>

            
           
          </v-col>
          <v-col
            
            cols="5"
          >
            <div v-if="event.type_id==1">
              <v-btn @click="get_data_table(motoric[month_id][event.match_id],loading)">{{ $t('Data') }} </v-btn>
            </div>
            <div v-else-if="event.type_id!=1 && event.type_id!=2"> 
              <p> {{ $t('MatchDay') }} {{event.matchday_counter}} <p> 
            </div>
          </v-col>
        </v-row>

      </v-timeline-item>

    </v-timeline>
    
     </v-content>
</v-app>

</template>

<script>
export default {
   data: () => ({
       
        events: [],
        events_matches_league: [],
        motoric: [],
        events_months: [], 
        loading: false,
        month_id: "", 
        show_month: [],
        month_timeline: "", 
        year_timeline: "",
        year_now: "",
        year_months: "",
        main_table_main: "",
        motoric_all: "",
        lang: "en"
    }),
    mounted(){ 
      this.get_events();
    },
    props: {
      get_data_table:Function,
      get_data_table2:Function
    },
    methods: { 
       async get_events(){ 
         // pobieranie i obrabiane id zawodnika 
        let url = window.location.href 

        const re = /users\/\d+/ 
        const found = url.match(re);
        const found2 = found[0].match(/\d+/g)
        const player_id = found2[0]

       
        //pobieranie api i wstepna obrobka 

        let res = await fetch('/api/users/'+player_id+'/events')
        let data = await res.json()
        this.events = data

        let res2 = await fetch('/api/users/'+player_id+'/motoric')
        let data2 = await res2.json()

         let res3 = await fetch('/api/users/'+player_id+'/wellness')
        let data3 = await res3.json()

        let res4 = await fetch('/api/users/'+player_id+'/rpe')
        let data4 = await res4.json()

        let res5 = await fetch('/language')
        let data5 = await res5.text()
        this.$i18n.locale = data5
        this.lang = data5

        let calendarr = new Date()
        let YYYY = calendarr.getYear() + 1900
        let MM = calendarr.getMonth() + 1 
        if (MM != 12 || MM != 11 || MM !=10){ 
          MM = "0" + MM 
        }
        let DD = calendarr.getDate()
        if (DD == 1 || DD == 2 || DD == 3 || DD == 4 || DD == 5 || DD == 6 || DD == 7 || DD == 8 || DD == 9){ 
          DD = "0" + DD 
        }
        let DDDD = YYYY + "-" + MM + "-" + DD


         if (data.length == 0 && data2.length == 0 && data3.length ==0 && data4.length ==0){

          let dataa = {color : 'purple',description: 'No Data',details : 'No Data',end : DDDD,has_kinas: false,id : 1,latitude : null,longitude : null,name : 'Brak danych',start : DDDD,type_id : 2 }
          data.push(dataa)
          let dataa2 = {acceleration : 0,date : DDDD,deceleration : 0,energy : 0,event_id:1,fatigue : 0,
          field_time : 0, hsr : 0,id : 1,meterage_per_minute : 0,mood :0 , muscle_soreness : 0 ,rpe : 0,running : 0,sleep_quality : 0,
          sprint : 0,state : "TO-COMPLETE",total_distance : 0 ,total_player_load : 0  }
          data2.push(dataa2)
          let dataa3 = {date : DDDD,energy : 0,event_id : 4,fatigue : 0,id : 1,mood : 0,muscle_soreness : 0,rpe : 0,sleep_quality : 0,state : 'TO-COMPLETE'}
          data3.push(dataa3)
          let dataa4 = {date : DDDD,event_id : 1,id : 1,state :  'TO-COMPLETE',total_time :'00:00:00',value : 0  }
          data4.push(dataa4)
        }


        if (data.length > 0 && data2.length > 0 && data3.length > 0 && data4.length > 0){


        for (let jj=0; jj<data.length; jj++){ 
          data[jj].start = data[jj].start.slice(0,10)
          data[jj].end = data[jj].end.slice(0,10)
        }

        for(let da2=0; da2<data2.length; da2++){ 
          for (let da3=0; da3<data3.length; da3++){ 
            if(data2[da2].date == data3[da3].date){ 
              data2[da2]["rpe"] = data4[da3].value
              data2[da2]["energy"] = data3[da3].energy
              data2[da2]["fatigue"] = data3[da3].fatigue
              data2[da2]["mood"] = data3[da3].mood
              data2[da2]["muscle_soreness"] = data3[da3].muscle_soreness
              data2[da2]["sleep_quality"] = data3[da3].sleep_quality
            }
          }
        }

      //podzial na lata 
      //let last_event_year = data[0].end.slice(0,4)
      //let how_many_times = last_event_year - 2020 
      let table_year=[]
      let one_year =[]
      let main_table = []
      let main_motoric = []

      let calendar_data1 = new Date()
      let calendat_year1 = (calendar_data1.getYear() + 1900) - 2020 

      for (let ye=0; ye<=calendat_year1; ye++){ 
        for(let ddd=0; ddd<data.length; ddd++){ 
          if (data[ddd].end.slice(0,4) == 2020 + ye && data[ddd].type_id!= 5)
          one_year.push(data[ddd])
        }
        table_year.push(one_year)
        one_year=[]
      }

      
      for (let yee=0; yee<=calendat_year1; yee++){ 


      
       //podzial na miesiace 
       let months = [], month1=[], month2=[], month3=[] ,month4=[], month5=[], month6=[], month7=[], month8=[] ,month9=[], month10=[], month11= [], month12 =[]
        for (let d=0; d<table_year[yee].length; d++){ 
          if (table_year[yee][d].type_id!= 5 ){
              if (table_year[yee][d].end.slice(5,7) == "01"){ 
                month1.push(table_year[yee][d])
              } else if (table_year[yee][d].end.slice(5,7) == "02"){ 
                month2.push(table_year[yee][d])
              } else if (table_year[yee][d].end.slice(5,7) == "03"){ 
                month3.push(table_year[yee][d])
              } else if (table_year[yee][d].end.slice(5,7) == "04"){ 
                month4.push(table_year[yee][d])
              } else if (table_year[yee][d].end.slice(5,7) == "05"){ 
                month5.push(table_year[yee][d])
              } else if (table_year[yee][d].end.slice(5,7) == "06"){ 
                month6.push(table_year[yee][d])
              } else if (table_year[yee][d].end.slice(5,7) == "07"){ 
                month7.push(table_year[yee][d])
              } else if (table_year[yee][d].end.slice(5,7) == "08"){ 
                month8.push(table_year[yee][d])
              } else if (table_year[yee][d].end.slice(5,7) == "09"){ 
                month9.push(table_year[yee][d])
              } else if (table_year[yee][d].end.slice(5,7) == "10"){ 
                month10.push(table_year[yee][d])
              } else if (table_year[yee][d].end.slice(5,7) == "11"){ 
                month11.push(table_year[yee][d])
              } else if (table_year[yee][d].end.slice(5,7) == "12"){ 
                month12.push(table_year[yee][d])
            } 
          }
        }

        // tworzenie tablicy miesiecy 
        month1.reverse()
        month2.reverse()
        month3.reverse()
        month4.reverse() 
        month5.reverse()
        month6.reverse()
        month7.reverse()
        month8.reverse()
        month9.reverse()
        month10.reverse()
        month11.reverse()
        month12.reverse()
        months.push(month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12)

        
        //podzial na mecze do wyświetlania danych 
        let motoryczne_dane = data2
        let chwilowa = []
        let glowna_miesiac = []
        let glowna_roczna = []
        let licznik_meczy_miesiac = 0

        for (let al = 0; al<months.length; al++){ 
          for (let al2 = 0; al2<months[al].length; al2++){ 
            if (months[al][al2].type_id == 1){ 

              // nadwanie id meczy w miesiacu 
              months[al][al2]["match_id"] = licznik_meczy_miesiac
              licznik_meczy_miesiac +=1

              for (let moto = 0; moto<motoryczne_dane.length; moto++){ 
                if (months[al][al2].end == motoryczne_dane[moto].date)
                  chwilowa.push(motoryczne_dane[moto])
              }
              glowna_miesiac.push(chwilowa)
              chwilowa = []
            } else { 
              //chwilowa.push(months[al][al2])
              for (let moto = 0; moto<motoryczne_dane.length; moto++){ 
                if (months[al][al2].end == motoryczne_dane[moto].date)
                  chwilowa.push(motoryczne_dane[moto])
              }
            }
          }
          licznik_meczy_miesiac = 0
         // glowna_miesiac.reverse()
          glowna_roczna.push(glowna_miesiac)
          glowna_miesiac = []
        }
        this.motoric = glowna_roczna

        // dodanie counter do eventow 
        
        for(let mm=0; mm<months.length; mm++){ 
            let counter = 0
          for (let c  = 0; c<months[mm].length; c++){ 
            if (months[mm][c].type_id == 1 || months[mm][c].type_id == 2){ 
              counter = 0
            }else { 
              counter +=1 
              months[mm][c]["matchday_counter"]= counter 
            }
          }
        }

        //ponowne odworcenie tabeli wyswietlania 
        month1.reverse()
        month2.reverse()
        month3.reverse()
        month4.reverse() 
        month5.reverse()
        month6.reverse()
        month7.reverse()
        month8.reverse()
        month9.reverse()
        month10.reverse()
        month11.reverse()
        month12.reverse()
        
        months = []
        months.push(month1,month2,month3,month4,month5,month6,month7,month8,month9,month10,month11,month12)
        

        //dodawanie do glownej tablicy 
        main_table.push(months)
        main_motoric.push(glowna_roczna)
      }

         
        // kalendarz i miesiace 
        let calendar_data = new Date()
        let calendar_month = calendar_data.getMonth()
        let calendat_year = calendar_data.getYear() + 1900
        this.year_now = calendat_year
        this.year_timeline = calendat_year
        this.month_id = calendar_month
        this.events_months = main_table[this.year_timeline-2020]
        this.show_month = main_table[this.year_timeline-2020][calendar_month]
        this.main_table_main = main_table
        this.motoric_all = main_motoric
        this.motoric = main_motoric[this.year_timeline-2020]

        // przypisanie aktualnego miesiaca 

        if (calendar_month == 0 && this.lang=="en"){ 
          this.month_timeline = " January   "
        } else if (calendar_month == 1 && this.lang=="en"){ 
          this.month_timeline = " February  "
        } else if (calendar_month == 2 && this.lang=="en"){ 
          this.month_timeline = "   March   "
        } else if (calendar_month == 3 && this.lang=="en"){ 
          this.month_timeline = "   April   "
        } else if (calendar_month == 4 && this.lang=="en"){ 
          this.month_timeline = "    May    "
        } else if (calendar_month == 5 && this.lang=="en"){ 
          this.month_timeline = "   June    "
        } else if (calendar_month == 6 && this.lang=="en"){ 
          this.month_timeline = "   July    "
        } else if (calendar_month == 7 && this.lang=="en"){ 
          this.month_timeline = "  August   "
        } else if (calendar_month == 8 && this.lang=="en"){ 
          this.month_timeline = " September "
        } else if (calendar_month == 9 && this.lang=="en"){ 
          this.month_timeline = "  October  "
        } else if (calendar_month == 10 && this.lang=="en"){ 
          this.month_timeline = " November  "
        } else if (calendar_month == 11&& this.lang=="en"){ 
          this.month_timeline = " December  "
        } else if(calendar_month == 0 && this.lang=="pl"){ 
          this.month_timeline = " Styczeń   "
          }else if (calendar_month == 1 && this.lang=="pl"){ 
          this.month_timeline = " Luty  "
        } else if (calendar_month == 2 && this.lang=="pl"){ 
          this.month_timeline = "   Marzec   "
        } else if (calendar_month == 3 && this.lang=="pl"){ 
          this.month_timeline = "   Kwieciń   "
        } else if (calendar_month == 4 && this.lang=="pl"){ 
          this.month_timeline = "    Maj    "
        } else if (calendar_month == 5 && this.lang=="pl"){ 
          this.month_timeline = "   Czerwiec    "
        } else if (calendar_month == 6 && this.lang=="pl"){ 
          this.month_timeline = "   Lipiec    "
        } else if (calendar_month == 7 && this.lang=="pl"){ 
          this.month_timeline = "  Sierpień   "
        } else if (calendar_month == 8 && this.lang=="pl"){ 
          this.month_timeline = " Wrzesień "
        } else if (calendar_month == 9 && this.lang=="pl"){ 
          this.month_timeline = "  Październik  "
        } else if (calendar_month == 10 && this.lang=="pl"){ 
          this.month_timeline = " Listopad  "
        } else if (calendar_month == 11&& this.lang=="pl"){ 
          this.month_timeline = " Grudzień  "
        }
      }
      }, 
      minus_month(){ 
        if (this.month_id >0 && this.month_id<=11){ 
          this.month_id-=1
        }
        this.show_month = this.events_months[this.month_id]

          if (this.month_id == 0 && this.lang=="en"){ 
          this.month_timeline = " January   "
        } else if (this.month_id == 1 && this.lang=="en"){ 
          this.month_timeline = " February  "
        } else if (this.month_id == 2 && this.lang=="en"){ 
          this.month_timeline = "   March   "
        } else if (this.month_id == 3 && this.lang=="en"){ 
          this.month_timeline = "   April   "
        } else if (this.month_id == 4 && this.lang=="en"){ 
          this.month_timeline = "    May    "
        } else if (this.month_id == 5 && this.lang=="en"){ 
          this.month_timeline = "   June    "
        } else if (this.month_id == 6 && this.lang=="en"){ 
          this.month_timeline = "   July    "
        } else if (this.month_id == 7 && this.lang=="en"){ 
          this.month_timeline = "  August   "
        } else if (this.month_id == 8 && this.lang=="en"){ 
          this.month_timeline = " September "
        } else if (this.month_id == 9 && this.lang=="en"){ 
          this.month_timeline = "  October  "
        } else if (this.month_id == 10 && this.lang=="en"){ 
          this.month_timeline = " November  "
        } else if (this.month_id == 11&& this.lang=="en"){ 
          this.month_timeline = " December  "
        } else if(this.month_id == 0 && this.lang=="pl"){ 
          this.month_timeline = " Styczeń   "
          }else if (this.month_id == 1 && this.lang=="pl"){ 
          this.month_timeline = " Luty  "
        } else if (this.month_id == 2 && this.lang=="pl"){ 
          this.month_timeline = "   Marzec   "
        } else if (this.month_id == 3 && this.lang=="pl"){ 
          this.month_timeline = "   Kwieciń   "
        } else if (this.month_id == 4 && this.lang=="pl"){ 
          this.month_timeline = "    Maj    "
        } else if (this.month_id == 5 && this.lang=="pl"){ 
          this.month_timeline = "   Czerwiec    "
        } else if (this.month_id == 6 && this.lang=="pl"){ 
          this.month_timeline = "   Lipiec    "
        } else if (this.month_id == 7 && this.lang=="pl"){ 
          this.month_timeline = "  Sierpień   "
        } else if (this.month_id == 8 && this.lang=="pl"){ 
          this.month_timeline = " Wrzesień "
        } else if (this.month_id == 9 && this.lang=="pl"){ 
          this.month_timeline = "  Październik  "
        } else if (this.month_id == 10 && this.lang=="pl"){ 
          this.month_timeline = " Listopad  "
        } else if (this.month_id == 11&& this.lang=="pl"){ 
          this.month_timeline = " Grudzień  "
        }
      },
      plus_month(){ 
        if (this.month_id >=0 && this.month_id<11){ 
          this.month_id+=1
        } 
        this.show_month = this.events_months[this.month_id]
        

         if (this.month_id == 0 && this.lang=="en"){ 
          this.month_timeline = " January   "
        } else if (this.month_id == 1 && this.lang=="en"){ 
          this.month_timeline = " February  "
        } else if (this.month_id == 2 && this.lang=="en"){ 
          this.month_timeline = "   March   "
        } else if (this.month_id == 3 && this.lang=="en"){ 
          this.month_timeline = "   April   "
        } else if (this.month_id == 4 && this.lang=="en"){ 
          this.month_timeline = "    May    "
        } else if (this.month_id == 5 && this.lang=="en"){ 
          this.month_timeline = "   June    "
        } else if (this.month_id == 6 && this.lang=="en"){ 
          this.month_timeline = "   July    "
        } else if (this.month_id == 7 && this.lang=="en"){ 
          this.month_timeline = "  August   "
        } else if (this.month_id == 8 && this.lang=="en"){ 
          this.month_timeline = " September "
        } else if (this.month_id == 9 && this.lang=="en"){ 
          this.month_timeline = "  October  "
        } else if (this.month_id == 10 && this.lang=="en"){ 
          this.month_timeline = " November  "
        } else if (this.month_id == 11&& this.lang=="en"){ 
          this.month_timeline = " December  "
        } else if(this.month_id == 0 && this.lang=="pl"){ 
          this.month_timeline = " Styczeń   "
          }else if (this.month_id == 1 && this.lang=="pl"){ 
          this.month_timeline = " Luty  "
        } else if (this.month_id == 2 && this.lang=="pl"){ 
          this.month_timeline = "   Marzec   "
        } else if (this.month_id == 3 && this.lang=="pl"){ 
          this.month_timeline = "   Kwieciń   "
        } else if (this.month_id == 4 && this.lang=="pl"){ 
          this.month_timeline = "    Maj    "
        } else if (this.month_id == 5 && this.lang=="pl"){ 
          this.month_timeline = "   Czerwiec    "
        } else if (this.month_id == 6 && this.lang=="pl"){ 
          this.month_timeline = "   Lipiec    "
        } else if (this.month_id == 7 && this.lang=="pl"){ 
          this.month_timeline = "  Sierpień   "
        } else if (this.month_id == 8 && this.lang=="pl"){ 
          this.month_timeline = " Wrzesień "
        } else if (this.month_id == 9 && this.lang=="pl"){ 
          this.month_timeline = "  Październik  "
        } else if (this.month_id == 10 && this.lang=="pl"){ 
          this.month_timeline = " Listopad  "
        } else if (this.month_id == 11&& this.lang=="pl"){ 
          this.month_timeline = " Grudzień  "
        }
      },
      plus_year(){ 
        if (this.year_timeline < this.year_now){ 
          this.year_timeline +=1
        }
        this.events_months = this.main_table_main[this.year_timeline-2020]
        this.show_month = this.main_table_main[this.year_timeline-2020][this.month_id]
        this.motoric = this.motoric_all[this.year_timeline-2020]

      },
      minus_year(){ 
        if (this.year_timeline > 2020){ 
          this.year_timeline -=1
        }
        this.events_months = this.main_table_main[this.year_timeline-2020]
        this.show_month = this.main_table_main[this.year_timeline-2020][this.month_id]
        this.motoric = this.motoric_all[this.year_timeline-2020]


        
      },
      matchday_counter_func(){ 
        let counter = 0
        for (let i  = 0; i<this.show_month.length; i++){ 
          if (this.show_month[i].type_id == 1 || this.show_month[i].type_id ){ 
            counter = ""
          } else { 
            counter +=1 
            this.show_month[i]["matchday_counter"]= counter 
          }
        }
      }
    

    }
}
</script>

<style>

</style>