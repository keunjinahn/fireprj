<template>
  <main-layout>
    <template v-slot>
      <div class="main-panel">
        <v-toolbar color="light-blue darken-4" dark flat>
          <v-toolbar-title>이벤트 리스트</v-toolbar-title>
        </v-toolbar>

        <v-card flat>
          <v-toolbar rounded dense class="elevation-1">
            <v-col cols="10"></v-col>
            <v-col cols="2">
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
          :items-per-page="5"
          :footer-props="{'items-per-page-options': [5, 10, 15,20,25,30,-1]}"
          @click:row="popupSensorData"
          class="elevation-1 mt-4">
          <template v-slot:item="row">
            <tr >
              <td >{{ row.item.event_datetime }}</td>
              <td >{{ row.item.event_type }}</td>
              <td >{{ row.item.customer.customer_name }}</td>
              <td >{{ row.item.receiver_type }}</td>
              <td >{{ row.item.receiver_id }}</td>
              <td >{{ row.item.system_id }}</td>
              <td >{{ row.item.repeater_id }}</td>
              <td >{{ row.item.sensor_id }}</td>
              <!-- <td >{{ row.item. }}</td> -->
            </tr>
          </template>
        </v-data-table>
      </div>
    </template>
  </main-layout> 
</template>

<script>
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
  },
  mounted() {
    this.getSensor()
  },
  watch: {
  },
  data() {
    return {
      sensor: {
        headers: [
          {text: "이벤트 시간", value: "event_datetime", sortable: false,align: 'center', width: 80},
          {text: "이벤트 구분", value: "event_type",align: 'center', sortable: false, width: 60},
          {text: "고객명", value: "customer.customer_name",align: 'center', sortable: false, width: 40},
          {text: "수신기 타입", value: "receiver_type",align: 'center', sortable: false, width: 20},
          {text: "수신기 번호", value: "receiver_id",align: 'center', sortable: false, width: 20},
          {text: "계통 번호", value: "system_id",align: 'center', sortable: false, width: 20},
          {text: "중계기 번호", value: "repeater_id",align: 'center', sortable: false, width: 20},
          {text: "감지기 번호", value: "sensor_id",align: 'center', sortable: false, width: 20},
          {text: "회선 설명", value: "",align: 'center', sortable: false, width: 20},
        ],
        data: [],
        options: {"page":1,"itemsPerPage":5,"sortBy":[],"sortDesc":[],"groupBy":[],"groupDesc":[],"mustSort":false,"multiSort":false},
        loading: false,
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
