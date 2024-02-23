<template>
  <main-layout>
    <template v-slot>
      <div class="main-panel">
        <v-toolbar
            color="light-blue darken-4"
            dark
            flat
        >
          <v-toolbar-title>사용자 관리</v-toolbar-title>

          <v-spacer></v-spacer>

          <template v-slot:extension>
            <v-tabs
                v-model="selected_tab_item"
                align-with-title
                slider-size="6"
            >
              <v-tabs-slider color="yellow"></v-tabs-slider>

              <v-tab
                  v-for="item in type_tab_items"
                  :key="item"
                  @change="change_tab_item(item)"
              >
                {{ item }}
              </v-tab>
            </v-tabs>
          </template>
        </v-toolbar>
        <v-tabs-items v-model="selected_tab_item">
          <v-tab-item
              v-for="(type_item) in type_tab_items"
              :key="type_item">
            <v-card flat>
              <br>
              
            </v-card>
          </v-tab-item>

        </v-tabs-items>
      </div>
    </template>
  </main-layout>
</template>

<script>
import moment from "moment";
export default {
  props: {
    fstatus: { type: [Number, String], default: 0 }
  },
  components: {},
  methods: {
    
  },
  mounted() {
  },
  watch: {
    'users.options': {
      handler() {
      },
      deep: true
    },
    fstatus () {
      console.log('fstatus: ' + this.fstatus)
      this.selected_tab_item = this.fstatus
    }
  },
  data() {
    return {
      users: {
        selected: [],
        singleSelect: false,
        headers_user: [
          {text: 'No.', value: 'id', sortable: false,align: 'start', width: 60},
          {text: "사용자구분", value: "user_type",align: 'center', sortable: true},
          {text: "지부", value: "area_code",align: 'center', sortable: true},
          {text: "아이디", value: "user_id",align: 'center', sortable: true},
          {text: "성명", value: "user_name",align: 'center', sortable: true},
          {text: "전화번호", value: "phone",align: 'center', sortable: false},
          {text: "핸드폰번호", value: "telephone",align: 'center', sortable: false},
          {text: "부서", value: "dept_name",align: 'center', sortable: false},
          {text: "등록일자", value: "created_date",align: 'center', sortable: true},
          {text: "회원상태", value: "user_status",align: 'center',width:200,sortable: true},
        ],
        headers_school: [
          {text: 'No.', value: 'id', sortable: false,align: 'center', width: 60},
          {text: "사용자구분(회원/학교)", value: "user_type",align: 'center', sortable: true},
          {text: "아이디", value: "user_id",align: 'center', sortable: true},
          // {text: "지역", value: "area_code",align: 'center', sortable: true},
          // {text: "성명", value: "user_name",align: 'center', sortable: true},
          {text: "회원명", value: "sub_group_name",align: 'center', sortable: true},
          {text: "학교명", value: "sub_school_name",align: 'center', sortable: true},
          {text: "전화번호", value: "phone",align: 'center', sortable: false},
          {text: "마지막로그인", value: "last_logon_time",align: 'center', width:200,sortable: true}
        ],
        headers_history: [
          { text: 'No.', value: 'id',align: 'center', sortable: false, width: 40 },
          { text: '일시', value: 'created',align: 'center', sortable: false, width: 180 },
          { text: '아이디', value: 'user_id',align: 'center', sortable: false },
          { text: '유형', value: 'type',align: 'center', sortable: false },
          { text: '아이피', value: 'ip_addr',align: 'center', sortable: false },
          { text: '운영체제', value: 'os_ver',align: 'center', sortable: false },
          { text: '브라우저', value: 'browser_ver',align: 'center', sortable: false },
        ],
        search_text: '',
        data: [],
        options: {},
        loading: false,
        search:{
          selected_user_type:null,
          selected_user_status:null,
          selected_member_type:null,
          selected_member_string:null,
          member_type_list:[
            {text:'전체',value:0},
            {text:'회원',value:1},
            {text:'학교',value:2}
          ],
          member_string_list:[
            {text:'전체',value:0},
            {text:'아이디',value:1},
            {text:'회원명',value:2},
            {text:'학교명',value:3},
            {text:'지역명',value:4},
          ],
        }

      },
      popup:{
        user: {
          data: {
            user_id:''
          },
          show: false,
          errors: [],
          form: {
          },
          selected_area_type:null,
          selected_user_status:null,
          selected_user_region:null,
          selected_user_search_type:null,
          r_area_type:null,
          r_user_status:null,
          passwd:"",
          passwd_c:"",
          user_phone_1:'',
          user_phone_2:'',
          user_phone_3:'',
          user_telephone:'',
          user_telephone_1:'',
          user_telephone_2:'',
          user_telephone_3:'',
        },
        del_user:{
          show:false,
          del_item:null,
          errors: [],
        },
        deleted_user:{
          show:false,
          errors: [],
        }
      },
      member_user_type:[
        {name:'관리자',code:1,check:false},
        {name:'공제사업처',code:2,check:false},
        {name:'권역별 지부',code:3,check:false},
        {name:'일반',code:4,check:false},
        {name:'회원',code:5,check:false},
        {name:'학교',code:6,check:false},
      ],
      member_user_type_m:[
        {name:'전체',code:0,check:false},
        {name:'공제사업처',code:2,check:false},
        {name:'권역별 지부',code:3,check:false},
        {name:'일반',code:4,check:false},
      ],
      member_area_type:[
        {text:'서울강원',value:'R001',index:0},
        {text:'경기인천',value:'R002',index:1},
        {text:'대전충청',value:'R003',index:2},
        {text:'대구경북',value:'R004',index:3},
        {text:'부산경남',value:'R005',index:4},
        {text:'호남제주',value:'R006',index:5},
      ],
      member_area_type_m:[
        {text:'전체',value:'R000',index:0},
        {text:'서울강원',value:'R001',index:0},
        {text:'경기인천',value:'R002',index:1},
        {text:'대전충청',value:'R003',index:2},
        {text:'대구경북',value:'R004',index:3},
        {text:'부산경남',value:'R005',index:4},
        {text:'호남제주',value:'R006',index:5},
      ],
      member_user_status:[
        {text:'대기',value:1},
        {text:'승인',value:2}
      ],
      member_user_status_m:[
        {text:'전체',value:2},
        {text:'대기',value:0},
        {text:'승인',value:1}
      ],
      regions: [
        {value: 0, text: '전체'},
        {value: 1, text: '강원'},
        {value: 2, text: '경기'},
        {value: 3, text: '경남'},
        {value: 4, text: '경북'},
        {value: 5, text: '광주'},
        {value: 6, text: '대구'},
        {value: 7, text: '대전'},
        {value: 8, text: '부산'},
        {value: 9, text: '서울'},
        {value: 10, text: '세종'},
        {value: 11, text: '울산'},
        {value: 12, text: '인천'},
        {value: 13, text: '전남'},
        {value: 14, text: '전북'},
        {value: 15, text: '제주'},
        {value: 16, text: '충남'},
        {value: 17, text: '충북'}
      ],

      loading: false,
      selected_tab_item: null,
      type_tab_items: ['사용자(한국교육시설안전원) 관리','회원/학교 관리','사용자 접속 이력'],
      all_item_check:true
    };
  },
};
</script>

