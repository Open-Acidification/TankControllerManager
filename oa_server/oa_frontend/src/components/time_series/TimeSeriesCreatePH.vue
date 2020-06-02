<template>
  <v-content class="pa-4 ma-0 fill-height">
    <v-form
      ref="create_form"
      v-model="valid"
      lazy-validation
    >
      <v-container>
        <v-row class="align-center pa-0" no-gutters>
          <v-col md="auto">
            <h3>
              Create New pH Time Series
            </h3>
          </v-col>
        </v-row>
        <v-row>
          <v-radio-group required row v-model="tsFunction">
            <v-radio
              label="Hold"
              value="hold"
            ></v-radio>
            <v-radio
              label="Ramp"
              value="ramp"
            ></v-radio>
            <v-radio
              label="Sine"
              value="sine"
            ></v-radio>
            <v-radio
              label="Custom"
              value=""
            ></v-radio>
          </v-radio-group>
        </v-row>
        <v-row>
          <v-text-field
            v-model="name"
            :counter="32"
            :rules="nameRules"
            label="Name"
            required
          />
        </v-row>
        <div v-if="tsFunction=='hold'">
          <v-row>
            <v-text-field
              v-model="holdAt"
              :rules="pHRules"
              label="Hold At"
              type="number"
              required
            />
          </v-row>
        </div>
        <div v-else-if="tsFunction=='ramp'">
          <v-row>
            <v-col class="pa-0 pr-4 ma-0">
              <v-text-field
                v-model="rampStart"
                :rules="pHRules"
                label="Start"
                type="number"
                required
              />
            </v-col>
            <v-col class="pa-0 ma-0">
              <v-text-field
                v-model="rampEnd"
                :rules="pHRules"
                label="End"
                type="number"
                required
              />
            </v-col>
            <v-col class="pa-0 pl-4 ma-0">
              <v-text-field
                v-model="rampDuration"
                :rules="timeRules"
                label="Duration"
                type="number"
                suffix="s"
                required
              />
            </v-col>
          </v-row>
        </div>
        <div v-else-if="tsFunction=='sine'">
          <v-row>
            <v-col class="pa-0 pr-4 ma-0">
              <v-text-field
                v-model="sineFreq"
                :rules="freqRules"
                label="Frequency"
                type="number"
                suffix="s"
                required
              />
            </v-col>
            <v-col class="pa-0 pr-2 ma-0">
              <v-text-field
                v-model="sineAmp"
                :rules="ampRules"
                label="Amplitude"
                type="number"
                required
              />
            </v-col>
            <v-col class="pa-0 pl-2 ma-0">
              <v-text-field
                v-model="sineOffX"
                :rules="timeRules"
                label="Offset (x)"
                type="number"
                suffix="s"
                required
              />
            </v-col>
            <v-col class="pa-0 pl-4 ma-0">
              <v-text-field
                v-model="sineOffY"
                :rules="pHRules"
                label="Offset (y)"
                type="number"
                required
              />
            </v-col>
          </v-row>
        </div>
        <div v-else>
          <!-- Implement custom time series creation later -->
        </div>
        <v-row>
          <v-col>
            <v-btn
              :disabled="!valid"
              color="success"
              class="mr-4"
              @click="submitForm"
              block
            >
              <v-dialog v-model="creating" persistent max-width="60">
                <CenteredProgress/>
              </v-dialog>
              Create Time Series
            </v-btn>
          </v-col>
          <v-col>
            <v-btn
              color="error"
              class="mr-4"
              @click="clearForm"
              block
            >
              Clear Form
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
    <v-snackbar
      v-model="successSnackbar"
      bottom
      right
    >
      Successfully created time series with ID {{createdID}}
    </v-snackbar>
    <v-snackbar
      v-model="errorSnackbar"
      bottom
      right
    >
      Something went wrong with creating the time series.
    </v-snackbar>
  </v-content>
</template>

<script>
import CenteredProgress from '../CenteredProgress.vue';

export default {
  name: 'TimeSeriesCreatePH',

  components: {
    CenteredProgress,
  },

  data () {
    return {
      // Time Series Function Selection
      tsFunction: "hold",
      // Form
      valid: false,
      name: '',
      nameRules: [
        v => !!v || 'Name is required',
        v => (v && v.length <= 32) || 'Name must contain 32 characters or fewer',
      ],

      // Generic rules
      pHRules: [
        v => (v && v >= 7 && v <= 14) || 'Value must be between 7 and 14, inclusive',
      ],
      timeRules: [
        v => (v && v >= 0) || 'Value must be at least 0 seconds',
      ],

      // Hold
      holdAt: 8,

      // Ramp
      rampStart: 8,
      rampEnd: 9,
      rampDuration: 600,

      // Sine
      sineFreq: 600,
      freqRules: [
        v => (v && v > 0) || 'Value must be greater than 0 seconds',
      ],
      sineAmp: 1,
      ampRules: [
        v => (v && v >= 0 && v <= 3.5) || 'Value must be between 0 and 3.5, inclusive',
      ],
      sineOffX: 0,
      sineOffY: 8,

      successSnackbar: false,
      createdID: 0,

      errorSnackbar: false,

      creating: false,
    };
  },
  methods: {
    clearForm () {
      this.$refs.create_form.reset();
    },
    submitForm () {
      this.$refs.create_form.validate();
      if (!this.valid) {
        return
      }
      var data = {
        name: this.name
      }
      var endpoint = "/generate/"+this.tsFunction+"/";
      if (this.tsFunction == 'hold') {
        data.at = this.holdAt;
      } else if (this.tsFunction == 'ramp') {
        data.start = this.rampStart;
        data.end = this.rampEnd;
        data.duration = this.rampDuration;
      } else if (this.tsFunction == 'sine') {
        data.frequency = this.sineFreq;
        data.amplitude = this.sineAmp;
        data.offset_x = this.sineOffX;
        data.offset_y = this.sineOffY;
      } else {
        endpoint = "/";
        return;
      }
      return this.createTimeSeries(endpoint, data);
    },
    createTimeSeries (endpoint, data) {
      this.creating = true;
      this.axios.post(
        'http://'+location.hostname+':8080/api/time_series/ph'+endpoint,
        data
      ).then((response) => {
        this.creating = false;
        this.createdID = response.data.id;
        this.successSnackbar = true;
        this.$store.dispatch('updateTimeSeries');
      }).catch((error) => {
        console.log(error);
        this.errorSnackbar = true;
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