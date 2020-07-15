<template>
  <v-content class="pa-4 ma-0 fill-height">
    <div v-if="device ">
      <v-form
        ref="update_form"
        v-model="valid"
        lazy-validation
      >
        <v-container>
          <v-row class="align-center pa-0" no-gutters>
            <v-col md="auto">
              <h3>
                Configure device with MAC address {{ device.mac }}
              </h3>
            </v-col>
            <v-spacer/>
            <v-col md="auto">
              <v-dialog v-model="confirmRemoval" persistent max-width="290">
                <template v-slot:activator="{ on }">
                  <v-btn icon v-on="on">
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </template>
                <v-card>
                  <v-card-title class="headline">Remove device?</v-card-title>
                  <v-card-text>
                    Are you sure you want to remove the device "{{device.name}}"?
                    Doing so will delete all of its stored data.
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" text @click="confirmRemoval = false">Cancel</v-btn>
                    <v-btn color="primary" text @click="removeDevice">Remove Device</v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-col>
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
          <v-row>
            <v-text-field
              v-model="ip"
              :rules="ipRules"
              label="IP Address"
              required
            />
          </v-row>
          <v-row>
            <v-col class="pa-0 pr-2 ma-0">
              <v-text-field
                v-model.number="tempVariance"
                :rules="varianceRules"
                label="Temperature Variance Threshold"
                type="number"
                required
              />
            </v-col>
            <v-col class="pa-0 pl-2 ma-0">
              <v-text-field
                v-model.number="phVariance"
                :rules="varianceRules"
                label="pH Variance Threshold"
                type="number"
                required
              />
            </v-col>
          </v-row>
          <v-row>
            <v-textarea
                v-model="notes"
                label="Notes"
            />
          </v-row>
          <v-row>
            <v-col>
              <v-btn
                :disabled="!valid"
                color="success"
                class="mr-4"
                @click="updateDevice"
                block
              >
                Update Device
              </v-btn>
            </v-col>
            <v-col>
              <v-btn
                color="error"
                class="mr-4"
                @click="fillForm"
                block
              >
                Reset Form
              </v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
      <v-divider/>
      <v-form
        ref="update_form"
        v-model="valid"
        lazy-validation
      >
        <v-container>
          <v-row class="align-center pa-0" no-gutters>
            <v-col md="auto">
              <h3>
                Choose time series:
              </h3>
            </v-col>
          </v-row>
          <v-row>
            <v-col class="pa-0 pr-2 ma-0">
              <v-select
                v-model="tempTimeSeriesID"
                :items="$store.state.timeSeries.temp"
                item-text="name"
                item-value="id"
                label="Temperature"
              ></v-select>
            </v-col>
            <v-col class="pa-0 pl-2 ma-0">
              <v-select
                v-model="pHTimeSeriesID"
                :items="$store.state.timeSeries.pH"
                item-text="name"
                item-value="id"
                label="pH"
              ></v-select>
            </v-col>
          </v-row>
          <v-row>
            <v-col class="pa-0 pr-2 ma-0">
              <v-text-field
                v-model.number="tempTimeSeriesDelay"
                :rules="delayRules"
                label="Temperature Delay"
                type="number"
                required
              />
            </v-col>
            <v-col class="pa-0 pl-2 ma-0">
              <v-text-field
                v-model.number="pHTimeSeriesDelay"
                :rules="delayRules"
                label="pH Delay"
                type="number"
                required
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-btn
                :disabled="!valid"
                color="success"
                class="mr-4"
                @click="applyTimeSeries"
              >
                Apply Time Series
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
        Successfully updated device.
      </v-snackbar>
      <v-snackbar
        v-model="updateErrorSnackbar"
        bottom
        right
      >
        Something went wrong with updating device.
      </v-snackbar>
      <v-snackbar
        v-model="removeErrorSnackbar"
        bottom
        right
      >
        Something went wrong with removing device.
      </v-snackbar>
    </div>
    <CenteredProgress v-else/>
  </v-content>
