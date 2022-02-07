import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

import pl from 'vuetify/lib/locale/pl'
import en from 'vuetify/lib/locale/en'

Vue.use(Vuetify);

export default new Vuetify({
    theme: { dark: true },
    lang: {
        locales: { en, pl },
        current: 'en',
      },
});
