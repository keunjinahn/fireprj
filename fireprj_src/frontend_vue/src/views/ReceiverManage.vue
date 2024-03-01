<template>
  <main-layout>
    <template v-slot>
      <div class="main-panel">
        <v-toolbar color="light-blue darken-4" dark flat>
          <v-toolbar-title>수신기 관리</v-toolbar-title>
        </v-toolbar>

        <v-card flat height="100">
          <v-toolbar rounded dense class="elevation-1" height="100">
            <v-col cols="8">
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
                      @click="openAddPopup"
                      class="m-left">
                <v-icon small>mdi-plus</v-icon>
                <div class="ml-1">추가</div>
              </v-btn>
            </v-col>
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
          :headers="receiver.headers"
          :items="receiver.data"
          :loading="receiver.loading"
          :options.sync="receiver.options"
          :server-items-length="receiver.total"
          :search="receiver.search"
          :items-per-page="5"
          :footer-props="{'items-per-page-options': [5, 10, 15,20,25,30,-1]}"
          class="elevation-1 mt-4 clickable-row">
          <template v-slot:[`item.fk_customer_idx`]="{item}">
            {{String(item.fk_customer_idx).padStart(5,'0')}}
          </template>
          <template v-slot:[`item.receiver_type`]="{item}">
            {{String(item.receiver_type).padStart(3,'0')}}
          </template>    
          <template v-slot:[`item.receiver_id`]="{item}">
            {{String(item.receiver_id).padStart(3,'0')}}
          </template>           
          <template v-slot:[`item.delete`]="{item}">
            <v-btn depressed small color="#aaaaaa"
                    dark class="ml-1"
                    @click.stop
                    @click="openModifyPopup(item)">
              수정
            </v-btn>            
            <v-btn depressed small color="deep-orange accent-4"
                    dark class="ml-1"
                    @click.stop
                    @click="openDeletePopup(item)">
              삭제
            </v-btn>
          </template>
        </v-data-table>
        <v-dialog v-model="addPopup.show" persistent max-width="500px">
          <v-card :loading="loading" :disabled="loading">
            <v-card-title class="pt-2 pb-1 primary white--text">
              <span class="body-1">{{(addPopup.popup_type == 'ADD')? '수신기 등록':'수신기 수정'}}</span>
            </v-card-title>
            <v-divider />
            <v-card-text>
              <v-container>
                <v-card>
                  <abl-document class="abl-page-popup" ref="report-popup">
                    <abl-doc-body class="abl-doc-body-popup">
                      <table class="abl-table-ts-popup">
                        <colgroup>
                          <col style="width: 25%" />
                        </colgroup>
                        <tr>
                            <th class="s-h" colspan="2" rowspan="1">고객명</th>
                            <td colspan="2">
                              <v-select dense hide-details
                                  v-model="addPopup.selected_custommer"
                                  :items="customer_list"
                                  item-text="customer_name"
                                  item-value="customer_idx"
                                  @change="onChangeCustomer"
                                >
                              </v-select>
                            </td>
                        </tr>          
                        <tr>
                          <th class="s-h" colspan="2" rowspan="1">고객 주소</th>
                          <td colspan="2">
                            <input type="text" disabled placeholder="고객 주소" class="abl-input" v-model="addPopup.form.customer_address"/>
                          </td>
                        </tr>   
                        <tr>
                          <th class="s-h" colspan="2" rowspan="1">고객 전화번호</th>
                          <td colspan="2">
                            <input type="text" disabled placeholder="고객 전화번호" class="abl-input" v-model="addPopup.form.customer_tel"/>
                          </td>
                        </tr>   
                        <tr>
                          <th class="s-h" colspan="2" rowspan="1">고객 식별자</th>
                          <td colspan="2">
                            <input type="text" disabled placeholder="고객 식별자" class="abl-input" v-model="addPopup.form.customer_idx"/>
                          </td>
                        </tr>     
                        <tr>
                          <th class="s-h" colspan="2" rowspan="1">수신기 타입</th>
                          <td colspan="2">
                            <input type="text" placeholder="000" class="abl-input" v-model="addPopup.form.receiver_type"/>
                          </td>
                        </tr>       
                        <tr>
                          <th class="s-h" colspan="2" rowspan="1">수신기 번호</th>
                          <td colspan="2">
                            <input type="text" placeholder="000" class="abl-input" v-model="addPopup.form.receiver_id"/>
                          </td>
                        </tr>                                                                                                                                                                                                                                                                 
                      </table>
                    </abl-doc-body>
                  </abl-document>                                   
                </v-card>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-btn
                  color="light-blue darken-2"
                  class="flex-grow-1"
                  text
                  @click="addPopup.show=false"
              >
                닫기
              </v-btn>
              <v-btn
                  color="light-blue darken-2"
                  class="flex-grow-1"
                  tile
                  dark
                  depressed
                  @click="addReceiver"
              >
              {{(addPopup.popup_type == 'ADD')? '수신기 등록':'수신기 수정'}}
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>


         <!-- <v-dialog v-model="infoPopup.show" persistent max-width="600px">
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
        </v-dialog> -->

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
    openAddPopup(){
      this.clearPopup();
      this.getCustomer();
      this.addPopup.popup_type = 'ADD'
      this.addPopup.show = true
      
    },
    openModifyPopup(item){
      this.addPopup.popup_type = 'MODIFY'
      this.addPopup.show = true
      const customer = this.customer_list.find(v=>v.customer_idx==item.fk_customer_idx)
      this.updateCustomer(customer)
      this.addPopup.form.receiver_id = String(item.receiver_id).padStart(3,'0')
      this.addPopup.form.receiver_type = String(item.receiver_type).padStart(3,'0')
      this.addPopup.form.receiver_idx = item.receiver_idx
      this.addPopup.form.id = item.id
    },
    clearPopup(){
      this.addPopup.form = {
          receiver_idx: '',
          fk_customer_idx: '',
          receiver_type: '',
          receiver_id: '',
          customer_idx:0,
          customer_address:'',
          customer_tel:'',
          id:''
        }
    },
    async getCustomer() {
      let {data} = await this.$http.get("customer")
      data.objects.map((v)=>this.customer_list.push({
        customer_name:v.customer_name,
        customer_tel:v.customer_tel,
        customer_address:v.customer_address,
        customer_idx:v.customer_idx
      }));
      this.addPopup.selected_custommer = this.customer_list[0]
      this.updateCustomer( this.customer_list[0])
    },
    updateCustomer(item){
      this.addPopup.form.customer_idx = String(item.customer_idx).padStart(5,'0')
      this.addPopup.form.customer_tel = item.customer_tel
      this.addPopup.form.customer_address = item.customer_address
    },
    onChangeCustomer(customer_idx){
      const item = this.customer_list.find(v=>v.customer_idx==customer_idx)
      this.updateCustomer(item)
    },
    async getReceiver() {

      let {data} = await this.$http.get("receiver")
      this.receiver.data = data.objects;
    },
    async addReceiver() {
      
      let param = {
        fk_customer_idx:this.addPopup.form.customer_idx,
        receiver_idx: String(this.addPopup.form.customer_idx).padStart(5,'0') + "_" + String(this.addPopup.form.receiver_type).padStart(3,'0') + "_" + String(this.addPopup.form.receiver_id).padStart(3,'0'),
        receiver_type:this.addPopup.form.receiver_type,
        receiver_id:this.addPopup.form.receiver_id,
      };
      if(this.addPopup.popup_type == 'ADD') {
        await this.$http.post("receiver", param)
      }else {
        await this.$http.patch(`receiver/${this.addPopup.form.id}`, param)
      }
      
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
    this.getCustomer()
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
      customer_list:[],
      receiver: {
        headers: [
          {text: '수신기 식별자', value: 'receiver_idx', sortable: false,align: 'center', width: 80},
          {text: "고객 식별자", value: "fk_customer_idx",align: 'center', sortable: false, width: 60},
          {text: "수신기 타입", value: "receiver_type",align: 'center', sortable: false, width: 40},
          {text: "수신기 번호", value: "receiver_id",align: 'center', sortable: false, width: 20},
          {text: "수정/삭제", value: "delete",align: 'center', sortable: false, width: 10},
        ],
        data: [],
        options: {"page":1,"itemsPerPage":10,"sortBy":[],"sortDesc":[],"groupBy":[],"groupDesc":[],"mustSort":false,"multiSort":false},
        loading: false,
        search: '',
      },
      loading: false,
      addPopup: {
        show: false,
        selected_custommer:null,
        form: {
          receiver_idx: '',
          fk_customer_idx: '',
          receiver_type: '',
          receiver_id: '',
          customer_idx:0,
          customer_address:'',
          customer_tel:'',
          id:''
        },
        loading:false,
        popup_type:'ADD'

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