</template>

<script>
import CenteredProgress from '../CenteredProgress.vue';

export default {
  name: 'DeviceConfig',

  components: {
    CenteredProgress,
  },

  data () {
    return {
      device: null,

      // Form
      valid: true,
      name: '',
      nameRules: [
        v => !!v || 'Name is required',
        v => (v && v.length <= 32) || 'Name must contain 32 characters or fewer',
      ],
      ip: '',
      ipRules: [
        v => !!v || 'IP address is required',
        v => /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(v) || 'IP address must be valid',
      ],
      tempVariance: 0.0,
      phVariance: 0.0,
      varianceRules: [
        v => v >= 0 || 'Value must not be negative',
      ],
      notes: '',

      tempTimeSeriesID: -1,
      tempTimeSeriesDelay: 0,
      pHTimeSeriesID: -1,
      pHTimeSeriesDelay: 0,
      delayRules: [
        v => v >= 0 || 'Delay must not be negative',
      ],

      successSnackbar: false,
      updateErrorSnackbar: false,
      removeErrorSnackbar: false,

      confirmRemoval: false,
    }
  },
  created () {
    this.fetchDevice()
  },
  watch: {
    '$route': 'fetchDevice'
  },
  methods: {
    fetchDevice () {
      // Try to get the device by its MAC address as specified in the route
      this.$store.dispatch('getDeviceWhenAvailable', this.$route.params.mac).then((device) => {
        this.device = device;
        this.fillForm();
      }).catch(() => {
        // We couldn't find the device, so return to the main devices page
        this.$router.push('/devices');
      });
    },
    fillForm () {
      this.name = this.device.name;
      this.ip = this.device.ip;
      this.tempVariance = this.device.temp_variance;
      this.phVariance = this.device.ph_variance;
      this.notes = this.device.notes;
    },
    updateDevice () {
      this.$refs.create_form.validate();
      if (!this.valid) {
        return
      }
      this.axios.put(
        'http://'+location.host+'/api/devices/'+this.device.mac+'/',
        {
          mac: this.device.mac,
          name: this.name,
          ip: this.ip,
          temp_variance: this.tempVariance,
          ph_variance: this.phVariance,
          notes: this.notes
        }
      ).then(() => {
        this.$store.dispatch('updateDevices');
        this.successSnackbar = true;
      }).catch((error) => {
        console.log(error);
        this.updateErrorSnackbar = true;
      });
    },
    removeDevice () {
      // Hide the dialog
      this.confirmRemoval = false;
      this.axios.delete(
         'http://'+location.host+'/api/devices/'+this.device.mac+'/'
      ).then(() => {
        // We've removed the device from the database, so remove it from the store
        this.$store.commit('removeDevice', this.device)
        // Then update the store just to make sure that we're in sync
        this.$store.dispatch('updateDevices');
        // Return to the main devices screen
        this.$router.push('/devices')
      }).catch((error) => {
        console.log(error);
        this.removeErrorSnackbar = true;
      });
    },
    applyTimeSeries () {
      if(this.tempTimeSeriesID >= 0 && this.pHTimeSeriesID >= 0) {
        var timeSeriesFormData = new FormData();
        timeSeriesFormData.set('ph_id', this.pHTimeSeriesID);
        timeSeriesFormData.set('ph_delay', this.pHTimeSeriesDelay);
        timeSeriesFormData.set('temp_id', this.tempTimeSeriesID);
        timeSeriesFormData.set('temp_delay', this.tempTimeSeriesDelay);

        this.axios.post(
           'http://'+location.host+'/api/devices/'+this.device.mac+'/time_series/',
          timeSeriesFormData,
          {headers: {'Content-Type': 'multipart/form-data'}}
        ).then((response) => {
          console.log(response);
          this.successSnackbar = true;
        }).catch((error) => {
          console.log(error);
          this.updateErrorSnackbar = true;
        });
      }
    },
  }
}
</script>

<style>
  html {
    overflow-y: hidden;
  }
</style>