<template>
  <v-card class="elevation-12 v-container">
    <v-subheader>이메일을 입력하시면 비밀번호 초기화 메일이 발송됩니다</v-subheader>
    <v-divider/>
    <div class="user-container">
      <abl-document class="user-page">
        <table class="password-init-table-user">
          <colgroup>
            <col style="width:20%"/>
          </colgroup>
          <tr>
            <th class="s-h" colspan="2">아이디</th>
            <td colspan="3"><input type="text" class="abl-input-a" v-model="user.user_id"  onKeyup="this.value=this.value.replace(/[^a-z0-9]/g,'');">
              <div style="margin-top: 10px">
                <span>@koies.or.kr</span>
              </div>
            </td>
          </tr>
          <tr>
            <th class="s-h" colspan="2">성명</th>
            <td colspan="3"><input type="text" class="abl-input-a" v-model="user.user_name"></td>
          </tr>
          <tr>
            <th class="s-h" colspan="2">전화번호</th>
            <td colspan="3">
              <div >
                <div >
                  <input type="text" class="abl-input-d" v-model="user.user_telephone_1" :minlength="3" :maxlength="3" onKeyup="this.value=this.value.replace(/[^0-9]/g,'');" />
                </div>
                <div >
                  <input type="text" class="abl-input-d" v-model="user.user_telephone_2" :minlength="3" :maxlength="4" onKeyup="this.value=this.value.replace(/[^0-9]/g,'');" />
                </div>
                <div >
                  <input type="text" class="abl-input-d" v-model="user.user_telephone_3" :minlength="4" :maxlength="4" onKeyup="this.value=this.value.replace(/[^0-9]/g,'');" />
                </div>
              </div>
            </td>
          </tr>
        </table>
        <br>

        <table class="abl-table-user-bottom">
          <colgroup>
            <col style="width:10%"/>
            <col style="width:90%"/>
          </colgroup>
          <tr>
            <td colspan="1">
              <v-btn depressed dark big
                     color="light-blue darken-2"
                     @click="$router.push({name: 'login'})">
                <div class="ml-1">취소</div>
              </v-btn>
            </td>
            <td colspan="1">
            </td>
            <td colspan="1">
              <v-btn depressed dark big
                     color="light-blue darken-2"
                     @click="submitPasswordInit()">
                <v-icon small>mdi-check</v-icon>
                <div class="ml-1">초기화 메일 발송</div>
              </v-btn>
            </td>
          </tr>
        </table>
      </abl-document>
    </div>
  </v-card>

<!--      <div class="pa-6">-->
<!--        <div class="mb-2">-->
<!--          <v-text-field outlined dense hide-details placeholder="사용자 이메일" type="email" />-->
<!--        </div>-->
<!--      </div>-->
<!--      <v-divider/>-->
<!--      <div class="d-flex justify-space-between">-->
<!--        <v-btn depressed text large @click="$router.push({name: 'login'})">-->
<!--          <v-icon>mdi-close</v-icon>-->
<!--          <div class="ml-1 line-height-hangul-fix">취소</div>-->
<!--        </v-btn>-->
<!--        <v-btn depressed text large-->
<!--          color="primary" -->
<!--          :loading="loading"-->
<!--          @click="submitAddMember()">-->
<!--          <div class="mr-1 line-height-hangul-fix">초기화 메일 발송</div>-->
<!--          <v-icon>mdi-check</v-icon>-->
<!--        </v-btn>-->
<!--      </div>-->
<!--    </template>-->
<!--    <template v-else-if="step === 1">-->
<!--      <div class="px-6 py-10 text-center">-->
<!--        <div class="mb-6 text-h4 font-weight-thin text-center">-->
<!--          초기화 메일 발송되었습니다-->
<!--        </div>-->
<!--        <v-btn text large color="primary" @click="$router.push({name: 'login'})">-->
<!--          로그인 화면으로 이동-->
<!--        </v-btn>-->
<!--      </div>-->
<!--    </template>-->
<!--    <template v-else>-->
<!--      잘못된 접근입니다-->
<!--    </template>-->
<!--  </v-card>-->
</template>

