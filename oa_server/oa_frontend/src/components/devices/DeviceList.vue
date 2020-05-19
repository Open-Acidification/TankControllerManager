<template>
  <v-navigation-drawer
    expand-on-hover
    width=400
    v-model="sidebar"
    permanent
  >
    <v-list
      class="overflow-hidden"
      dense
    >
      <v-card
        v-for="device in this.$store.state.devices"
        :key="device.mac"
      >
        <v-list-item two-line>
          <v-list-item-content>
            <v-list-item-title class="headline mb-1">{{ device.name }}</v-list-item-title>
            <v-list-item-subtitle>{{ device.mac }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-card-actions>
          <div>
            <v-icon v-if="device.status == 0" color="red accent-4">mdi-close-network</v-icon>
            <v-icon v-else-if="device.status == 1" color="light-green darken-3">mdi-check-network</v-icon>
            <v-icon v-else color="yellow darken-1">mdi-help-network</v-icon>
          </div>
          <v-spacer/>
          <v-btn icon>
            <v-icon>mdi-poll</v-icon>
          </v-btn>
          <v-btn :to="{path: '/devices/'+device.mac+'/configure'}" icon>
            <v-icon>mdi-wrench</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
      <v-btn large color="green" width=400>Add Device</v-btn>
    </v-list>
  </v-navigation-drawer>
</template>

<script>

export default {
  name: 'DeviceList',
  props: ["devices"],
}
</script>

<style>

</style>