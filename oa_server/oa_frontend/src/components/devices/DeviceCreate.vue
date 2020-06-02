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
              Add New Device
            </h3>
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
              @click="createDevice"
              block
            >
            <v-dialog v-model="creating" persistent max-width="60">
              <CenteredProgress/>
            </v-dialog>
              Create Device
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
      v-model="createErrorSnackbar"
      bottom
      right
    >
      Something went wrong with adding the device.
    </v-snackbar>
  </v-content>
</template>

<script>
import CenteredProgress from '../CenteredProgress.vue';

export default {
  name: 'DeviceCreate',

  components: {
    CenteredProgress,
  },

  data () {
    return {
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
      tempVariance: 5.0,
      phVariance: 1.0,
      varianceRules: [
        v => v >= 0 || 'Value must be positive',
      ],
      notes: '',

      createErrorSnackbar: false,

      creating: false,
    }
  },
  methods: {
    clearForm () {
      this.$refs.create_form.reset();
    },
    createDevice () {
      this.creating = true;
      this.axios.post(
        'http://localhost:8080/api/devices/',
        {
          ip: this.ip,
          name: this.name,
          temp_variance: this.tempVariance,
          ph_variance: this.phVariance,
          notes: this.notes
        }
      ).then((response) => {
        var mac = response.data.mac;
        this.$store.dispatch('updateDevices');
        this.$router.push('/devices/'+mac)
      }).catch((error) => {
        console.log(error);
        this.creating = false;
        this.createErrorSnackbar = true;
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