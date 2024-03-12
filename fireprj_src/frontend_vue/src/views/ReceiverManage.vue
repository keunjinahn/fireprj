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
                      class="m-left"
                      @click="downloadExcel()">
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
          @click:row="openViewPopup"
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
                    @click="openModifyPopup(item,'MODIFY')">
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
              <span class="body-1">{{getPopupTitle(addPopup.popup_type)}}</span>
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
                                  :disabled="addPopup.popup_type != 'ADD'"
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
                            <input type="text" :disabled="addPopup.popup_type == 'VIEW'" placeholder="000" class="abl-input" v-model="addPopup.form.receiver_type"/>
                          </td>
                        </tr>       
                        <tr>
                          <th class="s-h" colspan="2" rowspan="1">수신기 번호</th>
                          <td colspan="2">
                            <input type="text" :disabled="addPopup.popup_type == 'VIEW'" placeholder="000" class="abl-input" v-model="addPopup.form.receiver_id"/>
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
                  v-if="addPopup.popup_type != 'VIEW'"
              >
              {{getPopupTitle(addPopup.popup_type)}}
              </v-btn>
            </v-card-actions>
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
import axios from "axios";
export default {
  props: {
  },
  components: {},
  methods: {
    openAddPopup(){
      if(!this.$session.isAdmin()){
        alert("권한이 없습니다.")
        return
      }

      this.clearPopup();
      this.getCustomer();
      this.addPopup.popup_type = 'ADD'
      this.addPopup.show = true
      
    },
    openModifyPopup(item,type){
      if(!this.$session.isAdmin()){
        alert("권한이 없습니다.")
        return
      }
      this.addPopup.popup_type = type
      this.addPopup.show = true
      this.addPopup.selected_custommer  = this.customer_list.find(v=>v.customer_idx==item.fk_customer_idx)
      this.updateCustomer(this.addPopup.selected_custommer)
      this.addPopup.form.receiver_id = String(item.receiver_id).padStart(3,'0')
      this.addPopup.form.receiver_type = String(item.receiver_type).padStart(3,'0')
      this.addPopup.form.receiver_idx = item.receiver_idx
      this.addPopup.form.id = item.id
    },
    openViewPopup(item){
      this.openModifyPopup(item,'VIEW')
    },
    getPopupTitle(type){
      if(type == 'ADD') return '수신기 등록'
      if(type == 'MODIFY') return '수신기 수정'
      if(type == 'VIEW') return '수신기 정보'
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
      this.updateCustomer(this.addPopup.selected_custommer)
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

      const { page, itemsPerPage, sortBy, sortDesc } = this.receiver.options;
      try {
        let filters_or = []
        let filters_and = []
        let order_by = []
        if (this.receiver.search) {
          filters_or.push({name: 'customer', op: 'has', val: {name: "customer_name", op: "like", val: `%${this.receiver.search}%`}});
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

        let { data } = await this.$http.get("receiver", { params });
        this.receiver.total = data.num_results;
        this.receiver.data = data.objects.map((v, i) => {
          v._index = i + (page - 1) * itemsPerPage + 1;
          return v;
        });
      } catch (err) {
        console.error(err);
      } finally {
        this.receiver.loading = false;
      }
    },
    async addReceiver() {
      
      let param = {
        fk_customer_idx:this.addPopup.form.customer_idx,
        receiver_idx: String(this.addPopup.form.customer_idx).padStart(5,'0') + "_" + String(this.addPopup.form.receiver_type).padStart(3,'0') 
        + "_" + String(this.addPopup.form.receiver_id).padStart(3,'0'),
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
      if(!this.$session.isAdmin()){
        alert("권한이 없습니다.")
        return
      }      
      this.deletePopup.delTarget = item.id;
      this.deletePopup.show = true;
    },
    async deleteReceiver() {
      let param = this.deletePopup.delTarget;
      await this.$http.delete(`receiver/${param}`)
      this.getReceiver()
      this.deletePopup.show = false;
    },
    async downloadExcel() {
      let params = {
        "page_name": "receiver_manage",
        "headers": (() => {
          let headers_text = []
          for (let i=1; i < this.receiver.headers.length-1; i++) {
            headers_text.push(this.receiver.headers[i].text)
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
        var download_file_name = "수신기목록_" + Date.now().toString() + ".xlsx"
        link.setAttribute('download', download_file_name)
        link.click()
      })
      .catch(() => console.log('error: excel download error'))
    }
  },
  mounted() {
    this.getCustomer()
    this.getReceiver()
  },
  watch: {
    "receiver.options": {
      handler() {
        this.getReceiver()
      },
      deep: true,
    },
  },
  data() {
    return {
      customer_list:[],
      receiver: {
        headers: [
          {text: 'No.', value: 'id', sortable: false, align: 'center', width: 20 },
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
        total:0
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
