<template>
  <main-layout>
    <template v-slot>
      <div class="main-panel">
        <v-toolbar color="light-blue darken-4" dark flat>
          <v-toolbar-title>최신 이벤트 상태</v-toolbar-title>
        </v-toolbar>

        <v-card flat height="100">
          <v-toolbar rounded dense class="elevation-1" height="100">
            <v-col cols="8">
              <v-text-field outlined dense hide-details
                            placeholder="이벤트 검색"
                            append-icon="mdi-magnify"
                            v-model="sensor.search"
                            @keydown.enter="getSensorEvent()"
                            class="m-right"
              />
            </v-col>
            <v-col cols="1">
              <v-btn depressed dark big
                      color="light-blue darken-2"
                      @click="getSensorEvent()">
                
                <div class="ml-1">조회</div>
              </v-btn>
            </v-col>
            <!-- <v-col cols="1">
              <v-btn depressed dark big
                      color="light-blue darken-2"
                      class="m-left"
                      @click="downloadExcel()">
                <v-icon small>mdi-arrow-down-bold-outline</v-icon>
                <div class="ml-1">xls 다운로드</div>
              </v-btn>
            </v-col> -->
          </v-toolbar>
        </v-card>

        <v-data-table
        :headers="event.headers"
        :items="event.data"
        :loading="event.loading"
        :options.sync="event.options"
        :server-items-length="event.total"
        :items-per-page="20"
        :footer-props="{'items-per-page-options': [5, 10, 15,20,25,30,-1]}"
        class="elevation-1 mt-4">
          <template v-slot:item="row">
            <tr >
              <td :class="{'red-event': check_red(row.item.event_id)}">{{ row.item._index }}</td>
              <td :class="{'red-event': check_red(row.item.event_id)}">{{ row.item.event_datetime | moment('YYYY-MM-DD HH:mm:ss')}}</td>
              <td :class="{'red-event': check_red(row.item.event_id)}">{{ row.item.event.event_category }}</td>
              <td :class="{'red-event': check_red(row.item.event_id)}">{{ row.item.event.event_desc }}</td>
              <td :class="{'red-event': check_red(row.item.event_id)}">{{ row.item.customer.customer_name }}</td>
              <td :class="{'red-event': check_red(row.item.event_id)}">{{ $session.receiver_type_list.find(v=>v.code==row.item.receiver_type).name }}</td>
              <td :class="{'red-event': check_red(row.item.event_id)}">{{ String(row.item.receiver_id).padStart(3,'0') }}</td>
              <td :class="{'red-event': check_red(row.item.event_id)}">{{ String(row.item.system_id).padStart(3,'0') }}</td>
              <td :class="{'red-event': check_red(row.item.event_id)}">{{ String(row.item.repeater_id).padStart(3,'0') }}</td>
              <td :class="{'red-event': check_red(row.item.event_id)}">{{ String(row.item.sensor_id).padStart(3,'0') }}</td>
              <td :class="{'red-event': check_red(row.item.event_id)}">{{ row.item.sensor_value }}</td>
            </tr>
          </template>
        </v-data-table> 
            
      </div>



    </template>
  </main-layout> 
</template>

