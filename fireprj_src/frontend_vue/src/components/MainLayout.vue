<template>
  <div class="w-100">
    <v-app-bar app clipped-left dense class="top-menu" color="white" elevation="1">
      <router-link :to="{name: 'dashboard'}" class="d-flex align-center">
        <img src="@/assets/logo-black.png"/>
      </router-link>
      <div class="ml-auto d-flex align-center">
        <div class="worktime mr-4">{{worktime}}</div>
        <v-divider vertical/>
        <v-btn text color="grey darken-1" @click="onManualDownload()">
          <v-icon color="grey lighten-1" class="mr-1" >mdi-file-download-outline</v-icon>
          메뉴얼
        </v-btn>
        <v-divider vertical/>
        <v-btn :disabled="$session.getUserType() == 5 || $session.getUserType() == 6" text color="grey darken-1" href="" @click="userinfo.show=true">
          <v-icon color="grey lighten-1" class="mr-1">{{($session.getUserType() == 5 ||$session.getUserType() == 6)? "mdi-home-city-outline":"mdi-account-edit"}}</v-icon>
          {{getLoginName()}}

        </v-btn>
        <v-divider vertical/>
        <v-btn icon small color="deep-orange accent-2" class="ml-4" @click="logout_dialog.show=true">
          <v-icon>mdi-power</v-icon>
        </v-btn>
      </div>
    </v-app-bar>

    <v-navigation-drawer app clipped absolute permanent color="white" :mini-variant="mini">
<!--        <div class="mt-2 px-4 d-flex justify-center">-->
<!--          <v-btn block rounded depressed dark color="red accent-2" :to="{name: 'dashboard'}">-->
<!--            <v-icon>mdi-map-check-outline</v-icon>-->
<!--            <div class="ml-2">대시보드</div>-->
<!--          </v-btn>-->

