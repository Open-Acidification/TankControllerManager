<template>
  <v-card
    class="mb-2"
    :to="{path: '/tanks/'+tank.tankid}"
    style="white-space: nowrap;"
    min-width="400"
  >
    <v-container>
      <v-row class="align-center" no-gutters>
        <v-col>
          <v-card-text class="pt-0">
            <span class="title">Tank {{addZero(tank.tankid)}}</span>
          </v-card-text>
        </v-col>
        <v-col class="text-right">
          <v-card-text class="pt-0">
            <span class="caption">Last updated 
              {{addZero(tank.last_update.getHours())}}:{{addZero(tank.last_update.getMinutes())}} 
              ({{tank.minutes_ago}} minutes ago)</span>
          </v-card-text>
        </v-col>
      </v-row>
      <v-row class="text-center" no-gutters>
        <v-col>
          <v-card-text class="pt-0">
            <span class="subtitle-2">Temperature: {{tank.temp}} °C</span><br>
            <span class="subtitle-2">(Setpoint: {{tank.temp_setpoint}} °C)</span>
          </v-card-text>
        </v-col>
        <v-col>
          <v-card-text class="pt-0">
            <span class="subtitle-2">pH: {{tank.pH}}</span><br>
            <span class="subtitle-2">(Setpoint: {{tank.pH_setpoint}})</span>
          </v-card-text>
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col>
          <v-sheet
            class="mr-1"
            color="success"
            elevation="4"
            dark
          >
            <v-sparkline
              :value="tank.sparklines.temp"
              color="white"
              line-width="2"
              padding="16"
            />
          </v-sheet>
        </v-col>
        <v-col>
          <v-sheet
            class="ml-1"
            color="warning"
            elevation="4"
            dark
          >
            <v-sparkline
              :value="tank.sparklines.pH"
              color="white"
              line-width="2"
              padding="16"
            />
          </v-sheet>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>

export default {
  name: 'TankCard',
  props: ["tank"],
  methods: {
    addZero: function (i) {
      if (i < 10) {
        i = "0" + i;
      }
      return i;
    }
  }
}
</script>

<style>

</style>