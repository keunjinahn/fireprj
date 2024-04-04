<template>
  <div class="d-flex elevation-2 white">
    <div class="login-panel">
      <div class="login-panel-inner">
        <div class="login-legend">
          <h1>(주)리더스테크<br>통합 화재 감지 시스템</h1>
        </div>
        <div class="login-input-wrap">
            <div class="login-inner">
              <v-form>
                <div class="mb-4">
                  <v-text-field outlined dense hide-details
                    v-model="form.username"
                    label="아이디"
                    name="username"
                    type="text"
                    prepend-inner-icon="person"
                    @keypress.enter="login"
                  />
                </div>
                <div>
                  <v-text-field outlined dense hide-details
                    v-model="form.password"
                    id="password"
                    label="비밀번호"
                    name="password"
                    prepend-inner-icon="lock"
                    type="password"
                    @keypress.enter="login"
                  />
                </div>
                <br>
                <div class="mb-4 btn-center">
                  <v-btn width="250" height="50" color="primary" @click="login" :loading="loading">로그인</v-btn>
                </div>                
              </v-form>
            </div>
        
        </div>
     
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    async login() {
      if (!this.form.username || !this.form.password)
        return (this.error = '아이디와 패스워드를 입력해 주세요.')

      this.loading = true
      try {
        let {data} = await this.$http.post('login', this.form)
        if (data.status) {
          this.$session.login(data)
          await this.$session.setToken(data.user)
          this.$router.push('/sensor_log_event')
        }else {
          if (data.reason == 1) {
            alert('로그인이 실패(아이디를 확인하여주세요!)')
          } else if (data.reason == 2) {
            alert('로그인이 실패(패스워드를 확인하여주세요!)')
          }
        }
        return data
      }
      catch (err) {
        this.error = err.message
      }
      finally {
        this.loading = false
      }
      this.$router.replace({name: 'sensor_log_event'})
    }
  },
  data(){
    return {
      loading: false,
      form: {
        username: '',
        password: ''
      },
      error: null,
    };
  }
}
</script>

<style lang="scss" scoped>
  .notice-content {
    white-space: pre-line;
  }
  .login-panel-inner {
    width: 380px;
  }
  .login-input-wrap {
  }
  .login-fn-btn {
    min-width: 100px;
    text-align: center;
  }
  .notice-wrap {
    padding: 48px;
    overflow: hidden;
    background-color: #DFEFF7;
    //background-image: url(~@/assets/bg/bg-3.svg);
    background-size: contain;
    background-position: left bottom;
    flex: 1 1 50%;
  }
  .notice-header {
    font-family: 'Noto Sans KR';
    font-style: normal;
    font-weight: bold;
    font-size: 16px;
    line-height: 23px;
    letter-spacing: -0.04em;

    padding-bottom: 10px;
    border-bottom: 1px solid white;
  }
  .notice {
    // 배경을 넣으시려면 이부분 주석을 해제하시면 됩니다
    // background-image: url(../assets/bg/bg-1.jpg);
    // background-size: cover;
    // background-position: center center;
  }
  .cloud-img {
    width: 538px;
  }
  .login-panel {
    overflow: hidden;
    flex: 1 1 50%;
    padding: 60px 0;
    min-width: 500px;
    display: flex;
    justify-content: center;
    align-items: center;

  }
  .login-legend {
    text-align: center;
    margin-left: -40px;
    margin-bottom: 40px;
  }
  .login-legend-1 {
    font-family: 'Noto Sans KR';
    font-style: normal;
    font-weight: bold;
    font-size: 24px;
    line-height: 35px;
    letter-spacing: -0.04em;
  }
  .login-legend-2 {
    font-family: 'Noto Sans KR';
    font-style: normal;
    font-weight: normal;
    font-size: 12px;
    line-height: 17px;
  }
  .v-list-w{
    max-width: 300px;
  }
  .disabled {
    opacity: 0.5;
    pointer-events: none;
  }


  .notice-list-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 4px 0;
    padding-left: 12px;

    font-size: 12px;
    color: #404040;

    cursor: pointer;
    position: relative;
  }
  .notice-list-item-title {
    &:before {
      position: absolute;
      content: "•";
      font-size: 18px;
      top: 9px; left: 0px;
      line-height: 0;
    }
  }
  .notice-list-item-date {
    font-size: 11px;
  }
.gif-center{
  display: block;
  margin: 0 auto;
}
.btn-center{
  text-align: center;
}
</style>
