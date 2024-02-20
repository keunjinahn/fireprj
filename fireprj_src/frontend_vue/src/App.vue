<template>
  <div id="app">
    <v-app id="environ-app">
      <router-view/>
      <modal />
      <v-dialog v-model="dialog.show" max-width="500px">
        <v-card>
          <v-card-title>{{dialog.message}}</v-card-title>
          <v-card-actions>
            <v-btn tile depressed class="flex-grow-1" @click="dialog.show = false">확인</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-app>
  </div>
</template>

<script>
import Modal from '@/components/Modal'
export default {
  components: {Modal},
  mounted () {
    this.$session.$on('dialog', params => {
      this.dialog.show = params.show
      this.dialog.message = params.message || ''
    })
  },
  data () {
    return {
      dialog: {
        show: false,
        message: ''
      }
    }
  }
}
</script>

<style lang="scss">
  #environ-app > .v-application--wrap { width: 100% }
  #environ-app .v-data-table td {height: 42px}

  .clickable-row {
    user-select: none;
    cursor: pointer;
  }

  
  .detail-enter-active { transition: transform .5s}
  .detail-leave-active {transition: transform .5s}
  .detail-enter {transform: translateX(370px)}
  .detail-leave-to {transform: translateX(370px)}
  .line-height-hangul-fix { margin-top: 1px; }
</style>
