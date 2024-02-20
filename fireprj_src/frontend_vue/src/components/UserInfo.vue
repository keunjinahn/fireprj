<template>
  <div style="width: 1000px">
    <v-btn v-show="this.call_type.regist" fab x-small dark depressed color="grey darken-1" class="user-info-close" @click="$router.push('/')">
      <v-icon>mdi-close</v-icon>
    </v-btn>
    <v-card :loading="loading" :disabled="loading">
      <v-subheader>{{getSummitString()}}</v-subheader>
      <v-divider/>
      <div class="user-container">
        <abl-document class="user-page" :key="user.id">
          <table class="abl-table-user">
            <colgroup>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
            </colgroup>
            <tr>
              <th class="s-h" colspan="3">회원구분</th>
              <td colspan="3" >
                <v-checkbox
                    v-model="member_user_type[1].check"
                    :label="''"
                    class="shrink v-c-size" @change="onUserTypeChage(1)">
                  <template v-slot:input>
                    <input type="checkbox" class="v-c-size">
                  </template>
                  <template v-slot:label>
                    <span class="v-l-size-2" >{{member_user_type[1].name}}</span>
                  </template>
                </v-checkbox>
              </td>
              <td colspan="3">
                <v-checkbox
                    v-model="member_user_type[2].check"
                    :label="''"
                    class="shrink v-c-size"  @change="onUserTypeChage(2)">
                  <template v-slot:input>
                    <input type="checkbox" class="v-c-size">
                  </template>
                  <template v-slot:label>
                    <span class="v-l-size-2" >{{member_user_type[2].name}}</span>
                  </template>
                </v-checkbox>
              </td>
              <td colspan="3">
                <v-checkbox
                    v-model="member_user_type[3].check"
                    :label="''"
                    class="shrink v-c-size"  @change="onUserTypeChage(3)">
                  <template v-slot:input>
                    <input type="checkbox" class="v-c-size">
                  </template>
                  <template v-slot:label>
                    <span class="v-l-size-2" >{{member_user_type[3].name}}</span>
                  </template>
                </v-checkbox>
              </td>
            </tr>
            <tr>
              <th class="s-h" colspan="3">추가정보</th>
              <td colspan="9">
                <v-container fluid>
                  <v-row align="center">
                    <v-col class="d-flex" cols="12" sm="3">
                      <v-select solo dense hide-details light
                                v-model="user.selected_area_type"
                                :items="member_area_type"
                                placeholder="-"
                                :disabled="!member_user_type[2].check "
                                class="s-size"
                                @change="onChangeAreaType()"
                      >
                      </v-select>
                    </v-col>
                  </v-row>
                </v-container>
              </td>
            </tr>
            <tr>
              <th class="s-h" colspan="3">아이디</th>
              <td colspan="9"><input type="text" :disabled="call_type.myinfo || call_type.userlist_modify " class="abl-input-b" v-model="user.user_id" @change="user.overlab_result=0" onKeyup="this.value=this.value.replace(/[^a-z0-9]/g,'');">
                <span>@koies.or.kr</span>
                <v-btn v-show="call_type.regist" depressed dark big
                       color="light-blue darken-2"
                       class="left-m-1"
                       @click="onUserOverlabCheck()"
                >
                  <v-icon small>mdi-account-check</v-icon>
                  <div>중복확인</div>
                </v-btn>
                <v-btn depressed dark big disabled
                       color="light-blue darken-2"
                       class="left-m-1"
                       @click="onUserEmailAuth()"
                >
                  <v-icon small>mdi-email-check</v-icon>
                  <div >이메일인증</div>
                </v-btn>
              </td>
            </tr>
            <tr v-show="call_type.userlist_modify">
              <th class="s-h" colspan="3">최근로그인</th>
              <td colspan="9"><span class="s-left">{{user.last_logon_time | moment('YYYY-MM-DD HH:mm:ss')}}</span></td>
            </tr>
            <tr v-show="call_type.userlist_modify">
              <th class="s-h" colspan="3">비밀번호 변경일</th>
              <td colspan="9"><span class="s-left">{{user.password_date | moment('YYYY-MM-DD HH:mm:ss')}}</span></td>
            </tr>
            <tr>
              <th class="s-h" colspan="3">비밀번호</th>
              <td colspan="9"><input type="password" class="abl-input-b" placeholder="*****" v-model="user.user_passwd" />
                <span class="ui-p-valide">※ 영문 대소문자, 숫자, 특수문자를 포함한 8-12자(한글 및 띄어쓰기 없음, 특수문자 !@#$% 허용)</span>
              </td>
            </tr>
            <tr>
              <th class="s-h" colspan="3">비밀번호 확인</th>
              <td colspan="9"><input type="password" class="abl-input-b" placeholder="*****" v-model="user.user_passwdc" /></td>
            </tr>
            <tr>
              <th class="s-h" colspan="3">성명</th>
              <td colspan="3"><input type="text" class="abl-input-c" v-model="user.user_name"></td>
              <th class="s-h" colspan="3">부서명</th>
              <td colspan="3"><input type="text" class="abl-input-c" v-model="user.dept_name" /></td>
            </tr>
            <tr>
              <th class="s-h" colspan="3">전화번호</th>
              <td colspan="3" >
                <div >
                  <div >
                    <input type="text" class="abl-input-d" v-model="user.user_phone_1" :minlength="3" :maxlength="3" onKeyup="this.value=this.value.replace(/[^0-9]/g,'');" />
                  </div>
                  <div>
                    <span></span>
                  </div>
                  <div>
                    <input type="text" class="abl-input-d" v-model="user.user_phone_2" :minlength="4" :maxlength="4" onKeyup="this.value=this.value.replace(/[^0-9]/g,'');"  />
                  </div>
                  <div>
                    <span></span>
                  </div>
                  <div>
                    <input type="text" class="abl-input-d" v-model="user.user_phone_3" :minlength="4" :maxlength="4" onKeyup="this.value=this.value.replace(/[^0-9]/g,'');" />
                  </div>
                </div>
              </td>
              <th class="s-h" colspan="3">핸드폰번호</th>
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
            <tr v-show="!this.call_type.regist">
              <th class="s-h" colspan="3">승인 상태</th>
              <td colspan="9">
                <v-container fluid>
                  <v-row align="center">
                    <v-col class="d-flex" cols="12" sm="3">
                      <v-select solo dense hide-details light
                                v-model="user.selected_user_status"
                                :items="member_user_status"
                                placeholder="대기/승인"
                                class="s-size"
                                :disabled="call_type.myinfo"
                                @change="onChangeUserStatus()"
                      >
                      </v-select>
                    </v-col>
                  </v-row>
                </v-container>
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
                <v-btn v-if="!this.call_type.regist" depressed dark big
                       color="light-blue darken-2"
                       :disabled="$session.hasPermission([1])"
                       @click="onExitUser()">
                  <v-icon small>mdi-account-remove</v-icon>
                  <div class="ml-1">탈퇴</div>
                </v-btn>
              </td>
              <td colspan="1">
              </td>
              <td colspan="1">
                <v-btn depressed dark big
                       color="light-blue darken-2"
                       @click="submitMember()">
                  <v-icon small>mdi-check</v-icon>
                  <div class="ml-1">{{getSummitString()}}</div>
                </v-btn>
              </td>
            </tr>
          </table>
          <!--                       :disabled="!(agreements[0] && agreements[1] && agreements[2])"-->
        </abl-document>
      </div>
    </v-card>
    <v-dialog v-model="popup.exit_user.show" max-width="500px">
      <v-card>
        <v-card-title>회원 탈퇴 하시겠습니까?</v-card-title>
        <v-card-actions>
          <v-btn tile depressed class="flex-grow-1" @click="exitUser()">탈퇴</v-btn>
          <v-btn tile depressed class="flex-grow-1" @click="popup.exit_user.show = false">취소</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="popup.del_user.show" max-width="500px">
      <v-card>
        <v-card-title>선택한 사용자를 삭제하시겠습니까?</v-card-title>
        <v-card-actions>
          <v-btn tile depressed class="flex-grow-1" @click="deleteUser()">삭제</v-btn>
          <v-btn tile depressed class="flex-grow-1" @click="popup.del_user.show = false">취소</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="popup.deleted_user.show" max-width="500px">
      <v-card>
        <v-card-title>유저가 삭제되었습니다.</v-card-title>
        <v-card-actions>
          <v-btn tile depressed class="flex-grow-1" @click="popup.deleted_user.show = false">확인</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="popup.relogin.show" max-width="500px">
      <v-card>
        <v-card-title>다시 로그인하여 주십시오</v-card-title>
        <v-card-actions>
          <v-btn tile depressed class="flex-grow-1" @click="onReLogin()">획인</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import AblDocument from '@/components/AblDocument'
export default {
  props: {
    userinfo: { type: Object, required: true },
    call_type: { type: Object, required: true }
  },
  components: {AblDocument},
  methods: {
    onUserTypeChage(index){
      this.member_user_type.forEach(v => v.check = false)
      this.member_user_type[index].check = true
      if(this.member_user_type[2].check != true ){
        this.user.selected_area_type = null
        this.user.r_area_code = null
      }
    },
    onChangeAreaType(){
      this.user.r_area_code=this.user.selected_area_type
    },
    onChangeUserStatus(){
      this.user.r_user_status=this.user.selected_user_status
    },
    onChangeCheckStauts1(item){
      this.users.data[this.users.data.indexOf(item)].user_status_1 = (item.user_status_0 == true)? false:true
      this.users.data[this.users.data.indexOf(item)].user_status = (item.user_status_0 == true)? 0:1
      this.users.selected.forEach( function(v) {
        if(v == item) {
          v.user_status = item.user_status;
        }
      })
    },
    onChangeCheckStauts2(item){
      this.users.data[this.users.data.indexOf(item)].user_status_0 = (item.user_status_1 == true)? false:true
      this.users.data[this.users.data.indexOf(item)].user_status = (item.user_status_1 == true)? 1:0
      this.users.selected.forEach( function(v) {
        if(v == item) {
          v.user_status = item.user_status;
        }
      })
    },
    onSelectedChnage(){
      this.users.data.forEach(v=>v.enable=false)
      this.users.selected.forEach(v=>v.enable=true)
    },
    async applyUserStatus(){

      for(var i=0;i<this.users.selected.length;i++){
        for(var j=0;j<this.users.data.length;j++){
          if(this.users.selected[i].user_id == this.users.data[j].user_id){
            let params = {}
            params.user_id = this.users.data[j].user_id;
            params.user_status = this.users.data[j].user_status
            await this.$http.patch(`users/${this.users.data[j].id}`, params)
          }
        }
      }
      this.getUsers(this.type_tab_items[this.selected_tab_item])
      this.users.selected = []
    },
    async onUserOverlabCheck(){
      if(this.user.user_id.length < 4){
        this.$session.$emit('modal-alert', '사용자 아이디를 확인해주세요!')
        return
      }
      this.loading = true;
      try {
        let params = {user_id: this.user.user_id}
        let {data} = await this.$http.post('login_overlap',params )
        if(data.status == true){
          if(data.overlap_result == 0){
            this.$session.$emit('modal-alert', '사용할수 없는 아이디 입니다.!')
            return
          }else{
            this.$session.$emit('modal-alert', '사용가능한 아이디 입니다.!')
          }
          this.user.overlab_result = data.overlap_result
        }
      } catch (e) {
        this.$session.$emit('modal-alert', e.toString())
      } finally {
        this.loading = false;
      }
    },
    getSummitString(){
      if(this.call_type.myinfo)
        return "내정보 수정"
      if(this.call_type.regist)
        return "회원등록 신청"
      if(this.call_type.userlist_add)
        return "회원추가"
      if(this.call_type.userlist_modify)
        return "회원수정"
    },
    onExitUser(){
      if(this.call_type.myinfo)
        this.popup.exit_user.show=true
      else if(this.call_type.userlist_modify)
        this.popup.del_user.show=true
    },
    async exitUser(){
      await this.$http.delete(`users/${this.userinfo.id}`)
      this.$session.logout()
    },
    async deleteUser() {
      await this.$http.delete(`users/${this.userinfo.id}`)
      this.$session.$emit('modal-alert', '삭제되었습니다.')
      this.popup.del_user.show = false
      if(this.call_type.userlist_modify)
        this.$emit('refresh_list')
    },
    async submitMember() {


      let params = {}
      if(!this.call_type.regist)
        params.id = this.userinfo.id;



      if(this.call_type.regist) {
        if(this.user.user_id.length < 4){
          this.err_msg = '사용자 아이디를 확인해 주세요!'
          this.$session.$emit('modal-alert', this.err_msg)
          return
        }
        if(this.user.overlab_result == 0){
          this.err_msg = '아이디 중복체크를 확인해 주세요!'
          this.$session.$emit('modal-alert', this.err_msg)
          return
        }
        if(this.user.user_name.length < 2){
          this.err_msg = '사용자 이름을 확인해 주세요!'
          this.$session.$emit('modal-alert', this.err_msg)
          return
        }
        if(this.user.dept_name.length < 2){
          this.err_msg = '부서명을 확인해 주세요!'
          this.$session.$emit('modal-alert', this.err_msg)
          return
        }
        params.user_id = this.user.user_id;
      }

      if (this.call_type.regist && !this.user.user_passwd){
        this.err_msg = '비밀번호를 확인해 주세요!'
        this.$session.$emit('modal-alert', this.err_msg)
        return
      }
      else {
        if(this.user.user_passwd.length > 0) {
          if (this.user.user_passwd.length < 8 || this.user.user_passwd.length > 12) {
            this.err_msg = '비밀번호를 확인해주세요!'
            this.$session.$emit('modal-alert', this.err_msg)
            return
          }
          if (!/^[a-zA-Z0-9~!@#$%^&*()_+|<>?:{}]+$/.test(this.user.user_passwd)) {
            this.err_msg = '비밀번호를 확인해주세요!'
            this.$session.$emit('modal-alert', this.err_msg)
            return
          }
          if (this.user.user_passwd !== this.user.user_passwdc) {
            this.err_msg = '비밀번호를 확인해주세요!'
            this.$session.$emit('modal-alert', this.err_msg)
            return
          }
        }
      }

      if(this.call_type.myinfo || this.call_type.userlist_modify || this.call_type.regist) {

        params.area_code = this.user.r_area_code
        params.user_status = this.user.r_user_status
        for (var i = 0; i < this.member_user_type.length; i++) {
          if (this.member_user_type[i].check == true) {
            params.user_type = i + 1
            break
          }
        }
        if(params.user_type == 3 && (params.area_code == 'R000' || params.area_code == null)){ // 권역별지부는 추가정보 필수 선택
          this.err_msg = '추가정보를 확인해주세요!'
          this.$session.$emit('modal-alert', this.err_msg)
          return
        }
      }

      if(this.user.user_passwd.length >=8)
        params.user_passwd = this.user.user_passwd;

      if(this.user.user_telephone_1.length !=3
          || this.user.user_telephone_2.length !=4
          || this.user.user_telephone_3.length !=4
          || this.user.user_phone_3.length !=4
          || this.user.user_telephone_1 != '010'
          || this.user.user_phone_1.length <2
          || this.user.user_phone_1.length >3
          || this.user.user_phone_2.length <3
          || this.user.user_phone_2.length >4
      ){
        this.err_msg = '전화번호나 핸드폰 번호 자리수를 확인해 주세요!'
        this.$session.$emit('modal-alert', this.err_msg)
        return
      }

      params.user_name = this.user.user_name;
      params.phone = this.user.user_phone_1.toString() + '-' + this.user.user_phone_2.toString() + '-' + this.user.user_phone_3.toString();
      params.telephone = this.user.user_telephone_1.toString() + '-' + this.user.user_telephone_2.toString() + '-' + this.user.user_telephone_3.toString();
      params.dept_name = this.user.dept_name;
      if(this.call_type.regist){
        let {data} = await this.$http.post(`user_register`, params)
        if(data.register_result == 1) {
          this.$session.$emit('modal-alert', '관리자 승인 후 사용 가능합니다.')
          this.$router.push('/')
        }else if(data.register_result == 0) {
          this.$session.$emit('modal-alert', '회원등록처리가 정상처리 되지 못했습니다.')
          this.$router.push('/')
        }
      }else{
        let {data} = await this.$http.post(`user_update`, params)
        if(data.update_result == 1 && !this.$session.hasPermission([1])){
          this.popup.relogin.show = true
        }
        if(this.call_type.userlist_modify)
          this.$emit('refresh_list')
      }

    },
    onUserEmailAuth(){
      this.$session.$emit('modal-alert', '미지원기능입니다.')
    },
    onReLogin(){
      this.popup.relogin.show = false
      this.$session.logout()
    }
  },
  mounted () {
    // alert(JSON.stringify(this.userinfo))
    // Object.assign(this.user,this.userinfo)
    if(this.call_type.myinfo || this.call_type.userlist_modify) {
      this.user.id = this.userinfo.id
      this.user.user_id = this.userinfo.user_id
      this.user.user_name = this.userinfo.user_name
      this.user.user_phone_1 = this.userinfo.phone.split('-')[0]
      this.user.user_phone_2 = this.userinfo.phone.split('-')[1]
      this.user.user_phone_3 = this.userinfo.phone.split('-')[2]
      this.user.user_telephone_1 = this.userinfo.telephone.split('-')[0]
      this.user.user_telephone_2 = this.userinfo.telephone.split('-')[1]
      this.user.user_telephone_3 = this.userinfo.telephone.split('-')[2]
      this.user.dept_name = this.userinfo.dept_name
      this.user.last_logon_time = this.userinfo.last_logon_time
      this.user.password_date = this.userinfo.password_date

      this.member_user_type.forEach(v => v.check = false)
      this.member_user_type[this.userinfo.user_type - 1].check = true
      for (var i = 0; i < this.member_area_type.length; i++) {
        if (this.member_area_type[i].value == this.userinfo.area_code) {
          this.user.selected_area_type = this.member_area_type[i]
          this.user.r_area_code = this.member_area_type[i].value
          break
        }
      }
      for (i = 0; i < this.member_user_status.length; i++) {
        if (this.member_user_status[i].value == this.userinfo.user_status) {
          this.user.selected_user_status = this.member_user_status[i]
          this.user.r_user_status = this.member_user_status[i].value
          break
        }
      }
    }else{
      this.member_user_type[2].check = true
      this.user.selected_area_type = this.member_area_type[0]
      this.user.r_area_code = this.member_area_type[0].value
      this.user.r_user_status = 0

    }

  },
  data () {
    return {
      user: {
        show: true,
        id:-1,
        user_id:'',
        user_name:'',
        dept_name:'',
        user_passwd:'',
        user_passwdc:'',
        user_phone:'',
        user_phone_1:'',
        user_phone_2:'',
        user_phone_3:'',
        user_telephone:'',
        user_telephone_1:'',
        user_telephone_2:'',
        user_telephone_3:'',
        user_email:'',
        errors: [],
        selected_area_type:null,
        selected_user_status:null,
        r_area_type:null,
        r_user_status:null,
        r_area_code:null,
        overlab_result:0,
        last_logon_time:null,
        password_date:null
      },
      member_user_type:[
        {name:'관리자',code:1,check:false},
        {name:'공제사업처',code:2,check:false},
        {name:'권역별 지부',code:3,check:false},
        {name:'일반',code:4,check:false},
        {name:'회원',code:5,check:false},
        {name:'학교',code:6,check:false},
      ],
      member_area_type:[
        {text:'-',value:'R000',index:9},
        {text:'서울강원',value:'R001',index:0},
        {text:'경기인천',value:'R002',index:1},
        {text:'대전충청',value:'R003',index:2},
        {text:'대구경북',value:'R004',index:3},
        {text:'부산경남',value:'R005',index:4},
        {text:'호남제주',value:'R006',index:5},
      ],
      member_user_status:[
        {text:'대기',value:0},
        {text:'승인',value:1}
      ],
      loading: false,
      school: {},
      refresh_id:0,
      s3_data_json:null,
      deleteDialog:{
        show: false,
        delItem:''
      },
      previews:[],
      popup:{
        del_user:{
          show:false,
          del_item:null,
          errors: [],
        },
        deleted_user:{
          show:false,
          errors: [],
        },
        relogin:{
          show:false,
          errors: [],
        },
        exit_user:{
          show:false,
          errors: [],
        }
      },
      err_msg:''
    }
  }
}
</script>

<style lang="scss" scoped>
.t1 {
  text-align: justify;
  text-align-last: justify;
  flex: 1 0 auto;
  padding: 0 10px;
}

.abl-page {
  padding: 15px 30px;
}

.abl-table-user {
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
  .abl-input-b {
    float:left;
    padding-left: 10px;
    margin-top: 5px;
    margin-left: 10px;
    margin-right: 10px;
    width: 28%;
    height: 30px;
    background-color: #ffffff;
    border: 1px solid #aaaaaa;
    &:hover, &:focus {
      background-color: #ebebeb;
    }

  }
  .abl-input-c {
    float:left;
    padding-left: 10px;
    margin-top: 5px;
    margin-left: 10px;
    margin-right: 10px;
    width: 75%;
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
    width: 20%;
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
</style>