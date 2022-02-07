<template>
  <v-row class="fill-height">
    <v-col style="z-index: 0">
      <v-sheet height="64">
        <v-toolbar
          flat
        >
            <!--v-btn
                class="mr-4"
                color="primary"
                @click="dialog = true"
             >
                Add Event
            </v-btn-->

          <v-btn
            outlined
            class="mr-4"
            color="grey darken-2"
            @click="setToday"
          >
            {{ $t('today') }}
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
                <span>{{ $t('month') }}</span>
                <v-icon right>
                  mdi-menu-down
                </v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item @click="type = 'day'">
                <v-list-item-title>{{ $t('day') }}</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = 'week'">
                <v-list-item-title>{{ $t('week') }}</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = 'month'">
                <v-list-item-title>{{ $t('month') }}</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = '4day'">
                <v-list-item-title>{{ $t('4day') }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-toolbar>
      </v-sheet>

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
              <v-toolbar-title v-html="selectedEvent.name"></v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>
            <v-card-text>
              <!--form v-if="currentlyEditing != selectedEvent.id">
                  {{ this.event_type }}
              </form>
              <form v-else>
                  <textarea-autosize 
                  v-model="selectedEvent.details"
                  type="text"
                  style="width: 100%"
                  :min-height="100"
                  placeholder="add note">
                  </textarea-autosize> 
              </form-->
              <form style="color: black">
                {{ selectedEvent.name }}
                {{ selectedEvent.event_type }}
                {{ selectedEvent.kinase }}
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
        <v-alert v-if="isPast"
        border="right"
        colored-border
        type="warning"
        elevation="2"
        class="mt-4"
      >
        This event has passed - surveys won't be generated
      </v-alert>
      </v-sheet>
    </v-col>
  </v-row>
</template>

<script>

export default {
    components: {
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
        types: ['Training','Match league', 'Match Cup', 'Match international', 'Medical'],
        currentlyEditing: null,
        selectedEvent: {},
        selectedElement: null,
        selectedOpen: false,
        events: [],
        dialog: false,
        selectedUsers: '',
        requiredRules: [v => !!v || 'Required'],
        valid: true,
        selectedUsersError: false,
        addEventSuccess: false,
        dateError: false,
        kinase: null,
        isPast: null,
        event: {}
    }),
    mounted() {
        this.getLanguage();
        this.getEvents();
    },
    methods: {
      async getEvents(){
        //const res = await fetch('http://localhost:5000/api/events')
        const res = await fetch('api/my_events')
        const data = await res.json()
        this.events = data
      },
      async addEvent() {
        
        //Walidacja
        if (this.selectedUsers == '' ) {
          this.selectedUsersError = true
          this.addEventSuccess = false
          return
        }
        this.selectedUsersError = false
        if (this.date_start > this.date_end || (this.date_end == this.date_start && this.hour_start > this.hour_end)) {
          this.dateError = true
          this.addEventSuccess = false
          return
        }
        this.dateError = false
        this.addEventSuccess = true
        this.dialog = false //lepiej byłoby to dac przy przycisku w template

        this.checkIfPast()


        const selectedId = []
        for (var i = 0; i < this.selectedUsers.length; i++) {
          //const obj = {
            //id: this.selectedUsers[i].id
          //}
          selectedId.push(this.selectedUsers[i].id)
        }

        this.event = {
            name: this.name,
            details: this.details,
            start: this.date_start + " " + this.hour_start + ":00",
            end: this.date_end + " " + this.hour_end + ":00",
            type: this.getTypeId(this.event_type),
            color: this.color,
            latitude: null,
            longitude: null,
            //by_users: [1],
            by_users: selectedId,
            by_team: [],
            kinase: this.kinase
        }
        //const res = await fetch('http://localhost:5000/api/events', {
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
          this.color = 'red'
          return 5
        }
        else if(event_type == 'Training') {
          this.color = 'blue'
          return 4
        }
        else if(event_type == 'Match international') {
          this.color = 'green'
          return 3
        }
        else if(event_type == 'Match Cup') {
          this.color = 'blue'
          return 2
        }
        else if(event_type == 'Match league') {
          this.color = 'green'
          return 1
        }
      },
      checkIfPast() {
        if (this.date_end < this.today) {
          this.isPast = true
        }
        else {
          this.isPast = false
        }
      },
      update(variable2) {
        this.selectedUsers = variable2
      },
      closeDialog() {
        if (this.addEventSuccess == true) {
          this.dialog = false
        }
      },
      async getLanguage() {
        const res = await fetch('/language')
        const data = await res.text()
        this.$i18n.locale = data
        this.$vuetify.lang.current = data
        this.lang = data
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