<!--        </div>-->
      <div class="mt-2 px-4 d-flex justify-space-between align-center">
        <template v-if="mini">
          <v-icon @click="mini = false">mdi-chevron-double-right</v-icon>
        </template>
        <template v-else>
          <v-btn depressed dark small
                color="light-blue darken-2"
                  width="100"
                @click="sitemap_dialog.show=true">
            <div>전체메뉴</div>
          </v-btn>
          <v-btn icon @click="mini = true">
            <v-icon>mdi-chevron-double-left</v-icon>
          </v-btn>
        </template>
      </div>
      <v-list class="transparent">
        <template v-for="(item, i) in items">
          <template v-if="$session.hasPermission(item.allow) && (!item.heading || !mini)">
            <template v-if="item.heading">
              <v-divider v-show="item.show" :key="item.heading" />
              <v-subheader v-show="item.show" :key="i" class="main-menu-header">{{item.heading}}</v-subheader>
            </template>
            <v-list-item  v-show="item.show" :disabled="item.disabled" v-else :key="i" :to="item.to" color="primary darken-3">
              <v-list-item-action >
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-action>
              <v-list-item-content>
                <v-list-item-title color="light-blue darken-4">{{ item.text }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </template>
        </template>
      </v-list>

    </v-navigation-drawer>

    <v-main class="page-container">
<!--      <div v-if="$route.name !== 'dashboard' && $route.meta.breadcrumb" class="breadcrumb d-flex justify-space-between px-4">-->
<!--        <div class="text-body-2 d-flex align-center blue&#45;&#45;text">-->
<!--          <v-icon small color="light-blue darken-4" class="mr-2">mdi-note-outline</v-icon>-->
<!--          {{$route.meta.breadcrumb[$route.meta.breadcrumb.length - 1].text}}-->
<!--        </div>-->
<!--        <v-breadcrumbs :items="$route.meta.breadcrumb">-->
<!--          <template v-slot:divider>-->
<!--            <v-icon>mdi-chevron-right</v-icon>-->
<!--          </template>-->
<!--        </v-breadcrumbs>-->
<!--      </div>-->
    <template v-if="$route.name === 'dashboard'">
      <div class="float-menu fm-sub">
        <slot name="left"></slot>
      </div>
    </template>
      <slot></slot>
    </v-main>

    <v-dialog v-model="sitemap_dialog.show" content-class="v-pos" persistent max-width="1000px" max-height="500px">
      <div class="sitemap-container">
        <v-card >
          <v-card-title class="pt-2 pb-1 primary white--text">
            <span class="body-1">사이트맵</span>
          </v-card-title>
          <v-btn fab x-small depressed color="deep-purple lighten-5" class="sitemap-close" @click="sitemap_dialog.show=false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <abl-document class="sitemap-page">
            <div class="abl-doc-body">
              <table class="abl-table-sitemap">
                <colgroup>
                  <col style="width:12.5%"/>
                  <col style="width:12.5%"/>
                </colgroup>
                <tr>
                  <th class="s-h" colspan="1">모니터링</th>
                  <th class="s-h" colspan="1">대시보드</th>
                  <td colspan="6" class="th-cursor">
                    <span class="th-cursor" @click="move_page({name: 'dashboard', params: {fstatus: undefined}})">대시보드</span>
                  </td>
                </tr>
                <tr>
                  <th class="s-h" rowspan="2" colspan="1">태풍 정보</th>
                  <th class="s-h" rowspan="1" colspan="1">태풍 관리</th>
                  <td colspan="6" class="th-cursor">
                    <span class="th-cursor" @click="move_page({name: 'typhoon_manage_tab', params: {fstatus:0}})">과거 태풍 관리</span>
                    <span class="th-cursor" @click="move_page({name: 'typhoon_manage_tab', params: {fstatus:1}})">신규 태풍 등록</span>
                  </td>
                </tr>
                <tr>
                  <th class="s-h" rowspan="1" colspan="1">태풍 피해 관리</th>
                  <td colspan="6" class="th-cursor">
                    <span class="th-cursor" @click="move_page({name: 'damage_manage_tab', params: {fstatus:0}})">태풍별 피해 현황</span>
                    <span class="th-cursor" @click="move_page({name: 'damage_manage_tab', params: {fstatus:1}})">태풍별 피해 예측 현황</span>
                  </td>
                </tr>
                <tr>
                  <th class="s-h" rowspan="1" colspan="1">통계 관리</th>
                  <th class="s-h" rowspan="1" colspan="1">태풍 피해 통계 현황</th>
                  <td colspan="6" class="th-cursor">
                    <span class="th-cursor" @click="move_page({name: 'statistics_dashboard_tab', params: {fstatus:0}})">태풍피해 통계 현황</span>
                  </td>
                </tr>
                <tr>
                  <th class="s-h" rowspan="1" colspan="1">보고서 관리</th>
                  <th class="s-h" rowspan="1" colspan="1">세부 피해내역 보고서</th>
                  <td colspan="6" class="th-cursor">
                    <span class="th-cursor" @click="move_page({name: 'statistics_report_tab', params: {fstatus:0}})">학교별 피해내역 보고서</span>
<!--                    <span class="th-cursor" @click="move_page({name: 'statistics_report_tab', params: {fstatus:1}})">학교별 피해내역 보고서</span>-->
<!--                    <span class="th-cursor" @click="move_page({name: 'statistics_report_tab', params: {fstatus:2}})">학교별 피해내역 보고서</span>-->
                  </td>
                </tr>
                <tr>
                  <th class="s-h" rowspan="1" colspan="1">커뮤니티</th>
                  <th class="s-h" rowspan="1" colspan="1">공지 및 자료실</th>
                  <td colspan="6" class="th-cursor">
                    <span v-show="$session.hasPermission([1])" class="th-cursor" @click="move_page({name: 'community_list_tab', params: {fstatus:0}})">공지사항</span>
                    <span class="th-cursor" @click="move_page({name: 'community_list_tab', params: {fstatus:1}})">Q &amp; A</span>
                    <span class="th-cursor" @click="move_page({name: 'community_list_tab', params: {fstatus:2}})">자료실</span>
                  </td>
                </tr>
                <tr v-show="$session.hasPermission([1])" >
                  <th class="s-h" rowspan="1" colspan="1">사용자 관리</th>
                  <th class="s-h" rowspan="1" colspan="1">사용자 관리</th>
                  <td colspan="6" class="th-cursor">
                    <span class="th-cursor" @click="move_page({name: 'user_manage_tab', params: {fstatus:0}})">사용자(한국교육시설안전원) 관리</span>
                    <span class="th-cursor" @click="move_page({name: 'user_manage_tab', params: {fstatus:1}})">회원/학교 관리</span>
                    <span class="th-cursor" @click="move_page({name: 'user_manage_tab', params: {fstatus:2}})">사용자 이력 관리</span>
                  </td>
                </tr>
                <tr v-show="$session.hasPermission([1])" >
                  <th class="s-h" rowspan="1" colspan="1">시스템 설정</th>
                  <td colspan="6" class="th-cursor">
                    <span class="th-cursor" @click="onSettingShow()">메일서버 설정</span>
                  </td>
                </tr>
              </table>
            </div>
          </abl-document>
        </v-card>
      </div>
    </v-dialog>
    <v-dialog v-model="userinfo.show" persistent max-width="1000px" max-height="500px">
      <div class="user-info-container">
        <v-btn fab x-small dark depressed color="grey darken-1" class="user-info-close" @click="userinfo.show=false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <user-info :userinfo="$session.getUserInfo()" :call_type="{myinfo:true,regist:false,userlist_add:false,userlist_modify:false}"/>
      </div>
    </v-dialog>
    <v-dialog v-model="logout_dialog.show" max-width="500px">
      <v-card>
        <v-card-title>로그아웃 하시겠습니까?</v-card-title>
        <v-card-actions>
          <v-btn tile depressed class="flex-grow-1" @click="$session.logout()">로그아웃</v-btn>
          <v-btn tile depressed class="flex-grow-1" @click="logout_dialog.show = false">취소</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="smtp_dialog.show" persistent max-width="600px">
      <v-card>
        <v-card-title class="pt-2 pb-1 primary white--text">
          <span class="body-1">SMPT 메일 설정</span>
        </v-card-title>
        <v-divider />
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="6">
                <v-text-field
                    outlined
                    dense
                    label="메일 전송서버 주소"
                    v-model="smtp_dialog.form.smtp_server"
                    hide-details
                />
              </v-col>
              <v-col cols="6">
                <v-text-field
                    outlined
                    dense
                    label="메일 전송서버 포트"
                    v-model="smtp_dialog.form.smtp_port"
                    hide-details
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="6">
                <v-text-field
                    outlined
                    dense
                    label="전송메일주소"
                    v-model="smtp_dialog.form.smtp_sender"
                    hide-details
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="6">
                <v-text-field
                    outlined
                    dense
                    label="아이디"
                    v-model="smtp_dialog.form.smtp_id"
                    hide-details
                />
              </v-col>
              <v-col cols="6">
                <v-text-field
                    outlined
                    dense
                    label="패스워드"
                    v-model="smtp_dialog.form.smtp_pass"
                    hide-details
                />
              </v-col>
            </v-row>

          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-btn
              color="light-blue darken-2"
              class="flex-grow-1"
              text
              @click="smtp_dialog.show = false"
          >
            닫기
          </v-btn>
          <v-btn
              color="light-blue darken-2"
              class="flex-grow-1"
              tile
              dark
              depressed
              @click="submitSettingHadler"
          >
            저장
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import AblDocument from '@/components/AblDocument'
import UserInfo from '@/components/UserInfo'
import axios from "axios";
export default {
  components: {AblDocument ,UserInfo},
  props: {
    source: String,
  },
  methods:{
    move_page(move_info){
      if (move_info.name === this.$route.name && move_info.params.fstatus === this.$route.params.fstatus) {
        // this.refreshKey = Date.now()
        return;
      }
      else {
        this.$router.push(move_info)
        this.sitemap_dialog.show = false
      }
    },
    onManualDownload(){
      var idx = "1"
      if(this.$session.getUserType() == 2 || this.$session.getUserType() == 3 || this.$session.getUserType() == 4)
        idx = "2"
      else if(this.$session.getUserType() == 5 || this.$session.getUserType() == 6)
        idx = "3"
      var url = this.$session.getWebURL() + "/manual_" + idx + ".pdf"
      axios({
        url: url,
        method: 'GET',
        responseType: 'blob',
      }).then((response) => {
        var fileURL = window.URL.createObjectURL(new Blob([response.data]));
        var fileLink = document.createElement('a');

        fileLink.href = fileURL;
        fileLink.setAttribute('download', '한국교육시설 재난피해 태풍 예측시스템 매뉴얼.pdf');
        document.body.appendChild(fileLink);
        fileLink.click();
      });
    },
    getLoginName(){
      if(this.$session.hasPermission([5])){
        return this.$session.getUserInfo().sub_group_name
      }else if(this.$session.hasPermission([6])){
        return this.$session.getUserInfo().sub_school_name
      }
      return this.$session.getUserName()
    },
    async onSettingShow(){
      let q = JSON.stringify({ filters: [{name: 'id', op: 'eq', val: 1}] })
      let {data} = await this.$http.get('settings', {params: {q}})
      if(data.num_results > 0){
        var smtp_data = data.objects[0]
        this.smtp_dialog.form.smtp_server = smtp_data.smtp_server
        this.smtp_dialog.form.smtp_port = smtp_data.smtp_port
        this.smtp_dialog.form.smtp_sender = smtp_data.smtp_sender
        this.smtp_dialog.form.smtp_id = smtp_data.smtp_id
        this.smtp_dialog.form.smtp_pass = smtp_data.smtp_pass
      }
      this.smtp_dialog.show = true
    },
    async submitSettingHadler(){
      let params = {};
      if(this.smtp_dialog.form.smtp_server.length == 0
          || this.smtp_dialog.form.smtp_port.length == 0
          || this.smtp_dialog.form.smtp_id.length == 0
          || this.smtp_dialog.form.smtp_pass.length == 0
          || this.smtp_dialog.form.smtp_sender.length == 0
      ){
        this.$session.$emit('modal-alert', 'SMTP 서버 정보를 입력해 주세요!')
        return
      }
      params.smtp_server = this.smtp_dialog.form.smtp_server
      params.smtp_port = this.smtp_dialog.form.smtp_port
      params.smtp_sender = this.smtp_dialog.form.smtp_sender
      params.smtp_id = this.smtp_dialog.form.smtp_id
      params.smtp_pass = this.smtp_dialog.form.smtp_pass
      await this.$http.patch(`settings/1`, params)
      this.smtp_dialog.show = false
      this.$session.$emit('modal-alert', 'SMTP 서버 설정이 수정되었습니다!')
    }

  },
  computed: {
    clock () {
      if (!this.$session.sessionStart) return '00:00'
      let diff = Math.floor((Date.now() - this.$session.sessionStart) / 1000)
      return `${diff / 60}:${diff % 60}`
    }
  },
  mounted () {
    setInterval(() => {
      this.worktime = this.$session.getSessionDuration()
    })
  },
  data: () => ({
    mini: false,
    worktime: '00:00',
    refreshKey: Date.now(),
    items: [
      { heading: '모니터링' },
      {
        icon: "mdi-desktop-mac-dashboard",
        text: "대시보드",
        to: { name: "dashboard" },
        disabled:false,
        show:true,
      },
      { heading: '태풍정보'},
      {
        icon: "mdi-weather-hurricane",
        text: "태풍관리",
        to: { name: "typhoon_manage" },
        disabled:false,
        show:true,
      },
      {
        icon: "mdi-database-search",
        text: "태풍 피해 관리",
        to: { name: "damage_manage" },
        disabled:false,
        show:true,
      },
      { heading: '통계 관리'},
      {
        icon: "mdi-chart-areaspline-variant",
        text: "태풍 피해 통계 현황",
        to: { name: "statistics_dashboard" },
        disabled:false,
        show:true,
      },
      { heading: '보고서 관리'},
      {
        icon: "mdi-chart-pie",
        text: "세부 피해내역 보고서",
        to: { name: "statistics_report" },
        disabled:false,
        show:true,
      },
      { heading: '커뮤니티'},
      {
        icon: "mdi-chat-processing",
        text: "커뮤니티",
        to: { name: "community_list" },
        disabled:false,
        show:true,
      },
      { heading: '사용자 관리', allow: [1]},
      {
        allow: [1],
        icon: "mdi-account-plus",
        text: "사용자 관리",
        to: { name: "user_manage" },
        disabled:false,
        show:true,
      },
    ],
    sitemap_dialog:{
      show:false
    },
    userinfo: {
      show: false,
      data: null
    },
    logout_dialog: {
      show: false,
    },
    smtp_dialog:{
      show:false,
      form:{
        smtp_server:'',
        smtp_port:null,
        smtp_sender:'',
        smtp_id:'',
        smtp_pass:''
      }

    },
  }),
};
</script>

<style lang="scss">
/* #keep .v-navigation-drawer__border {
  display: none
} */
.top-menu {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 100;
}
.float-menu {
  position: absolute;
  width: 300px;
  z-index: 100;

  &.fm-main {
    top: 63px;
    left: 5px;
  }
  &.fm-sub {
    top: 15px;
    left: 5px;
  }
}
.page-container {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1;
  background-color:#dadada;
  // background-color: #3d5f70;
  // background-image: url(../assets/bg/bg-1.jpg);
  // background-size: cover;
}
.inc-count {
  display: inline-block;
  margin: 4px 0px 4px 5px;
  box-sizing: border-box;
  font-weight: bold;
}

.sub-menu {
  border-radius: 5px;
  // background-color: rgba(21, 65, 106, 0.8);
  background-color: rgba(255,255,255,0.86);
}

.menusd-enter-active {
  position: absolute;
  transition: transform 0.5s;
}
.menusd-leave-active {
  position: absolute;
  transition: transform 0.5s;
}
.menusd-enter {
  transform: translateX(-320px);
}
.menusd-leave-to {
  transform: translateX(-320px);
}
.sitemap-container {
  position: relative;
}
.sitemap-close {
  position: absolute;
  top: 2px; right: 10px;
  z-index: 10;
}
.sitemap-page {
  padding: 5px 5px;
  .th-cursor{
    cursor: pointer;
    margin-left: 10px;
    border-bottom: 1px solid blueviolet;
  }
}

.main-menu-header {
  height: 30px !important;
  background-color: #2a5b82;
  border-color: #2a5b82;
  color: white !important;
}

.breadcrumb {
  background-color: white;
  border-bottom: 1px solid #dadada;
}
.sw-pos {
  margin-top: -12px;
}

.user-info-container {
  position: relative;
}
.user-info-close {
  position: absolute;
  top: 10px; right: 20px;
  z-index: 10;
}
.v-pos {
  position: absolute;
  top: 50px; left: 100px;
}
</style>
