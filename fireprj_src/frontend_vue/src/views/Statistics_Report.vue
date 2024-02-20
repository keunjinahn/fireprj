<template>
  <main-layout>
    <template v-slot>
      <div class="main-panel">
        <v-toolbar
            color="light-blue darken-4"
            dark
            flat
        >
          <v-toolbar-title>세부 피해내역 보고서</v-toolbar-title>

          <v-spacer></v-spacer>

          <template v-slot:extension>
            <v-tabs
                v-model="selected_tab_item"
                align-with-title
                slider-size="6"
            >
              <v-tabs-slider color="yellow"></v-tabs-slider>

              <v-tab v-show="$session.hasPermission([1,2,3,4])" @change="change_tab_item(type_tab_items[0])">
                {{type_tab_items[0]}}
              </v-tab>
              <v-tab v-show="$session.hasPermission([5])" @change="change_tab_item(type_tab_items[1])">
                {{type_tab_items[0]}}
              </v-tab>
              <v-tab v-show="$session.hasPermission([6])" @change="change_tab_item(type_tab_items[2])">
                {{type_tab_items[0]}}
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
import _ from 'lodash'
import moment from 'moment'
import axios from "axios";
const pieOptions = {

  chart: {backgroundColor: 'transparent', type: 'pie', height: 280},
  title: {
    text: ''
  },
  credits: {enabled: false},
//   legend: {enabled: false},
  legend: {layout: 'horizontal'},
  plotOptions: {
    pie: {
      allowPointSelect: true,
      cursor: 'pointer',
      dataLabels: {
        enabled: true,
        format: '<b>{point.name}</b>: {point.y} 건'
      },
      showInLegend: true
    }
  },
  xAxis: {
  },
  series: [{
    data: [],
    name: 'data',
    colorByPoint: true
  }]
}

