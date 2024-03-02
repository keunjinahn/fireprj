<template>
  <main-layout>
    <template v-slot>
      <div class="main-panel">
        <v-toolbar color="light-blue darken-4" dark flat>
          <v-toolbar-title>대시보드</v-toolbar-title>
        </v-toolbar>

        <v-card flat>
          <v-row>
            <v-col cols="6">
              <v-card light outlined color="white">
                <v-card-title class="body-1 font-weight-bold py-2">감지기 가동현황</v-card-title>
                <v-divider/>
                <v-card-text>
                  <highcharts
                    constructor-type="chart"
                    :options="chart1Option"
                  />
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="6">
              <v-card light outlined color="white">
                <v-card-title class="body-1 font-weight-bold py-2"></v-card-title>
                <v-divider/>
                <v-card-text>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>          
        </v-card>

        
      </div>
    </template>
  </main-layout> 
</template>

<script>

const pieOptions = {
  colors: ['#003f5c', '#58508d','#bc5090', '#ff6361', '#ffa600','#aa3f5c', '#aa508d','#aa5090', '#aa6361', '#aaa600'],
  chart: {
    plotBackgroundColor: null,
    plotBorderWidth: null,
    plotShadow: false,
    type: 'pie'
  },
  title: {
    text: ''
  },
  tooltip: {
    pointFormat: '<b>{point.name2}</b>: {point.y} 백만원'
  },
  accessibility: {
    point: {
      valueSuffix: '%'
    }
  },
  plotOptions: {
    pie: {
      allowPointSelect: true,
      cursor: 'pointer',
      dataLabels: {
        enabled: true,
        format: '<b>{point.name1}</b>: {point.y} 개교 '
      },
      showInLegend: true
    }
  },
  series: [{
    name: 'Brands',
    colorByPoint: true,
    data: []
  }],
}
import _ from 'lodash'
import moment from 'moment'
import axios from "axios";
export default {
  props: {
  },
  components: {},
  methods: {
    async getSensor() {

      const { page, itemsPerPage, sortBy, sortDesc } = this.sensor.options;
      try {
        let { data } = await this.$http.get("event_list");
      } catch (err) {
        console.error(err);
      } finally {
        this.sensor.loading = false;
      }      
       
    },
  },
  mounted() {
    this.getSensor()
  },
  computed: {
    chart1Option () {
      let obj = _.cloneDeep(pieOptions)
      obj.xAxis[0].categories = this.data.by_year.map(v => v.year)
      obj.series[0].data = this.data.by_year.map(v => v.count)
      obj.series[0].name = '가동 감지기수'
      obj.series[1].data = this.data.by_year.map(v => (Math.floor(v.cost/1000000)))
      obj.series[1].name = '미가동 감지기수'

      return obj
    },
  },
  watch: {
    "sensor.options": {
      handler() {
        this.getSensor()
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
        options: {"page":1,"itemsPerPage":20,"sortBy":[],"sortDesc":[],"groupBy":[],"groupDesc":[],"mustSort":false,"multiSort":false},
        loading: false,
        search: '',
        total:0
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
      ,data:[]
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
