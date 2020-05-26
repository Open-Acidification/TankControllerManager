<template>
  <v-content v-if="device" class="pa-4 ma-0 fill-height">
    <h3>
      Configure device with MAC address {{ device.mac }}:
    </h3>
    <v-form
      ref="update_form"
      v-model="valid"
      lazy-validation
    >
      <v-text-field
        v-model="name"
        :counter="32"
        :rules="nameRules"
        label="Name"
        required
      />
      <v-text-field
        v-model="ip"
        :rules="ipRules"
        label="IP Address"
        required
      />
      <v-textarea
          v-model="notes"
          label="Notes"
      />
      <v-btn
        :disabled="!valid"
        color="success"
        class="mr-4"
        @click="updateDevice"
      >
        Update Device
      </v-btn>
      <v-btn
        color="error"
        class="mr-4"
        @click="resetForm"
      >
        Reset Form
      </v-btn>
    </v-form>
  </v-content>
</template>

<script>

export default {
  name: 'DeviceConfig',
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
      notes: '',
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
      this.device = this.$store.getters.getDevice(this.$route.params.mac);
      this.fillForm();
    },
    resetForm () {
      this.fillForm();
    },
    fillForm () {
      this.name = this.device.name;
      this.ip = this.device.ip;
      this.notes = this.device.notes;
    },
    updateDevice () {
      this.axios.put(
        'http://localhost:8080/api/devices/'+this.device.mac+'/',
        {
          "mac": this.device.mac,
          "name": this.name,
          "ip": this.ip,
          "notes": this.notes
        }
      ).then(response => {
        console.log(response);
        this.$store.dispatch('updateDevices');
      }).catch(function (error) {
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