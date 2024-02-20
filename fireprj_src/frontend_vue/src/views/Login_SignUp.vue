<template>
  <v-card class="elevation-12 vc-pos">
    
  </v-card>
</template>

<script>
export default {
  components: {},
  methods: {
   },
  mounted() {
  },
  data() {
    return {
     };
  }
};
</script>

<style lang="scss" scoped>
  .login-container {
    position: relative;
  }
  .login-title {
    position: absolute;
    top: -100px; left: -32px;
    background-color: white;
    font-size: 40px;
    padding: 2px 20px;
    font-weight: 100;
  }
  .term-preview {
    // padding: 10px;
    border: 1px solid #606060;
    font-size: 10px;
    overflow-x: hidden;
    overflow-y: scroll;
    height: 500px;
  }

  .report-cont {
    height: 100vh;
    margin-left:20px;
    overflow-y: auto;

    .report-inner {
      padding: 0px 10px;
    }

    &::-webkit-scrollbar { width: 2px; }
    &::-webkit-scrollbar-thumb { background-color: rgba(0,0,0,0.2); }
  }

  .user-info-close {
    position: absolute;
    top: 10px; right: 0px
  }
  .u-width{
    width: 800px;
  }
  .vc-pos{
    width: 1000px;
  }
</style>
