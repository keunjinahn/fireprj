<template>
  <v-main class="login-main">
    <v-container class="fill-height" color="transparent" fluid>
      <v-row align="center" justify="center">
        <v-col cols="12" sm="12" md="7">
          <div class="login-container">
            <router-view />
          </div>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<style lang="scss" scoped>
  .login-main {
    background-color: #E6EEFF !important;
    background-image: url('~@/assets/bg/bg-2.jpg');
    background-size: cover;
    background-position: center center;
  }
  .rain-background {
    margin: auto;
    background: #417cb7;
    display: block;
    z-index: 0;
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 50vh;
    overflow: hidden;
  }
  .rain-background-bottom {
    margin: auto;
    display: block;
    z-index: 0;
    position: absolute;
    top: 20vh; left: 0; right: 0;
    height: 80vh;
    overflow: hidden;
    background-image: url(../assets/bg/background.jpg);
    background-size: cover;
    background-position: center center;
    opacity: 0.5;
  }
  .login-container {
    position: relative;
  }
  .login-title {
    position: fixed;
    top: 35px; left: auto;
    color: #606060;
    font-size: 16px;
    font-weight: 400;
    padding: 2px 20px;
    
    display: flex;
    justify-content: space-around;
    align-items: center;

    img {
      padding: 8px 10px 8px 0;
      margin: 6px 8px 6px 0;
    }
  }
</style>
