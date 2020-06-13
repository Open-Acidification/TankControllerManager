<template>
  <v-content class="pa-4 ma-0 fill-height">
    <div v-if="tank">
      <v-form
        ref="query_form"
        v-model="valid"
        lazy-validation
      >
        <v-container>
          <v-row class="align-center pa-0" no-gutters>
            <v-col md="auto">
              <h3>
                View data from tank #{{ tank.tankid }}:
              </h3>
            </v-col>
            <v-spacer/>
            <v-col md="auto">
              <span class="subtitle-2">Device: {{tank.device_name}}</span>
              <v-btn :to="{path: '/devices/'+tank.device_mac}" icon>
                <v-icon>mdi-cog</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-container>
        <v-container>
          <v-row>
            <router-view/>
          </v-row>
          <v-row>
            <v-col class="pa-0 pr-4 ma-0">
              <v-text-field
                v-model="freq"
                :rules="positiveRules"
                label="Frequency"
                type="number"
                required
              />
            </v-col>
            <v-col class="pa-0 ma-0">
              <v-text-field
                v-model="cutoff"
                :rules="positiveRules"
                label="Cutoff"
                type="number"
                required
              />
            </v-col>
            <v-col class="pa-0 pl-4 ma-0">
              <v-text-field
                v-model="total"
                :rules="positiveRules"
                label="Total"
                type="number"
                required
              />
            </v-col>
          </v-row>
          <v-row>
            <!-- <v-col>
              <v-btn
                :disabled="true"
                color="secondary"
                class="mr-4 black--text"
                @click="loadGraph"
                block
              >
                View Graph
              </v-btn>
            </v-col> -->
            <v-col>
              <v-btn
                color="secondary"
                class="mr-4 black--text"
                @click="downloadCSV"
                block
              >
                Download CSV
              </v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
    </div>
    <CenteredProgress v-else/>
  </v-content>
</template>

<script src="https://d3js.org/d3.v5.js"></script>
<script>
import CenteredProgress from '../CenteredProgress.vue';

export default {
  name: 'TankView',

  components: {
    CenteredProgress,
  },

  data () {
    return {
      tank: null,

      valid: true,

      // Constraints
      start: null,
      end: null,
      freq: 0,
      cutoff: 0,
      total: 0,
      positiveRules: [
        v => v >= 0 || 'Value must not be negative',
      ],
    }
  },
  created () {
    this.fetchTank()
  },
  watch: {
    '$route': 'fetchTank'
  },
  methods: {
    fetchTank () {
      this.$store.dispatch('waitForTanks').then(() => {
        this.tank = this.$store.getters.getTank(this.$route.params.tankid);
      });
    },
    loadGraph () {
      // this.axios.get('http://'+location.hostname+':8080/api/tanks/'+this.tank.tankid+
      //     '/data?freq='+this.freq+'&cutoff='+this.cutoff+'&total='+this.total,
      // ).then(() => {

      // });
      var data = [20, 10, 15, 14, 13, 12]
      this.$router.push({ path: '/tanks/'+this.tank.tankid+'/chart', params: {chartdata: data,  options: {}}})
    },
    downloadCSV () {
      this.axios({
        url: 'http://'+location.hostname+':8080/api/tanks/'+this.tank.tankid+
          '/data?freq='+this.freq+'&cutoff='+this.cutoff+'&total='+this.total+'&download=1',
        method: 'GET',
        responseType: 'blob', // important
      }).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'file.csv');
        document.body.appendChild(link);
        link.click();
      }).catch((error) => {
        console.log(error);
      });
    },
  }
}
</script>

<style>
  html {
    overflow-y: hidden;
  }
</style>