<script>
import axios from "axios";
import { eq } from 'lodash';
import moment from 'moment'
export default {
  props: {
  },
  components: {},
  methods: {

    async getSensorEvent() {
      const { page, itemsPerPage, sortBy, sortDesc } = this.event.options;
      try {
        let filters_or = []
        let filters_and = []
        let order_by = []
        order_by.push({field: "event_log_idx", direction: 'desc'})
        if (this.sensor.search) {
          filters_or.push({name: 'event', op: 'has', val: {name: "event_category", op: "like", val: `%${this.sensor.search}%`}});
          filters_or.push({name: 'customer', op: 'has', val: {name: "customer_name", op: "like", val: `%${this.sensor.search}%`}});
        }        
        let q = {
          filters: [{or: filters_or}, {and: filters_and}],
          order_by
        }
        let params = {
          q: q,
          results_per_page: itemsPerPage,
          page: page,

        };
        let { data } = await this.$http.get("event_log_list", { params });
        this.event.total = data.num_results;
        this.event.data = data.objects.map((v, i) => {
          v._index = i + (page - 1) * itemsPerPage + 1;
          return v;
        });
      } catch (err) {
        console.error(err);
      } finally {
        this.event.loading = false;
      }    
    },
    
    async downloadExcel() {
      let params = {
        "page_name": "sensor_event",
        "headers": (() => {
          let headers_text = []
          for (let i=1; i < this.sensor.headers.length-1; i++) {
            headers_text.push(this.sensor.headers[i].text)
          }
          return headers_text
        })()
      }
      let {data} = await this.$http.post('make_excel', params)

      var url = this.$session.getWebURL() + '/api/v1/save_excel/' + data.filename
      axios({
        method: 'get',
        url:url,
        responseType: 'blob'
      })
      .then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data], {
          type: 'application/vnd.ms-excel'
        }))
        const link = document.createElement('a')
        link.href = url
        var download_file_name = "감지기상태_" + Date.now().toString() + ".xlsx"
        link.setAttribute('download', download_file_name)
        link.click()
      })
      .catch(() => console.log('error: excel download error'))
    },
    check_red(index){
      if(index == 145 || index == 20 || index == 39)
        return true
      return false
    },
    startInterval() {
      this.stopInterval();

      this.intervalId = setInterval(() => {
        this.getSensorEvent()
      }, 1000);
    },
    stopInterval() {
      if (this.intervalId) {
        clearInterval(this.intervalId)
        this.intervalId = null
      }
    },
  },
  mounted() {
    this.getSensorEvent()
    this.startInterval()
  },
  beforeDestroy() {
    this.stopInterval()
  },
  watch: {
    "event.options": {
      handler() {
        this.stopInterval()
        this.startInterval()
      },
      deep: true,
    },
  
  },
  data() {
    return {
      sensor: {
        selectedId: '',
        headers: [
          {text: 'No.', value: 'id', sortable: false, align: 'center', width: 20 },
          {text: "이벤트 시간", value: "event_datetime", sortable: false,align: 'center', width: 80}, 
          {text: "고객 식별자", value: "fk_customer_idx",align: 'center', sortable: false, width: 60},
          {text: "고객명", value: "customer.customer_name",align: 'center', sortable: false, width: 40},
          {text: "수신기 타입", value: "receiver_type",align: 'center', sortable: false, width: 80},
          {text: "수신기 번호", value: "receiver_id",align: 'center', sortable: false, width: 20},
          {text: "계통 번호", value: "system_id",align: 'center', sortable: false, width: 20},
          {text: "중계기 번호", value: "repeater_id",align: 'center', sortable: false, width: 20},
          {text: "감지기 번호", value: "sensor_id",align: 'center', sortable: false, width: 20},
          {text: "등록 상태", value: "register_status",align: 'center', sortable: false, width: 20},
          {text: "동작 상태", value: "action_status",align: 'center', sortable: false, width: 20},
          {text: "통신 상태", value: "com_status",align: 'center', sortable: false, width: 20},
          {text: "배터리 상태", value: "battery_status",align: 'center', sortable: false, width: 20},
        ],
        data: [],
        options: {"page":1,"itemsPerPage":10,"sortBy":[],"sortDesc":[],"groupBy":[],"groupDesc":[],"mustSort":false,"multiSort":false},
        loading: false,
        search: '',
        total:0
      },
      event: {
        headers: [
          {text: 'No.', value: 'id', sortable: false, align: 'center', width: 20 },
          {text: "이벤트 시간", value: "event_datetime", sortable: false,align: 'center', width: 80}, 
          {text: "이벤트 구분", value: "event_category", sortable: false,align: 'center', width: 80},
          {text: "이벤트 내용", value: "event_desc", sortable: false,align: 'center', width: 100},
          {text: "고객명", value: "customer_name",align: 'center', sortable: false, width: 40},
          {text: "수신기 타입", value: "receiver_type",align: 'center', sortable: false, width: 80},
          {text: "수신기 번호", value: "receiver_id",align: 'center', sortable: false, width: 20},
          {text: "계통 번호", value: "system_id",align: 'center', sortable: false, width: 20},
          {text: "중계기 번호", value: "repeater_id",align: 'center', sortable: false, width: 20},
          {text: "감지기 번호", value: "sensor_id",align: 'center', sortable: false, width: 20},         
          {text: "감지기 현재값", value: "sensor_value",align: 'center', sortable: false, width: 60},   
        ],
        data: [],
        options: {"page":1,"itemsPerPage":10,"sortBy":[],"sortDesc":[],"groupBy":[],"groupDesc":[],"mustSort":false,"multiSort":false},
        loading: false,
        search: '',
        total:0,
        red_event_list:[145,20,39],

      },      
      loading: false,
      selected_sensor:null,
      intervalId:null
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
.main-panel .v-data-table header {
  font-size: 14px;
}
.main-panel .v-data-table th {
  font-size: 14px;
}
.main-panel .v-data-table td {
  font-size: 14px;
}
td {
  text-align: center;
}
.main-panel .v-data-table{
  cursor:pointer
}
.flex-grow-1{
  margin-left:10px;
  margin-bottom: 10px;
  width:48%;
}
.red-event{
  color:red
}
</style>
