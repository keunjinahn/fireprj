<template>
  <main-layout>
    <template v-slot>
      <div class="main-panel">
        <v-toolbar color="light-blue darken-4" dark flat>
          <v-toolbar-title>데이터 분석</v-toolbar-title>
        </v-toolbar>

        <v-card flat height="100">
          <v-toolbar rounded dense class="elevation-1" height="100">
            <v-col cols="7">
              <v-text-field outlined dense hide-details
                            placeholder="데이터 검색"
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
                      class="m-left">
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
              <td >{{ row.item.event_datetime }}</td>
              <td >{{ row.item.fk_customer_idx }}</td>
              <td >{{ row.item.customer.customer_name }}</td>
              <td >{{ row.item.receiver_type }}</td>
              <td >{{ row.item.receiver_id}}</td>
              <td >{{ row.item.system_id}}</td>
              <td >{{ row.item.repeater_id }}</td>
              <td >{{ row.item.sensor_id }}</td>
            </tr>
          </template>
        </v-data-table>
        
        <br/>
        <v-card flat>
          <v-row>
            <div class="sensor-detail-container-2">
              <highcharts
                constructor-type="chart"
                :options="chartOption_flux"
                class="hi-weight"
              />
            </div>
          </v-row>
        </v-card>

      </div>
    </template>
  </main-layout>
</template>

<script>
import _ from "lodash";
const chartOptions = {
  // chart: { zoomType: 'xy' },
  title: { text: null },
  colors: ["skyblue", "orange"],
  xAxis: [{categories: [], crosshair: false}],
  yAxis: [
    {
      labels: { format: "{value:,f}" },
      title: { text: "계측 값" },
    },
  ],
  credits: { enabled: false },
  tooltip: { shared: true, crosshair: false },
  series: [{ data: [], type: "line", name: "value", lineWidth: 2 }],
};

export default {
  props: {
  },
  components: {},
  methods: {
    async getSensor() {

      let {data} = await this.$http.get("sensor_event")
      this.sensor.data = data.objects;
    },
    // async getSensorData() {
    //   let {data} = await this.$http.post("sensor_data", {}).catch((error) =>{
    //     console.log(error)
    //   });

    //   this.data_objs.cate_flux = [];
    //   this.data_objs.flux = [];
    //   this.data_objs.cate_flux = data.sensor_flux_list.map(v=> v.created_date)
    //   data.sensor_flux_list.map((v)=> this.data_objs.flux.push({
    //     x:moment(v.created_date).valueOf(),
    //     y:Math.ceil(v.data *8)/8
    //   }));
    //   this.startInterval()
      
    // },
    // startInterval(){
    //   clearTimeout(this.tick);
    //   this.tick = setTimeout(async ()=> {
    //     this.getSensorData();
    //   },2000);
    // },

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
  computed:{
    // chartOption_flux() {
    //   let obj = _.cloneDeep(chartOptions);
    //   obj.series[0].data = this.data_objs.flux.map((v) => v.y);
    //   obj.xAxis[0].categories = this.data_objs.cate_flux
    //   obj.yAxis[0].title.text = "유량";
    //   obj.series[0].name = "유량값"
    //   return obj;
    // },
  },
  data() {
    return {
      sensor: {
        headers: [
          {text: "이벤트 시간", value: "event_datetime", sortable: false,align: 'center', width: 80}, 
          {text: "고객 식별자", value: "fk_customer_idx",align: 'center', sortable: false, width: 60},
          {text: "고객명", value: "customer.customer_name",align: 'center', sortable: false, width: 40},
          {text: "수신기 타입", value: "receiver_type",align: 'center', sortable: false, width: 20},
          {text: "수신기 번호", value: "receiver_id",align: 'center', sortable: false, width: 20},
          {text: "계통 번호", value: "system_id",align: 'center', sortable: false, width: 20},
          {text: "중계기 번호", value: "repeater_id",align: 'center', sortable: false, width: 20},
          {text: "감지기 번호", value: "sensor_id",align: 'center', sortable: false, width: 20},
        ],
        data: [],
        options: {"page":1,"itemsPerPage":5,"sortBy":[],"sortDesc":[],"groupBy":[],"groupDesc":[],"mustSort":false,"multiSort":false},
        loading: false,
        search: '',
      },
      loading: false,
      addPopup: {
        show: false,
        form: {
          repeater_idx: '',
          fk_customer_idx: '',
          receiver_id: '',
          system_id: '',
          repeater_id: '',
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
