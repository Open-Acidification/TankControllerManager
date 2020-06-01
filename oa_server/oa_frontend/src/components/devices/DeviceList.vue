<template>
  <v-navigation-drawer
    :expand-on-hover="!($route.path == '/devices')"
    width=400
    permanent
  >
    <v-list
      class="overflow-hidden"
      dense
    >
      <div
        v-for="device in this.$store.state.devices"
        :key="device.mac"
      >
        <v-list-item :to="{path: '/devices/'+device.mac}" two-line>
          <v-list-item-content>
            <v-list-item-title class="headline mb-1">{{ device.name }}</v-list-item-title>
            <v-list-item-subtitle>
              {{ device.mac }}
            </v-list-item-subtitle>
            <div>
              <v-icon v-if="device.status == 0" color="error">mdi-close-network</v-icon>
              <v-icon v-else-if="device.status == 1" color="success">mdi-check-network</v-icon>
              <v-icon v-else color="warning">mdi-help-network</v-icon>
            </div>
          </v-list-item-content>
        </v-list-item>
        <v-divider/>
      </div>
      <v-btn large color="green lighten-1" block>Add Device</v-btn>
    </v-list>
  </v-navigation-drawer>
</template>

<script>

export default {
  name: 'DeviceList',
}
</script>

<style>

</style>