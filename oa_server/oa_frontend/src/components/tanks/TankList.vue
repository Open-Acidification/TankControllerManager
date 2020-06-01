<template>
  <v-navigation-drawer
    :expand-on-hover="!($route.path == '/tanks')"
    width=400
    permanent
  >
    <v-list
      class="overflow-hidden"
      dense
    >
      <div
        v-for="tank in this.$store.state.tanks"
        :key="tank.tankid"
      >
        <TankCard :tank="tank"/>
      </div>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import TankCard from './TankCard.vue'

export default {
  name: 'TankList',

  components: {
    TankCard,
  }
}
</script>

<style>

</style>