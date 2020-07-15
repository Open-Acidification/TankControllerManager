<script>
import { Line } from 'vue-chartjs'

export default {
  name: 'TankChart',
  extends: Line,
  props: ['chartdata', 'options'],
  mounted () {
    this.renderChart(this.chartdata, this.options)
  }
}
</script>

<style>
</style>