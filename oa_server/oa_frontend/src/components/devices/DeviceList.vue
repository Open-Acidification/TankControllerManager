<template>
  <v-navigation-drawer permanent>
    <v-list
      dense
      nav
    >
      <v-toolbar
        v-for="device in devices"
        :key="device.mac"
        link
        extended
      >
        <v-toolbar-title>{{ device.name }}</v-toolbar-title>

        <template #extension>
          <v-btn icon>
            <v-icon>mdi-poll</v-icon>
          </v-btn>
          <v-btn icon>
            <v-icon>mdi-wrench</v-icon>
          </v-btn>
          <div v-if="device.online">
            <v-icon color="light-green darken-3">mdi-check-network</v-icon>
          </div>
          <div v-else>
            <v-icon color="red accent-4">mdi-close-network</v-icon>
          </div>
        </template>
      </v-toolbar>
    </v-list>
  </v-navigation-drawer>
</template>

<script>

export default {
  name: 'DeviceList',
  props: ["devices"]
}
</script>

<style>

</style>