<template>
  <main-layout>
    <template v-slot>
      <div class="main-panel">
        <v-toolbar
            color="light-blue darken-4"
            dark
            flat
        >
          <v-toolbar-title>태풍 관리</v-toolbar-title>

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
              v-for="type_item in type_tab_items"
              :key="type_item">
            <v-card flat >
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
  methods: {

  },
  mounted() {
  },
  watch: {
    "typhoon.options": {
      handler() {
      },
      deep: true,
    },
    "path.options": {
      handler() {
      },
      deep: true,
    },
    fstatus () {
      console.log('fstatus: ' + this.fstatus)
      this.selected_tab_item = this.fstatus
    },
    "typhoon.past_dialog.options": {
      handler() {
      },
      deep: true,
    },
  },
  data() {
    return {
      typhoon: {
        search: '',
        headers_past: [
          { text: 'No.', value: 'id', sortable: false, width: 40 , align: 'center'},
          { text: "태풍번호", value: "typhoon_number", width: 200, align: 'center', sortable: true },
          { text: "태풍이름", value: "typhoon_name" , width: 200, align: 'center', sortable: true },
          { text: "시작일시", value: "typhoon_start_date", width: 200, align: 'center' , sortable: false },
          { text: "종료일시", value: "typhoon_end_date", width: 200, align: 'center' , sortable: false },
          // { text: "태풍방향", value: "typhoon_dir", width: 200, align: 'center' , sortable: false },
          { text: "태풍크기", value: "typhoon_size", width: 200, align: 'center' , sortable: false },
        ],
        headers_future: [
          { text: 'No.', value: 'id', sortable: false, width: 40 , align: 'center'},
          { text: "태풍번호", value: "typhoon_number", width: 200, align: 'center', sortable: true },
          { text: "태풍이름", value: "typhoon_name" , width: 200, align: 'center', sortable: true },
          { text: "시작일시", value: "typhoon_start_date", width: 200, align: 'center' , sortable: false },
          { text: "종료일시", value: "typhoon_end_date", width: 200, align: 'center' , sortable: false },
          // { text: "태풍방향", value: "typhoon_dir", width: 200, align: 'center' , sortable: false },
          { text: "태풍크기", value: "typhoon_size", width: 200, align: 'center' , sortable: false },
          { text: "수정", value: "", width: 80, align: 'center', sortable: false },
          { text: "삭제", value: "", width: 80, align: 'center', sortable: false },
        ],

        data: [],
        options: {"page":1,"itemsPerPage":5,"sortBy":[],"sortDesc":[],"groupBy":[],"groupDesc":[],"mustSort":false,"multiSort":false},
        loading: false,
        dialog: {
          show: false,
          form: {
            typhoon_number: "",
            typhoon_name: "",
            typhoon_start_date: moment().format("YYYY-MM-DD HH:mm:ss"),
            typhoon_end_date: moment()
                .add(1, "month")
                .format("YYYY-MM-DD HH:mm:ss"),
            typhoon_dir: null,
            typhoon_size: null,
            parent_typhoon_id:-1
          },
          del_show:false,
          deleted_show:false,
          del_item:null,
          path_del_show:false,
          path_deleted_show:false,
          path_del_item:null
        },
        past_dialog :{
          headers: [
            { text: 'No.', value: 'id', sortable: false, width: 40 , align: 'center'},
            { text: "태풍번호", value: "typhoon_number", width: 200, align: 'center', sortable: true },
            { text: "태풍이름", value: "typhoon_name" , width: 200, align: 'center', sortable: true },
            { text: "선택", value: "", width: 60, align: 'center', sortable: false },
          ],
          show:false,
          data:[],
          loading:false,
          options: {"page":1,"itemsPerPage":5,"sortBy":[],"sortDesc":[],"groupBy":[],"groupDesc":[],"mustSort":false,"multiSort":false},
          search_string:''
        },
      },

      path: {
        headers_past: [
          { text: "일시", value: "created_date", align: 'center', sortable: true },
          { text: "위도", value: "latitude", align: 'center', sortable: false },
          { text: "경도", value: "longitude", align: 'center', sortable: false },
          { text: "중심기압", value: "center_pressure", align: 'center', sortable: false },
          { text: "최대속도(초)", value: "max_speed_s" , align: 'center', sortable: false },
          { text: "최대속도(시)", value: "max_speed_h" , align: 'center', sortable: false },
          { text: "풍속반경", value: "wind_radius" , align: 'center', sortable: false },
          { text: "폭풍반경", value: "storm_radius" , align: 'center', sortable: false },
          { text: "방향", value: "direction" , align: 'center', sortable: false },
          { text: "이동속도", value: "move_speed_h", align: 'center', sortable: false },
        ],
        headers_future: [
          { text: "일시", value: "created_date", align: 'center', sortable: true },
          { text: "위도", value: "latitude", align: 'center', sortable: false },
          { text: "경도", value: "longitude", align: 'center', sortable: false },
          { text: "중심기압", value: "center_pressure", align: 'center', sortable: false },
          { text: "최대속도(초)", value: "max_speed_s" , align: 'center', sortable: false },
          { text: "최대속도(시)", value: "max_speed_h" , align: 'center', sortable: false },
          { text: "풍속반경", value: "wind_radius" , align: 'center', sortable: false },
          { text: "폭풍반경", value: "storm_radius" , align: 'center', sortable: false },
          { text: "방향", value: "direction" , align: 'center', sortable: false },
          { text: "이동속도", value: "move_speed_h", align: 'center', sortable: false },
          { text: "수정", value: "", width: 80, align: 'center', sortable: false },
          { text: "삭제", value: "", width: 80, align: 'center', sortable: false },
        ],
        data: [],
        options: {"page":1,"itemsPerPage":5,"sortBy":[],"sortDesc":[],"groupBy":[],"groupDesc":[],"mustSort":false,"multiSort":false},
        loading: false,
        dialog: {
          show: false,
          form: {
            created_date: moment().format("YYYY-MM-DD HH:mm:ss"),
            latitude: "",
            longitude: "",
            center_pressure: "",
            max_speed_s: "",
            max_speed_h: "",
            wind_radius: "",
            storm_radius: "",
            direction: "",
            move_speed_h: ""
          }
        },
        selected_typhoon_id : -1
      },

      options: {
        dir: ["동쪽", "서쪽", "남쪽"],
        size: ["대형", "중형", "소형"],
        path_dir:["남","남남동","남남서","남동","남서","동","동남동","동북동","북","북동","북북동","북북서","북서","서","서남서","서북서"],
        strength:["강","매우강","약","중","초강력"]
      },

      datetime: {
        show: false,
        date: "",
        time: "",
      },

      loading: false,
      selected_tab_item: null,
      type_tab_items: ['과거 태풍 관리','신규 태풍 등록'],
      search: {
        dialog: {
          show: false,
          form: {
            typhoon_start_date: moment("2010-01-01").format("YYYY-MM-DD"),
            typhoon_end_date: moment(moment().format("YYYY") + "-12-31").format("YYYY-MM-DD"),
          },
          selected_search_type:null,
          selected_search_type_code:0,
          search_type:[
            {name:"전체",code:0},
            {name:"태풍번호",code:1},
            {name:"태풍이름",code:2},
            {name:"태풍크기",code:3},
          ]
        },
        datetime: {
          show: false,
          date: "",
          time: "",
        },

      },
      allowedHours: v => v % 2,
      allowedMinutes: v => v >= 10 && v <= 50,
      allowedStep: m => m % 10 === 0,
      timePickerRefreshKey: Date.now()
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
.m-right{margin-right: 20px;}
.flex-grow-0{
  margin-left:10px;
  margin-bottom: 10px;
  width:200px;
}
.tm-s-v-m{
  margin-right: 10px;
}
.text-center{
  text-align: center;
}
.b-r{
  text-align:right;
}
td {
  text-align: center;
}
</style>
