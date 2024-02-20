<template>
  <main-layout>
    <template v-slot>
      <div class="main-panel">
        <v-toolbar
            color="light-blue darken-4"
            dark
            flat
        >
          <v-toolbar-title>태풍 피해 관리</v-toolbar-title>

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
  import axios from 'axios'
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
      "accident.options": {
        handler() {
        },
        deep: true,
      },
      fstatus () {
        console.log('fstatus: ' + this.fstatus)
        this.selected_tab_item = this.fstatus
      }
    },
    data() {
      return {
        empty:'',
        empty2:'',
        active: false,
        accident: {
          headers_past: [
            { text: "No", value: "id", align: 'center', sortable: false },
            { text: "회원명", value: "mem_name",align: 'center',  sortable: true },
            { text: "학교명", value: "school_name", align: 'center', sortable: true },
            { text: "지역", value: "area_code_name",align: 'center',  sortable: true },
            { text: "설립구분", value: "establish_gubun_name", align: 'center', sortable: true },
            { text: "학교급구분", value: "organ_gubun2_name",align: 'center',  sortable: true },
            { text: "태풍이름", value: "sub2_disaster_naming",align: 'center', sortable: true },
            { text: "재난일시", value: "sub2_sdate", align: 'center', sortable: true },
            { text: "피해경위", value: "sub2_damage_detail", align: 'center', sortable: false },
            { text: "총지급액", value: "total_payment_money",align: 'center',  sortable: true },
          ],
          headers_future: [
            { text: "No", value: "id",align: 'center',  sortable: false },
            { text: "회원명", value: "mem_name",align: 'center',  sortable: true },
            { text: "학교명", value: "school_name", align: 'center', sortable: true },
            { text: "지역", value: "area_code_name", align: 'center', sortable: true },
            { text: "설립구분", value: "establish_gubun_name", align: 'center', sortable: true },
            { text: "학교급구분", value: "organ_gubun2_name", align: 'center', sortable: true },
            { text: "태풍이름", value: "sub2_disaster_naming", align: 'center', sortable: true },
            { text: "피해예상규모", value: "total_payment_money", align: 'center', sortable: true },
          ],
          search_text: '',
          data: [],
          loading: false,
          options: {"page":1,"itemsPerPage":10,"sortBy":[],"sortDesc":[],"groupBy":[],"groupDesc":[],"mustSort":false,"multiSort":false},
        },
        alert_dialog:{
          show: false,
          progress_show:false,
          progress_del_show:false,
          error: []
        },
        schooldetail: {
          show: false,
          data: null
        },
        dialog: {
          refresh_id :1,
          show: false,
          form: null
        },
        upload: {
          loading: false,
          dialog: {
            show: false,
          }
        },
        excel: {
          loading: false
        },
        options: {
          acci_year: ["2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"],
          school_type: ["유치원", "초등학교", "중학교", "고등학교", "대학", "전문대학", "특수학교", "대학원", "연구기관", "기타"],
        },

        datetime: {
          show: false,
          date: "",
          time: "",
        },

        loading: false,

        excelData: [],

        upload_file: null,
        excel_upload_loading: false,
        selected_tab_item: null,
        type_tab_items: ['태풍별 피해 현황','태풍별 피해 예측 현황'],
        search: {
          dialog: {
            show: false,
            form: {
              acci_start_date: moment("2010-01-01").format("YYYY-MM-DD"),
              acci_end_date: moment().format("YYYY-MM-DD"),
            },
            selected_search_type:null,
            selected_search_type_code:0,
            search_type:[
              {name:"전체",code:0},
              {name:"회원명",code:1},
              {name:"학교명",code:2},
              {name:"태풍이름",code:3},
            ]
          },
          datetime: {
            show: false,
            date: "",
            time: "",
          },
        },
        download_file_index:1
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
    font-size: 14px !important;
  }
  .main-panel .v-data-table th {
    font-size: 14px;
  }
  .main-panel .v-data-table td {
    font-size: 14px;
  }
  .p-right {
    float:right;
    max-width: 100px;
  }
  .container-h{
    max-height: 40px;
    margin-top: -30px;
  }
  .container-h2{
    max-height: 60px;
    margin-top: -25px;
  }

  $control-width: 100px;
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

  .abl-page {
    padding: 15px 30px;
  }
  .control-cont {
    width: $control-width; height: 1px;
    padding: 5px 8px; margin-right: 15px;
    border-radius: 3px;
    user-select: none;
    position: relative;
    margin-left:0px;
    margin-top: 50px;
    .control-inner {
      position: absolute;
    }

    .abl-divider {
      margin-top: 20px;
      font-size: 12px;
    }

    .category-select {
      width: $control-width;
    }

  }
.image-left-m{
  margin-left: 14px;
  padding: -100px -100px;
}
.t-text-s{
  font-size: 14px !important;
}
.school-detail-container {
  position: relative;
}
.school-detail-close {
  position: absolute;
  top: 20px; right: 10px;
  z-index: 10;
}
.m-right{margin-right: 20px;}
.text-center{
  text-align: center;
}
td {
  text-align: center;
}
.m-left{margin-left: 10px;}
</style>