const chartOptions = {
  chart: {backgroundColor: 'transparent', type: 'column', height: 200},
  title: {text: null},
  credits: {enabled: false},
  legend: {enabled: false},
  xAxis: {
    categories: []
  },
  yAxis: {title:{enabled: false}},
  series: [{
    data: [],
    name: 'data',
    maxPointWidth: 10
  }]
}
export default {
  props: {
    fstatus: { type: [Number, String], default: 0 }
  },
  components: {},
  methods: {
 
  },
  computed: {
  
  },
  mounted () {

  },
  watch: {
    "report.options": {
      handler() {
      },
      deep: true,
    },
    fstatus () {
      console.log('fstatus: ' + this.fstatus)
      this.selected_tab_item = this.fstatus
    }
  },
  data () {
    return {
      report: {
        headers: [
          { text: "순번", value: "id", align: 'center', sortable: false },
          { text: "재난번호", value: "disaster_num",align: 'center',  sortable: false },
          { text: "회원명", value: "mem_name",align: 'center',  sortable: false },
          { text: "학교명", value: "school_name", align: 'center', sortable: false },
          { text: "태풍이름", value: "sub2_disaster_naming",align: 'center', sortable: false },
          // { text: "학교번호", value: "school_num", align: 'center', sortable: false },
          { text: "건물피해", value: "building_info",align: 'center',  sortable: false },
          // { text: "기본담보피해", value: "qurantee_info", align: 'center', sortable: false },
          { text: "부속물피해", value: "accessories",align: 'center',  sortable: false },
          { text: "물품피해", value: "article",align: 'center',  sortable: false },
          { text: "배상책임", value: "compensation",align: 'center',  sortable: false },
          { text: "총지급액", value: "payment_money",align: 'center',  sortable: false },
        ],
        search_text: '',
        data: [],
        loading: false,
        options: {"page":1,"itemsPerPage":10,"sortBy":[],"sortDesc":[],"groupBy":[],"groupDesc":[],"mustSort":false,"multiSort":false},
      },
      headers: [
        { text: 'Col1', value: 'calories' },
        { text: 'Col2', value: 'calories' },
        { text: 'Col3', value: 'calories' },
        { text: 'Col4', value: 'calories' },
        { text: 'Col5', value: 'calories' }
      ],
      loading: false,
      items: [],

      search: {
        search_text:'',
        year: moment().format('YYYY'),
        school_type: null,
        regions: {value: 0, text: '전체'},
        yearlist: [],
        description: null,
        selected_search_type:null,
        selected_search_type_code:0,
        yearfrom:null,
        yearto:null,
        search_type:[
          {name:"전체",code:0},
          {name:"회원명",code:1},
          {name:"학교명",code:2},
          {name:"태풍이름",code:3},
          {name:"재난번호",code:4},
        ]
      },

      summary: {
        school_cnt: 0,
        acci_cost: 0,
        tp_cnt: 0
      },

      data: {
        area: [],
        tp: [],
        schools: [],
        refresh_id:0,
        loading:false
      },

      meta: {
        schoolTypes: [
          {value: null, text: '전체'},
          {value: '고등학교', text: '고등학교'},
          {value: '교육지원청', text: '교육지원청'},
          {value: '교육청', text: '교육청'},
          {value: '기타', text: '기타'},
          {value: '대학', text: '대학'},
          {value: '대학원', text: '대학원'},
          {value: '도서관', text: '도서관'},
          {value: '연구기관', text: '연구기관'},
          {value: '유치원(단/병)', text: '유치원(단/병)'},
          {value: '전문대학', text: '전문대학'},
          {value: '전시장', text: '전시장'},
          {value: '중학교', text: '중학교'},
          {value: '진흥원·교육연수원·수련시설', text: '진흥원·교육연수원·수련시설'},
          {value: '체육시설', text: '체육시설'},
          {value: '초등학교', text: '초등학교'},
          {value: '특수학교', text: '특수학교'},
          {value: '평생교육기관', text: '평생교육기관'}
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
      },
      selected_tab_item: null,
      type_tab_items: ['학교별 피해내역 보고서','관내 학교 피해 내역 보고서','우리 학교 피해 내역 보고서'],
      schooldetail: {
        show: false,
        data: null
      },
      dialog: {
        refresh_id :1,
        show: false,
        form: null
      },
      download_file_index:1
    }
  }
}
</script>

<style lang="scss" scoped>
.main-panel {
  padding: 10px;
  height: calc(100vh - 80px);
  overflow-y: auto;
}

.summary-content {
  height: 100px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.data-table-container {

}
.abl-page {
  padding: 15px 30px;
  width:1200px;
}
.school-file-upload {
  position: relative;
  top: 0px; left: 10px;
  z-index: 10;
}
.school-save {
  position: relative;
  top: -10px; left:15px;
  z-index: 10;
}
.report-download {
  position: relative;
  top: -10px; left:780px;
  z-index: 10;
}
.image-left-m{
  overflow: hidden;
  text-align: center;
  display: block;
  margin-left: auto;
  margin-right: auto;
}
.td-bold{
  background-color: #e7e7e7;
}
.image-default-h{
  height:26px !important;
  text-align: center;
}
.school-detail-container {
  position: relative;
}
.school-detail-close {
  position: absolute;
  top: 20px; right: 10px;
  z-index: 10;
}
.filter-label {
  padding: 0 10px;
}
.filter-year {
  width: 100px;
}
.filter-typhoon {
  width: 240px;
}
.filter-region {
  width: 200px;
}
.filter-search {
  width: 400px;
  margin-left:30px;
}
.filter-btn {
  width: 80px;
  margin-left:30px;
}
.filter-download {
  width: 100px;
  margin-left:60px;
}

.filter-divider {
  padding: 0 10px;
}
.flex-grow-0{
  margin-left:10px;
  margin-bottom: 10px;
  margin-top: 7px;
  width:200px;
}
.abl-page {
  padding: 15px 30px;
}
</style>