<style lang="scss" scoped>
.main-panel {
  padding: 10px;
  height: calc(100vh - 80px);
  overflow-y: auto;
}
.datetime-wrap {
  position: relative;
}
.func-wrap {
  position: absolute;
  top: 10px;
  right: -200px;
  width: 200px;
}
.main-panel .v-data-table header {
  font-size: 14px;
}
.main-panel .v-data-table th {
  font-size: 14px;
}
.main-panel .v-data-table td {
  font-size: 14px;
}
.search-action {
  flex: 0 0 120px;
  margin-left: 10px;
  display: flex;
  align-items: center;
}
.m-right{margin-right: 20px;}
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
td {
  text-align: center;
}

.user-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}
.user-close {
  position: absolute;
  top: 0px; right: 20px;
  z-index: 10;
}
.user-page {
  padding: 5px 5px;
  .th-cursor{
    cursor: pointer;
  }
}
.s-size{
  width:230px;
  max-height:20px !important;
  margin-top:-16px;
  margin-left:10px;
}
.s-left{
  text-align: left;
  margin-left: 0px;
}
.v-col-right{
  text-align: right;
}

.user-info-container {
  position: relative;
}
.user-info-close {
  position: absolute;
  top: 10px; right: 20px;
  z-index: 10;
}
</style>
