import Vue from 'vue';
import Vuetify from 'vuetify/lib';

import colors from 'vuetify/lib/util/colors'

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: colors.blue.darken4,
        secondary: colors.blue.lighten4,
        accent: colors.indigo.base,
      },
    },
  },
});
