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
          single-select
          item-key="id"
          :footer-props="{'items-per-page-options': [5, 10, 15,20,25,30,-1]}"
          class="elevation-1 mt-4">
          <template v-slot:item="row">
            <tr @click="onShowGraph(row.item,row)" :class="{'row-active': row.item.id == sensor.selectedId}">
              <td >{{ row.item.id }}</td>
              <td >{{ row.item.last_event_time | moment('YYYY-MM-DD HH:mm:ss')}}</td>
              <td >{{ String(row.item.fk_customer_idx).padStart(5,'0') }}</td>
              <td >{{ row.item.customer.customer_name }}</td>
              <td >{{ $session.receiver_type_list.find(v=>v.code==row.item.receiver.receiver_type).name }}</td>
              <td >{{ String(row.item.receiver_id).padStart(3,'0') }}</td>
              <td >{{ String(row.item.system_id).padStart(3,'0') }}</td>
              <td >{{ String(row.item.repeater_id).padStart(3,'0') }}</td>
              <td >{{ String(row.item.sensor_id).padStart(3,'0') }}</td>
            </tr>
          </template>
        </v-data-table>
        
        <br/>
        <template v-if="chart.show">
          <v-toolbar color="light-blue darken-1" dark flat>
            <v-toolbar-title>화재 감지기 신호</v-toolbar-title>
          </v-toolbar>        
          <v-toolbar rounded dense class="elevation-1" height="50">
            <v-row>
              <v-col cols="2">
                <v-radio-group
                inline
                class="vrg-cls"
                v-model="chart.range_value"
                >
                  <v-row >
                    <v-col cols="4" class="vrg-item">
                      <v-radio
                      label="일"
                      ></v-radio>
                    </v-col>
                    <v-col cols="4" class="vrg-item">
                      <v-radio
                      label="시"
                      ></v-radio>
                    </v-col>
                    <v-col cols="4" class="vrg-item">
                        <v-radio
                        label="분"
                        ></v-radio>                     
                    </v-col>                  
                  </v-row>
                </v-radio-group>
              </v-col>
              <v-col cols="8">
              </v-col>
              <!--
              <v-col cols="2">
                <v-radio-group
                inline
                class="vrg-cls"
                v-model="chart.check_type"
                >
                  <v-row >
                    <v-col cols="6" class="vrg-item">
                      <v-radio
                      label="정상동작"
                      ></v-radio>
                    </v-col>
                    <v-col cols="6" class="vrg-item">
                      <v-radio
                      label="이상동작"
                      ></v-radio>
                    </v-col>              
                  </v-row>
                </v-radio-group>
              </v-col>-->              
            </v-row>
            
          </v-toolbar>
          <v-card height="300">
            <v-card-title class="body-1 font-weight-bold py-2">감지기 번호 : {{(chart.sensor != undefined)? String(chart.sensor).padStart(3,'0') : ''}}</v-card-title>
            <v-divider/>
            <highcharts
                constructor-type="chart"
                class="realtime-graph"
                :options="chartOption_sensor_logs"
                />
          </v-card>

        </template>
        <!-- <v-card flat>
          <v-row>
            <div class="sensor-detail-container-2">
              <highcharts
                constructor-type="chart"
                :options="chartOption_flux"
                class="hi-weight"
              />
            </div>
          </v-row>
        </v-card> -->

      </div>
    </template>
  </main-layout>
</template>

<script>
import axios from "axios";
import moment from "moment";
import _ from "lodash";
const chartOptions = {
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
          order_by.push({field: "id", direction: 'asc'})
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
    async getLogs() {
      let params = {
        'sensor_id': this.chart.sensor
      }
      let {data} = await this.$http.get("sensor-log-chart", {params})
      this.chart.data = data.objects;
      // data.map((v) => {
      //   this.chart.data.push({
      //     x: v.dates,
      //     y: v.objects
      //   })
      // })
      console.log(JSON.stringify(this.chart.data))
    },
    startInterval() {
      clearTimeout(this.tick); //tick <-어디 있는 변수?
      this.tick = setTimeout(async () => {
        this.getSensorLogTempData();
      }, 1000)
    },
    async getSensorLogTempData(){
      if(this.chart.sensor == undefined || this.chart.sensor == null){
        clearTimeout(this.tick)
        return
      }
      let params = {
        range_value: this.chart.range_value + 1,
        sensor_id: this.chart.sensor,
      };
      let { data } = await this.$http.post("sensor_data_range", params)
      this.data_objs.cate = [];
      this.data_objs.data_list = [];
      this.data_objs.cate = data.sensor_rt_data_list.map(v => v.event_datetime.slice(-8))
      data.sensor_rt_data_list.map((v) => this.data_objs.data_list.push({
        x:moment(v.event_datetime).valueOf(),
        y:Math.ceil(v.data * 8) / 8
      }));    
      if (this.$route.path == "/sensor_analysis") this.startInterval();
      this.refresh_cnt += 1;
      this.show_anomal_layer = (this.check_type == 1)? true:false
    },
    onShowGraph(item,row){
      this.sensor.selectedId = item.id
      this.chart.show=true;
      this.chart.sensor=item.sensor_id;
      this.data_objs.cate = [];
      this.data_objs.data_list = [];      
      this.startInterval()
    }

  },
  mounted() {
    this.getSensorLogTempData()
  },
  watch: {
    "sensor.options": {
      handler() {
        this.getSensor()
      },
      deep: true,
    },
  },
  computed:{
    chartOption_sensor_logs() {
      let obj = _.cloneDeep(chartOptions);
      obj.series[0].data = this.data_objs.data_list.map((v) => v.y);
      obj.xAxis[0].categories = this.data_objs.cate
      obj.yAxis[0].title.text = "데이터 값";
      obj.yAxis[0].max = 10
      obj.series[0].name = "감지기 데이터"
      return obj
    }
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
        selectedId: '',
        singleSelect: false,        
        headers: [
          {text: 'No.', value: 'id', sortable: false, align: 'center', width: 20 },
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
        total:0
      },
      loading: false,
      chart: {
        show: true,
        sensor: null,
        data: [],
        range_value:0,
        check_type:0,
        show_anomal_layer:true
      },
      data_objs: {
        data_list: [],
        cate: [],                           
      },      
      refresh_cnt:0,
      tick:null
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
.realtime-graph{
  width: 100%;
  height:200px;
}
.vrg-cls{
  margin: auto;

}
.vrg-item{
  margin-top:20px;
  
}
</style>
