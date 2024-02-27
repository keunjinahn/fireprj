<template>
  <main-layout>
    <template v-slot>
      <div class="main-panel">
        <v-toolbar color="light-blue darken-4" dark flat>
          <v-toolbar-title>실시간 감지기</v-toolbar-title>
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
          class="elevation-1 mt-4">
          <template v-slot:item="row">
            <tr>
              <td >{{ row.item.fk_customer_idx }}</td>
              <td >{{ row.item.customer.customer_name }}</td>
              <td >{{ row.item.receiver_type }}</td>
              <td >{{ row.item.receiver_id}}</td>
              <td >{{ row.item.system_id}}</td>
              <td >{{ row.item.repeater_id }}</td>
              <td >{{ row.item.sensor_id }}</td>
              <td >{{ row.item.regist_status }}</td>
              <td >{{ row.item.action_status }}</td>
              <td >{{ row.item.network_status }}</td>
              <td >{{ row.item.battery_status }}</td>
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
    async getSensorEvent() {
      let {data} = await this.$http.get("sensor_event")
      this.sensor.data = data.objects;
    },
    // async getSensorEvent(page_reset) {
    //   this.sensor.loading = true;
    //   if(page_reset == true){
    //     this.sensor.options.page = 1
    //   }
    //   const { page, itemsPerPage} = this.sensor.options;
      
    //   try {

    //     let params = {
    //       results_per_page: itemsPerPage,
    //       page: page,
    //     };
       

    //     let { data } = await this.$http.get("sensor-event", { params });
    //     alert(1)
    //     this.sensor.total = data.num_results;
    //     this.sensor.data = data.objects.map((v, i) => {
    //       v._index = i + (page - 1) * itemsPerPage + 1;
    //       return v;
          
    //     });
    //     alert(JSON.stringify(data))
    //   }
    //    catch (err) {
    //     console.error(err);
    //   } finally {
    //     this.sensor.loading = false;
    //   }
    // },

  },
  mounted() {
    this.getSensorEvent()
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
          {text: "고객 식별자", value: "fk_customer_idx",align: 'center', sortable: false, width: 60},
          {text: "고객명", value: "customer.customer_name",align: 'center', sortable: false, width: 40},
          {text: "수신기 타입", value: "receiver_type",align: 'center', sortable: false, width: 20},
          {text: "수신기 번호", value: "receiver_id",align: 'center', sortable: false, width: 20},
          {text: "계통 번호", value: "system_id",align: 'center', sortable: false, width: 20},
          {text: "중계기 번호", value: "repeater_id",align: 'center', sortable: false, width: 20},
          {text: "감지기 번호", value: "sensor_id",align: 'center', sortable: false, width: 20},
          {text: "등록 상태", value: "regist_status",align: 'center', sortable: false, width: 20},
          {text: "동작 상태", value: "action_status",align: 'center', sortable: false, width: 20},
          {text: "통신 상태", value: "network_status",align: 'center', sortable: false, width: 20},
          {text: "배터리 상태", value: "battery_status",align: 'center', sortable: false, width: 20},
        ],
        data: [],
        options: {"page":1,"itemsPerPage":5,"sortBy":[],"sortDesc":[],"groupBy":[],"groupDesc":[],"mustSort":false,"multiSort":false},
        loading: false,
      },
      loading: false,
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
