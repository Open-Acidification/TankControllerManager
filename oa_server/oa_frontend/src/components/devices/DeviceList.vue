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
        dense
      >
        <v-toolbar-title>{{ device.name }}</v-toolbar-title>

        <v-spacer></v-spacer>

        <v-btn icon>
          <v-icon>mdi-poll</v-icon>
        </v-btn>
        <v-btn icon>
          <v-icon>mdi-settings</v-icon>
        </v-btn>
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