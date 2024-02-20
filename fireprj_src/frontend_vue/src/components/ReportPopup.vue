<template>
  <v-dialog
    v-model="value"
    width="500">

    <v-card>
      <v-card-title>
        장애가 발생한 단말기가 있습니다
      </v-card-title>

      <v-card-text>
        <slot />
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" text @click="close">
          확인
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: ['value'],
  methods: {
    close () {
      this.$emit('input', false)
    }
  },
  watch: {
    value: {
      handler (v) {
        if (v && this.$session.settings.dashboard.enable_alarm_sound) {
          this.$session.$emit('bell')
        }
      }
    }
  },
  data () {
    return {
    }
  }
}
</script>