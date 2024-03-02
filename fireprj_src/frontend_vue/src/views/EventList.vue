<template>
  <main-layout>
    <template v-slot>
      <div class="main-panel">
        <v-toolbar color="light-blue darken-4" dark flat>
          <v-toolbar-title>이벤트 리스트</v-toolbar-title>
        </v-toolbar>

        <v-card flat>
          <v-toolbar rounded dense class="elevation-1">
            <v-col cols="5">
              <v-text-field outlined dense hide-details
                            placeholder="이벤트 검색"
                            append-icon="mdi-magnify"
                            v-model="sensor.search"
                            @keydown.enter="getSensor()"
                            class="m-right"
              />
            </v-col>
            <v-col cols="1">
              <v-btn depressed dark big
                      color="light-blue darken-2"
                      @click="getSensor()">
                
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
          @click:row="popupSensorData"
          class="elevation-1 mt-4">
          <template v-slot:item="row">
            <tr >
              <td >{{ row.item.event_idx }}</td>
              <td >{{ row.item.system_id_c }}</td>
              <td >{{ row.item.repeater_id_c }}</td>
              <td >{{ row.item.sensor_id_c }}</td>
              <td >{{ row.item.sensor_value_c }}</td>
              <td >{{ row.item.inout_id_c }}</td>
              <td >{{ row.item.event_desc }}</td>
            </tr>
          </template>
        </v-data-table>
      </div>
    </template>
  </main-layout> 
</template>

<script>
import axios from "axios";
export default {
  props: {
  },
  components: {},
  methods: {
    async getSensor() {
      let {data} = await this.$http.get("event_list")
      this.sensor.data = data.objects;
    },
    popupSensorData(e, {item}) {
      this.infoPopup.form = item;
      this.infoPopup.show = true;
    },
    async downloadExcel() {
      let params = {
        "page_name": "event_list",
        "headers": (() => {
          let headers_text = []
          for (let i=0; i < this.sensor.headers.length; i++) {
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
        var download_file_name = "이벤트목록_" + Date.now().toString() + ".xlsx"
        link.setAttribute('download', download_file_name)
        link.click()
      })
      .catch(() => console.log('error: excel download error'))
    }
  },
  mounted() {
    this.getSensor()
  },
  watch: {
    "sensor.options": {
      handler() {
      },
      deep: true,
    },
  },
  data() {
    return {
      sensor: {
        headers: [
          {text: "이벤트", value: "event_idx", sortable: false,align: 'center', width: 80},
          {text: "계통 번호", value: "system_id_c",align: 'center', sortable: false, width: 60},
          {text: "중계기 번호", value: "repeater_id_c",align: 'center', sortable: false, width: 40},
          {text: "감지기 번호", value: "sensor_id_c",align: 'center', sortable: false, width: 20},
          {text: "감지기 현재값", value: "sensor_value_c",align: 'center', sortable: false, width: 20},
          {text: "입출력단 번호", value: "inout_id_c",align: 'center', sortable: false, width: 20},
          {text: "구분", value: "event_desc",align: 'center', sortable: false, width: 20},
        ],
        data: [],
        options: {"page":1,"itemsPerPage":10,"sortBy":[],"sortDesc":[],"groupBy":[],"groupDesc":[],"mustSort":false,"multiSort":false},
        loading: false,
        search: '',
      },
      loading: false,
      addPopup: {
        show: false,
        form: {
          sensor_idx: '',
          fk_customer_idx: '',
          receiver_id: '',
          system_id: '',
          repeater_id: '',
          sensor_id: '',
        }
      },
      infoPopup: {
        show: false,
        form: {}
      },
      deletePopup: {
        show: false,
        delTarget: ''
      }
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

.flex-grow-1{
  margin-left:10px;
  margin-bottom: 10px;
  width:48%;
}
</style>
