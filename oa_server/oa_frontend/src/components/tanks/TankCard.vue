<template>
  <v-card
    class="mb-2"
    :to="{path: '/tanks/'+tank.tankid}"
    style="white-space: nowrap;"
    min-width="400"
  >
    <v-container>
      <v-row class="align-center pa-0" no-gutters>
        <v-col>
          <v-card-text class="pt-0">
            <span class="title">{{addZero(tank.tankid)}} (Tank ID)</span>
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
      <v-row no-gutters v-if="'sparklines' in tank">
        <v-col>
          <v-sheet
            class="ml-1"
            :color="rgbArrayToCSS(blendColors([[50,175,0],[255,198,0],[187,36,0]], tank.temp_danger))"
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
            :color="rgbArrayToCSS(blendColors([[50,175,0],[255,198,0],[187,36,0]], tank.pH_danger))"
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
  props: ['tank'],
  methods: {
    addZero: function (i) {
      if (i < 10) {
        i = "0" + i;
      }
      return i;
    },
    /*
    Takes an array of colors, each represented as an array of three elements: red, green, and blue.
    Returns a color in between two colors, as specified by point. For example, point=0.5 would give
    the color halfway in between colors[0] and colors[1].
    */
    blendColors: function(colors, point) {
      // We don't want point to be negative
      point = Math.abs(point);

      var indexLow = Math.floor(point);
      var indexHigh = indexLow + 1;
      var fade = point - indexLow;

      // Our point is above our last color, so return it
      if (indexHigh >= colors.length) {
        return colors[colors.length - 1];
      }

      var colorLow = colors[indexLow];
      var colorHigh = colors[indexHigh];
      var colorNew = [0, 0, 0];

      for (var i; i < 3; i++) {
        var difference = colorHigh[i] - colorLow[i];
        colorNew[i] = colorLow[i] + difference * fade;
      }
      
      return colorNew;
    },
    rgbArrayToCSS: function(color) {
      return "rgb("+color[0]+","+color[1]+","+color[2]+")";
    }
  }
}
</script>

<style>

</style>