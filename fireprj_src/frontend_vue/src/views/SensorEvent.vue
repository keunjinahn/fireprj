<template>
  <main-layout>
    <template v-slot>
      <div class="main-panel">
        <v-toolbar color="light-blue darken-4" dark flat>
          <v-toolbar-title>화재감지기 상태</v-toolbar-title>
        </v-toolbar>

        <v-card flat height="100">
          <v-toolbar rounded dense class="elevation-1" height="100">
            <v-col cols="8">
              <v-text-field outlined dense hide-details
                            placeholder="감지기 검색"
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
            <v-col cols="1">
              <v-btn depressed dark big
                      color="light-blue darken-2"
                      class="m-left"
                      @click="downloadExcel()">
                <v-icon small>mdi-arrow-down-bold-outline</v-icon>
                <div class="ml-1">xls 다운로드</div>
              </v-btn>
            </v-col>
          </v-toolbar>
        </v-card>

        <v-data-table
          :headers="sensor.headers"
          :items="sensor.data"
          :loading="sensor.loading"
          :options.sync="sensor.options"
          :server-items-length="sensor.total"
          :search="sensor.search"
          :items-per-page="5"
          :footer-props="{'items-per-page-options': [5, 10, 15,20,25,30,-1]}"
          class="elevation-1 mt-4">
          <template v-slot:item="row">
            <tr @click="onSensorItemClick(row.item,row)" :class="{'row-active': row.item.id == sensor.selectedId}">
              <td >{{ row.item._index }}</td>
              <td >{{ row.item.last_event_time | moment('YYYY-MM-DD HH:mm:ss')}}</td>
              <td >{{ String(row.item.fk_customer_idx).padStart(5,'0') }}</td>
              <td >{{ row.item.customer.customer_name }}</td>
              <td >{{ $session.receiver_type_list.find(v=>v.code==row.item.receiver.receiver_type).name }}</td>
              <td>{{ String(row.item.receiver_id).padStart(3,'0') }}</td>
              <td >{{ String(row.item.system_id).padStart(3,'0') }}</td>
              <td >{{ String(row.item.repeater_id).padStart(3,'0') }}</td>
              <td >{{ String(row.item.sensor_id).padStart(3,'0') }}</td>
              <td >
                <div v-if="row.item.register_status" class="blue-circle"></div>
                <div v-else class="red-circle"></div>
              </td>
              <td >
                <div v-if="row.item.action_status" class="blue-circle"></div>
                <div v-else class="red-circle"></div>
              </td>
              <td >
                <div v-if="row.item.com_status" class="blue-circle"></div>
                <div v-else class="red-circle"></div>
              </td>
              <td >
                <div v-if="row.item.battery_status" class="blue-circle"></div>
                <div v-else class="red-circle"></div>
              </td>              
            </tr>
          </template>
        </v-data-table>
        <v-toolbar color="light-blue darken-1" dark flat>
          <v-toolbar-title>감지기 이벤트 상세</v-toolbar-title>
        </v-toolbar>         
        <v-data-table
        :headers="event.headers"
        :items="event.data"
        :loading="event.loading"
        :options.sync="event.options"
        :server-items-length="event.total"
        :items-per-page="5"
        :footer-props="{'items-per-page-options': [5, 10, 15,20,25,30,-1]}"
        class="elevation-1 mt-4">
        <template v-slot:item="row">
          <tr>
            <td >{{ row.item._index }}</td>
            <td >{{ row.item.event_datetime | moment('YYYY-MM-DD HH:mm:ss')}}</td>
            <td >{{ row.item.event_idx }}</td>
            <td >{{ row.item.sensor_value }}</td>
            <td >{{ row.item.event.event_desc }}</td>
            <td >{{ row.item.inout_id }}</td>
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

      const { page, itemsPerPage, sortBy, sortDesc } = this.sensor.options;
      try {
        let filters_or = []
        let filters_and = []
        let order_by = []
        if (this.sensor.search) {
          filters_or.push({name: 'customer', op: 'has', val: {name: "customer_name", op: "like", val: `%${this.sensor.search}%`}});
        }
        if (sortBy.length) {
          for (let i=0; i<sortBy.length; i++) {
            order_by.push({field: sortBy[i], direction: sortDesc[i] ? 'desc' : 'asc'})
          }
        }else{
          order_by.push({field: "last_event_time", direction: 'desc'})
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

        let { data } = await this.$http.get("sensor_event", { params });
        this.sensor.total = data.num_results;
        this.sensor.data = data.objects.map((v, i) => {
          v._index = i + (page - 1) * itemsPerPage + 1;
          return v;
        });
      } catch (err) {
        console.error(err);
      } finally {
        this.sensor.loading = false;
      }   
    },
    async onSensorItemClick(item){
      this.sensor.selectedId = item.id
      const { page, itemsPerPage, sortBy, sortDesc } = this.event.options;
      try {
        let filters_or = []
        let filters_and = []
        let order_by = []
        filters_and.push({name: 'sensor_id', op: 'eq', val: item.sensor_id})
        order_by.push({field: "event_log_idx", direction: 'desc'})
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
        this.selected_sensor = item
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
    }
    

  },
  mounted() {
    this.getSensorEvent()
  },
  watch: {
    "sensor.options": {
      handler() {
        this.getSensorEvent()
      },
      deep: true,
    },
    "event.options": {
      handler() {
        this.onSensorItemClick(this.selected_sensor)
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
        options: {"page":1,"itemsPerPage":5,"sortBy":[],"sortDesc":[],"groupBy":[],"groupDesc":[],"mustSort":false,"multiSort":false},
        loading: false,
        search: '',
        total:0
      },
      event: {
        headers: [
          {text: 'No.', value: 'id', sortable: false, align: 'center', width: 20 },
          {text: "이벤트 시간", value: "event_datetime", sortable: false,align: 'center', width: 80}, 
          {text: "이벤트 No.", value: "event_id", sortable: false,align: 'center', width: 80}, 
          {text: "감지기 현재값", value: "sensor_value",align: 'center', sortable: false, width: 60},
          {text: "이벤트 내용", value: "event_desc",align: 'center', sortable: false, width: 150},
          {text: "입출력단 번호", value: "inout_id",align: 'center', sortable: false, width: 40},          
        ],
        data: [],
        options: {"page":1,"itemsPerPage":5,"sortBy":[],"sortDesc":[],"groupBy":[],"groupDesc":[],"mustSort":false,"multiSort":false},
        loading: false,
        search: '',
        total:0
      },      
      loading: false,
      selected_sensor:null
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
</style>
