import 'regenerator-runtime/runtime'
<template>
  <v-row class="fill-height">
    <v-col>
      <v-sheet height="64">
        <v-toolbar
          flat
        >
            <v-btn
                class="mr-4"
                color="primary"
                @click="dialog = true"
             >
                Add Event
            </v-btn>

          <v-btn
            outlined
            class="mr-4"
            color="grey darken-2"
            @click="setToday"
          >
            Today
          </v-btn>
          <v-btn
            fab
            text
            small
            color="grey darken-2"
            @click="prev"
          >
            <v-icon small>
              mdi-chevron-left
            </v-icon>
          </v-btn>
          <v-btn
            fab
            text
            small
            color="grey darken-2"
            @click="next"
            class="mr-4"
          >
            <v-icon small>
              mdi-chevron-right
            </v-icon>
          </v-btn>
          <v-toolbar-title v-if="$refs.calendar">
            {{ $refs.calendar.title }}
          </v-toolbar-title>
          <v-spacer></v-spacer>
          <v-menu
            bottom
            right
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                outlined
                color="grey darken-2"
                v-bind="attrs"
                v-on="on"
              >
                <span>{{ typeToLabel[type] }}</span>
                <v-icon right>
                  mdi-menu-down
                </v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item @click="type = 'day'">
                <v-list-item-title>Day</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = 'week'">
                <v-list-item-title>Week</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = 'month'">
                <v-list-item-title>Month</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = '4day'">
                <v-list-item-title>4 days</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-toolbar>
      </v-sheet>
      <!-- Add event -->
      <v-dialog v-model="dialog" max-width="1000px">
          <v-card>
              <v-containter>
                  <v-form class="pa-md-4 mx-lg-auto" @submit.prevent="addEvent">
                      <v-text-field v-model="name" type="text" label="event name (requierd)">
                      </v-text-field>
                      <v-text-field v-model="details" type="text" label="detail">
                      </v-text-field>
                      <v-text-field v-model="start" type="date" label="start (requierd)">
                      </v-text-field>
                      <v-text-field v-model="hour_start" type="time" label="00:00">
                      </v-text-field>
                      <v-text-field v-model="end" type="date" label="end (requierd)">
                      </v-text-field>
                      <v-text-field v-model="hour_end" type="time" label="00:00">
                      </v-text-field>
                      <!--v-text-field v-model="event_type" type="number" label="type">
                      </v-text-field-->
                      <v-select
                        v-model="event_type"
                        :items="types"
                        label="Event type"
                        required
                      ></v-select>
                      <v-text-field v-model="color" type="color" label="color (click to open color menu)">
                      </v-text-field>
                      <Teams @pass="update"/>
                      <v-btn type="submit" color="primary" class="mr-4 mt-4" @click.stop="dialog=false">
                          Create Event
                      </v-btn>
                  </v-form>
              </v-containter>
          </v-card>
      </v-dialog>
      <v-sheet height="600">
        <v-calendar
          ref="calendar"
          v-model="focus"
          color="primary"
          :events="events"
          :event-color="getEventColor"
          :type="type"
          @click:event="showEvent"
          @click:more="viewDay"
          @click:date="viewDay"
          @change="updateRange"
        ></v-calendar>
        <v-menu
          v-model="selectedOpen"
          :close-on-content-click="false"
          :activator="selectedElement"
          offset-x
        >
          <v-card
            color="grey lighten-4"
            min-width="350px"
            flat
          >
            <v-toolbar
              :color="selectedEvent.color"
              dark
            >
              <v-btn @click="deleteEvent(selectedElement.id)" icon>
                <v-icon>mdi-delete</v-icon>
              </v-btn>
              <v-toolbar-title v-html="selectedEvent.name"></v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>
            <v-card-text>
              <form v-if="currentlyEditing != selectedEvent.id">
                  {{selectedEvent.details}}
              </form>
              <form v-else>
                  <textarea-autosize 
                  v-model="selectedEvent.details"
                  type="text"
                  style="width: 100%"
                  :min-height="100"
                  placeholder="add note">
                  </textarea-autosize> 
              </form>
            </v-card-text>
            <v-card-actions>
              <v-btn
                text
                color="secondary"
                @click="selectedOpen = false"
              >
                Close
              </v-btn>
              <v-btn
                text
                v-if="currentlyEditing != selectedEvent.id"
                @click.prevent="editEvent(selectedEvent)"
              >
                Edit
              </v-btn>
              <v-btn
                text
                v-else
                @click.prevent="updateEvent(selectedEvent)"
              >
                Save
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-menu>
      </v-sheet>
    </v-col>
  </v-row>
