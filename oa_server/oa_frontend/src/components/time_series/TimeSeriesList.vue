<template>
  <v-navigation-drawer
    :expand-on-hover="!($route.path == '/time_series')"
    width=300
    permanent
  >
    <v-list class="overflow-y-auto">
      <v-list-item>
          <v-list-item-title class="title">Temperature</v-list-item-title>
          <v-list-item-icon>
            <v-btn to="/time_series/temp/create" icon>
              <v-icon>mdi-plus-box</v-icon>
            </v-btn>
          </v-list-item-icon>
      </v-list-item>
      <v-divider/>
      <div
        v-for="tsTemp in this.$store.state.timeSeries.temp"
        :key="tsTemp.id"
      >
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="subtitle-1">
              {{ tsTemp.name }}
            </v-list-item-title>
          </v-list-item-content>
          <v-list-item-icon>
            <v-btn @click="removeTimeSeriesTemp(tsTemp)" icon>
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </v-list-item-icon>
        </v-list-item>
        <v-sparkline
          :value="tsTemp.value"
          color="black"
          line-width="2"
          padding=16
        />
        <v-divider/>
      </div>
      <v-list-item>
          <v-list-item-title class="title">pH</v-list-item-title>
          <v-list-item-icon>
            <v-btn to="/time_series/ph/create" icon>
              <v-icon>mdi-plus-box</v-icon>
            </v-btn>
          </v-list-item-icon>
      </v-list-item>
      <v-divider/>
      <div
        v-for="tsPH in this.$store.state.timeSeries.pH"
        :key="tsPH.id"
      >
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="subtitle-1">
              {{ tsPH.name }}
            </v-list-item-title>
          </v-list-item-content>
          <v-list-item-icon>
            <v-btn @click="removeTimeSeriesPH(tsPH)" icon>
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </v-list-item-icon>
        </v-list-item>
        <v-sparkline
          :value="tsPH.value"
          color="black"
          line-width="2"
          padding=16
        />
        <v-divider/>
      </div>
    </v-list>
  </v-navigation-drawer>
</template>

<script>

export default {
  name: 'TimeSeriesList',

  methods: {
    removeTimeSeriesTemp (ts) {
      this.axios.delete(
        'http://'+location.host+'/api/time_series/'+ts.id+'/'
      ).then(() => {
        // We've removed the time series from the database, so remove it from the store
        this.$store.commit('removeTimeSeriesTemp', ts)
        // Then update the store just to make sure that we're in sync
        this.$store.dispatch('updateTimeSeries');
      }).catch((error) => {
        console.log(error);
      });
    },
    removeTimeSeriesPH (ts) {
      this.axios.delete(
         'http://'+location.host+'/api/time_series/'+ts.id+'/'
      ).then(() => {
        // We've removed the time series from the database, so remove it from the store
        this.$store.commit('removeTimeSeriesPH', ts)
        // Then update the store just to make sure that we're in sync
        this.$store.dispatch('updateTimeSeries');
      }).catch((error) => {
        console.log(error);
      });
    },
  }
}
</script>

<style>

</style>