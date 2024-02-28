<template>
  <main-layout>
    <template v-slot>
      <div class="main-panel">
        <v-toolbar color="light-blue darken-4" dark flat>
          <v-toolbar-title>수신기 관리</v-toolbar-title>
        </v-toolbar>

        <v-card flat>
          <v-toolbar rounded dense class="elevation-1">
            <v-col cols="5">
              <v-text-field outlined dense hide-details
                            placeholder="수신기 검색"
                            append-icon="mdi-magnify"
                            v-model="receiver.search"
                            @keydown.enter="getReceiver()"
                            class="m-right"
              />
            </v-col>
            <v-col cols="1">
              <v-btn depressed dark big
                      color="light-blue darken-2"
                      @click="getReceiver()">
                
                <div class="ml-1">조회</div>
              </v-btn>
            </v-col>
            <v-col cols="1">
              <v-btn depressed dark big
                      color="light-blue darken-2"
                      @click="addPopup.show=true"
                      class="m-left">
                <div class="ml-1">추가</div>
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
          :headers="receiver.headers"
          :items="receiver.data"
          :loading="receiver.loading"
          :options.sync="receiver.options"
          :server-items-length="receiver.total"
          :search="receiver.search"
          :items-per-page="5"
          :footer-props="{'items-per-page-options': [5, 10, 15,20,25,30,-1]}"
          @click:row="popupReceiverData"
          class="elevation-1 mt-4 clickable-row">
          <template v-slot:[`item.delete`]="{item}">
            <v-btn depressed small color="deep-orange accent-4"
                    dark class="ml-1"
                    @click.stop
                    @click="openDeletePopup(item)">
              삭제
            </v-btn>
          </template>
        </v-data-table>

        <v-dialog v-model="addPopup.show" persistent max-width="600px">
          <v-card>
            <v-card-title class="pt-2 pb-1 primary white--text">
              <span class="body-1">수신기 추가</span>
            </v-card-title>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="수신기 식별자"
                                  placeholder="수신기 식별자"
                                  v-model="addPopup.form.receiver_idx"
                    />
                  </v-col>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="고객식별자"
                                  placeholder="고객식별자"
                                  v-model="addPopup.form.fk_customer_idx"
                    />
                  </v-col>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="수신기 타입"
                                  placeholder="수신기 타입"
                                  v-model="addPopup.form.receiver_type"
                    />
                  </v-col>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="수신기 번호"
                                  placeholder="수신기 번호"
                                  v-model="addPopup.form.receiver_id"
                    />
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-action>
              <v-btn color="light-blue darken-2"
                      class="flex-grow-1"
                      text
                      @click="addPopup.show=false">
                취소  
              </v-btn>
              <v-btn color="primary"
                      class="flex-grow-1 ml-2"
                      dark depressed
                      @click="addReceiver()">
                추가  
              </v-btn>
            </v-card-action>
          </v-card>
        </v-dialog>

        <v-dialog v-model="infoPopup.show" persistent max-width="600px">
          <v-card>
            <v-card-title class="pt-2 pb-1 primary white--text">
              <span class="body-1">수신기 정보</span>
            </v-card-title>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="수신기 식별자"
                                  placeholder="수신기 식별자"
                                  v-model="infoPopup.form.receiver_idx"
                    />
                  </v-col>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="고객식별자"
                                  placeholder="고객식별자"
                                  v-model="infoPopup.form.fk_customer_idx"
                    />
                  </v-col>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="수신기 타입"
                                  placeholder="수신기 타입"
                                  v-model="infoPopup.form.receiver_type"
                    />
                  </v-col>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="수신기 번호"
                                  placeholder="수신기 번호"
                                  v-model="infoPopup.form.receiver_id"
                    />
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-action>
              <v-btn color="light-blue darken-2"
                      class="flex-grow-1"
                      text
                      @click="infoPopup.show=false">
                닫기  
              </v-btn>
              <v-btn color="primary"
                      class="flex-grow-1 ml-2"
                      dark depressed
                      @click="modifyReceiverData()">
                수정  
              </v-btn>
            </v-card-action>
          </v-card>
        </v-dialog>

        <v-dialog v-model="deletePopup.show" persistent max-width="600px">
          <v-card>
            <v-card-title>
              <span>삭제하시겠습니까?</span>
            </v-card-title>
            <v-card-action>
              <v-btn color="light-blue darken-2"
                      class="flex-grow-1"
                      text
                      @click="deletePopup.show=false">
                취소  
              </v-btn>
              <v-btn color="primary"
                      class="flex-grow-1 ml-2"
                      dark depressed
                      @click="deleteReceiver()">
                삭제  
              </v-btn>
            </v-card-action>
          </v-card>
        </v-dialog>

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
    async getReceiver() {

      let {data} = await this.$http.get("receiver")
      this.receiver.data = data.objects;
    },
    async addReceiver() {
      let param = this.addPopup.form;
      await this.$http.post("receiver", param)
      this.getReceiver()
      this.addPopup.show = false;
    },
    popupReceiverData(e, {item}) {
      this.infoPopup.form = item;
      this.infoPopup.show = true;
    },
    async modifyReceiverData() {
      let param = this.infoPopup.form;
      delete param.customer;
      await this.$http.patch(`receiver/${param.id}`, param)
      this.getReceiver()
      this.infoPopup.show = false;
    },
    openDeletePopup(item) {
      this.deletePopup.delTarget = item.id;
      this.deletePopup.show = true;
    },
    async deleteReceiver() {
      let param = this.deletePopup.delTarget;
      await this.$http.delete(`receiver/${param}`)
      this.getReceiver()
      this.deletePopup.show = false;
    }
  },
  mounted() {
    this.getReceiver()
  },
  watch: {
    "receiver.options": {
      handler() {
      },
      deep: true,
    },
  },
  data() {
    return {
      receiver: {
        headers: [
          {text: '수신기 식별자', value: 'receiver_idx', sortable: false,align: 'center', width: 80},
          {text: "고객 식별자", value: "fk_customer_idx",align: 'center', sortable: false, width: 60},
          {text: "수신기 타입", value: "receiver_type",align: 'center', sortable: false, width: 40},
          {text: "수신기 번호", value: "receiver_id",align: 'center', sortable: false, width: 20},
          {text: "삭제 여부", value: "delete",align: 'center', sortable: false, width: 20},
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
          receiver_idx: '',
          fk_customer_idx: '',
          receiver_type: '',
          receiver_id: '',
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