</template>

<script>
import Teams from './Teams.vue'
//import Players from './Players'

export default {
    components: {
      Teams,
      //Players
    },
    data: () => ({
        today: new Date().toISOString().substr(0, 10),
        focus: new Date().toISOString().substr(0, 10),
        type: "month",
        typeToLabel: {
            month: "Month",
            week: "Week",
            day: "Day",
            "4day": "4 Days"
        },
        types: ['Training', 'Match', 'Medical'],
        currentlyEditing: null,
        selectedEvent: {},
        selectedElement: null,
        selectedOpen: false,
        events: [],
        dialog: false,
        parentvariable: ''
    }),
    mounted() {
        this.getEvents();
    },
    methods: {
      async getEvents(){
        //const res = await fetch('http://localhost:5000/api/events')
        const res = await fetch('api/events')
        const data = await res.json()
        console.log(data)
        this.events = data
      },
      async addEvent() {
        const selectedId = []
        for (var i = 0; i < this.parentvariable.length; i++) {
          //const obj = {
            //id: this.parentvariable[i].id
          //}
          selectedId.push(this.parentvariable[i].id)
        }
        console.log('tutaj')
        console.log(selectedId)

        const event = {
            name: this.name,
            details: this.details,
            start: this.start + " " + this.hour_start + ":00",
            end: this.end + " " + this.hour_end + ":00",
            color: this.color,
            type: this.getTypeId(this.event_type),
            latitude: null,
            longitude: null,
            //by_users: [1],
            by_users: selectedId,
            by_team: []
        }
        //onst res = await fetch('http://localhost:5000/api/events', {
        const res = await fetch('api/events', {
          method: 'POST',
          headers: {
            'Content-type': 'application/json',
          },
          body: JSON.stringify(event)
        })
        const data = await res.json()
        this.events = [...this.events, data]
      },
      getTypeId(event_type) {
        if(event_type == 'Medical') {
          return 5
        }
        else if(event_type == 'Training') {
          return 4
        }
        else if(event_type == 'Match') {
          return 1
        }
      },
      update(variable2) {
        this.parentvariable = variable2
      },
        /*
        async updateEvent(event) {
            await db.collection('calEvent').doc(this.currentlyEditing).update({
                details: event.details
            });
            this.selectedOpen = false;
            this.currentlyEditing = null;
        },
        async deleteEvent(event) {
            await db.collection("calEvent").doc(event).detele();

            this.selectedOpen = false;
            this.getEvents();
        },
        async addEvent() {
            if(this.name && this.start && this.end) {
                await db.collection('calEvent').add({
                    name: this.name,
                    details: this.details,
                    start: this.start,
                    end: this.end,
                    color: this.color
                });
                this.getEvents();
                this.name = "";
                this.details = "";
                this.start = "";
                this.end = "";
                this.color = "";
            } else {
                alert('Name required')
            }

        },*/
        viewDay( {date }) {
            this.focus = date;
            this.type = "day";
        },
        getEventColor(event) {
            return event.color;
        },
        setToday() {
            this.focus = this.today;
        },
        prev() {
            this.$refs.calendar.prev();
        },
        next() {
            this.$refs.calendar.next();
        },
        editEvent(event) {
            this.currentlyEditing = event.id
        },
        showEvent( { nativeEvent, event }) {
            const open = () => {
                this.selectedEvent = event;
                this.selectedElement = nativeEvent.target;
                setTimeout(() => (this.selectedOpen = true), 10);
            };

            if (this.selectedOpen) { 
                this.selectedOpen = false;
                setTimeout(open, 10);
            } else {
                open();
            }
            
            nativeEvent.stopPropagation();
        },
        updateRange ({ start, end }) {
            this.start = start
            this.end = end
        },
        nth (d) {
            return d > 3 && d < 21
            ? 'th'
            : ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th'][d % 10]
        }
    }
}
</script>