<script>
import Cookies from 'js-cookie'
export default {
  methods: {
    async submitPasswordInit () {
      let params = {}
      if (this.user.user_id.length < 4) {
        this.err_msg = '사용자 아이디를 확인해 주세요!'
        this.$session.$emit('modal-alert', this.err_msg)
        return
      }
      if (this.user.user_name.length < 2) {
        this.err_msg = '사용자 이름을 확인해 주세요!'
        this.$session.$emit('modal-alert', this.err_msg)
        return
      }
      if (this.user.user_telephone_1.length != 3
          || this.user.user_telephone_2.length != 4
          || this.user.user_telephone_3.length != 4
          || this.user.user_telephone_1 != '010'
      ) {
        this.err_msg = '전화번호나 핸드폰 번호를 확인해 주세요!'
        this.$session.$emit('modal-alert', this.err_msg)
        return
      }
      params.user_id = this.user.user_id
      params.user_name = this.user.user_name
      params.telephone = this.user.user_telephone_1.toString() + '-' + this.user.user_telephone_2.toString() + '-' + this.user.user_telephone_3.toString();
      let {data} = await this.$http.post(`user_password_init`, params)
      if(data.status == true){
        this.$session.$emit('modal-alert', '패스워드 초기화 메일을 발송하였습니다.')
        this.$router.push('/')
      }else{
        this.$session.$emit('modal-alert', '패스워드 초기화 메일을 발송이 실패하였습니다.')
        this.$router.push('/')
      }
      // if (data.email_result == 1) {
      //   this.$session.$emit('modal-alert', '패스워드 초기화 메일을 발송하였습니다.')
      //   this.$router.push('/')
      // } else if (data.email_result == 0) {
      //   this.$session.$emit('modal-alert', '이메일 전송을 실패하였습니다.')
      //   this.$router.push('/')
      // }
    }
  },
  data() {
    return {
      loading: false,
      step: 0,
      agreements: [false, false, false],

      form: {
        user_id: "",
        user_pw: ""
      },
      notices: [],
      popup: {
        show: false,
        data: null
      },
      remember: false,
      user: {
        user_id: "",
        user_name:'',
        user_telephone:'',
        user_telephone_1:'',
        user_telephone_2:'',
        user_telephone_3:'',
        user_email:'',
      },
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
  padding: 10px;
  border: 1px solid #dcdcdc;
  font-size: 10px;
  overflow: hidden;

  height: 80px;
}

.abl-page {
  padding: 15px 30px;
}

.password-init-table-user {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #a0a0a0;
  color:black;
  font-weight: normal;
  th, td {
    padding: 1px 1px;
    border: 1px solid #a0a0a0;
    font-size: 14px;
    height: 48px;
  }

  .m-h { background-color: #ebebeb; }
  .s-h { background-color: #ebebeb;height:30px;}
  .w-h { background-color: #ffffff; }
  .dbl-t { border-top: 3px double #a0a0a0; }
  .dbl-b { border-bottom: 3px double #a0a0a0; }
  .area-a { width: 80% !important;}
  .textarea-context {
    display: flex;
    min-height: 280px;
  }
  .s-h-1 {float:left;background-color: #ebebeb;border-right: 1px solid #a0a0a0;width:50%;height:200px!important;line-height: 30px;padding-top: 65px;}
  .s-h-2 {float:right;background-color: #ebebeb;border-bottom: 1px solid #a0a0a0;width:50%;height:100px!important;line-height: 30px;}
  .s-h-3-1 {background-color: #ebebeb;border-bottom: 1px solid #a0a0a0;width:100%;height:100%!important;}
  .s-h-3-2 {background-color: #ebebeb;width:100%;height:100%!important;}
  .s-h-4 {float:left;background-color: white;border-right: 1px solid #a0a0a0;width:50%;height:240px!important;}
  .s-h-4-0 {float:left;background-color: white;border-right: 0px solid #a0a0a0;width:50%;height:240px!important;}
  .s-h-4-1 {background-color: white;border-bottom: 1px solid #a0a0a0;width:100%;height:30px!important;}
  .s-h-4-2 {background-color: white;border-bottom: 0px solid #a0a0a0;width:100%;height:60px!important;}
  .abl-input {
    float:left;
    margin-left: 10px;
    width: 150px;
    height: 40px;
    background-color: #ffffff;
    //border: 1px solid #a0a0a0;
    &:hover, &:focus {
      background-color: #ebebeb;
    }
  }
  .abl-input-1 {
    float:left;
    margin-left: 10px;
    width: 50px;
    height: 40px;
    background-color: #ffffff;
    //border: 1px solid #a0a0a0;
    &:hover, &:focus {
      background-color: #ebebeb;
    }
  }
  .abl-input-a {
    float:left;
    padding-left: 10px;
    margin-top: 5px;
    margin-left: 10px;
    margin-right: 10px;
    width: 25%;
    height: 30px;
    background-color: #ffffff;
    border: 1px solid #aaaaaa;
    &:hover, &:focus {
      background-color: #ebebeb;
    }

  }
  .abl-input-b {
    float:left;
    padding-left: 10px;
    margin-top: 5px;
    margin-left: 10px;
    margin-right: 10px;
    width: 60%;
    height: 30px;
    background-color: #ffffff;
    border: 1px solid #aaaaaa;
    &:hover, &:focus {
      background-color: #ebebeb;
    }

  }
  .abl-input-d {
    float:left;
    padding-left: 10px;
    margin-top: 5px;
    margin-left: 10px;
    margin-right: 10px;
    width: 10%;
    height: 30px;
    background-color: #ffffff;
    border: 1px solid #aaaaaa;
    &:hover, &:focus {
      background-color: #ebebeb;
    }

  }
  .l-b{
    margin-top: 20px !important;
    height: 40px;
  }
  .b-empty{
    border: 0px;
  }
}
.abl-table-user-bottom {
  width: 100%;
  border-collapse: collapse;
  border: 0px solid #a0a0a0;
  color: black;
  font-weight: normal;

  th, td {
    padding: 1px 1px;
    border: 0px solid #a0a0a0;
    font-size: 14px;
    height: 48px;
  }
}
.s-left{
  text-align: left;
  margin-left: 10px;
}
.left-m-1{
  margin-left: 10px;
}
.user-info-close {
  position: relative;
  top: 10px; right: 0px;
  float:right;
  margin-right: 10px;
}
.v-c-size{
  width:80px;
  height:5px;
  text-align: center;
  margin-top: -15px;
  margin-left:35px;
}
.v-l-size{
  font-size: 14px;
  width:40px;
  text-align: center;
  margin-top: 0px;
  margin-left: -10px;
}
.v-l-size-2{
  font-size: 14px;
  width:100px;
  text-align: center;
  margin-top: 0px;
  margin-left: -10px;
}
.v-c-size-h{
  width:80px;
  height:5px;
  text-align: center;
  margin-top: -15px;
  margin-left:0px;
}
.ui-p-valide{
  font-size: 8px;
  color: red;
  margin-top: 10px !important;
}
.v-container{
  width:700px;
  margin-left: 263px;
  //display: flex;
  //justify-content: center;
  //align-items: center;
}
</style>
