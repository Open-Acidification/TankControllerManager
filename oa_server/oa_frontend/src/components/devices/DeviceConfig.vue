<template>
  <v-content class="pa-4 ma-0 fill-height">
    <div v-if="device">
      <h3>
        Configure device with MAC address {{ device.mac }}:
      </h3>
      <v-form
        ref="update_form"
        v-model="valid"
        lazy-validation
      >
        <v-container>
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
                @click="resetForm"
                block
              >
                Reset Form
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
        v-model="errorSnackbar"
        bottom
        right
      >
        Something went wrong with updating device.
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
        v => v >= 0 || 'Value must be positive',
      ],
      notes: '',

      successSnackbar: false,
      errorSnackbar: false,
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
      this.$store.dispatch('waitForDevices').then(() => {
        this.device = this.$store.getters.getDevice(this.$route.params.mac);
        this.fillForm();
      });
    },
    resetForm () {
      this.fillForm();
    },
    fillForm () {
      this.name = this.device.name;
      this.ip = this.device.ip;
      this.tempVariance = this.device.temp_variance;
      this.phVariance = this.device.ph_variance;
      this.notes = this.device.notes;
    },
    updateDevice () {
      this.axios.put(
        'http://localhost:8080/api/devices/'+this.device.mac+'/',
        {
          "mac": this.device.mac,
          "name": this.name,
          "ip": this.ip,
          "temp_variance": this.tempVariance,
          "ph_variance": this.phVariance,
          "notes": this.notes
        }
      ).then(() => {
        this.$store.dispatch('updateDevices');
        this.successSnackbar = true;
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