<template>
  <main-layout>
    <template v-slot>
      <div class="main-panel">
        <v-toolbar color="light-blue darken-4" dark flat>
          <v-toolbar-title>고객사 관리</v-toolbar-title>
        </v-toolbar>

        <v-card flat height="100">
          <v-toolbar rounded dense class="elevation-1" height="100">
            <v-col cols="8">
              <v-text-field outlined dense hide-details
                            placeholder="고객사 검색"
                            append-icon="mdi-magnify"
                            v-model="users.search"
                            @keydown.enter="getUser()"
                            class="m-right"
              />
            </v-col>
            <v-col cols="1">
              <v-btn depressed dark big
                      color="light-blue darken-2"
                      @click="getUser()">
                
                <div class="ml-1">조회</div>
              </v-btn>
            </v-col>
            <v-col cols="1">
              <v-btn depressed dark big
                      color="light-blue darken-2"
                      @click="openAddPopup()"
                      class="m-left">
                <div class="ml-1">추가</div>
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
          :headers="users.headers"
          :items="users.data"
          :loading="users.loading"
          :options.sync="users.options"
          :server-items-length="users.total"
          :search="users.search"
          :items-per-page="5"
          :footer-props="{'items-per-page-options': [5, 10, 15,20,25,30,-1]}"
          @click:row="openViewPopup"
          class="elevation-1 mt-4 clickable-row">                   
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
                            <th class="s-h" colspan="2" rowspan="1">고객사 이름</th>
                            <td colspan="2">
                               <input :disabled="addPopup.popup_type == 'VIEW'" type="text" placeholder="고객사 이름" class="abl-input" v-model="addPopup.form.customer_name"/>
                            </td>
                        </tr>          
                        <tr>
                          <th class="s-h" colspan="2" rowspan="1">전화번호</th>
                          <td colspan="2">
                            <input :disabled="addPopup.popup_type == 'VIEW'" type="text" placeholder="전화번호" class="abl-input" v-model="addPopup.form.customer_tel"/>
                          </td>
                        </tr>   
                        <tr>
                          <th class="s-h" colspan="2" rowspan="1">주소</th>
                          <td colspan="2">
                            <input :disabled="addPopup.popup_type == 'VIEW'" type="text" placeholder="주소" class="abl-input" v-model="addPopup.form.customer_address"/>
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
                  @click="addUser()"
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
                      @click="deleteUser()">
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
    clearUser() {
      this.addPopup.form =  {
          customer_idx:0,
          customer_name: '',
          customer_tel: '',
          customer_address: '',

        }      
    },
    openAddPopup() {
      if(!this.$session.isAdmin()){
        alert("권한이 없습니다.")
        return
      }        
      this.clearUser()
      this.getUser()
      this.addPopup.popup_type = 'ADD'
      this.addPopup.show = true
    },
    openModifyPopup(item,type) {
      if(!this.$session.isAdmin()){
        alert("권한이 없습니다.")
        return
      }        
      this.addPopup.form.customer_name = item.customer_name
      this.addPopup.form.customer_tel = item.customer_tel
      this.addPopup.form.customer_address = item.customer_address
      this.addPopup.popup_type = type
      this.addPopup.form.customer_idx = item.customer_idx
      this.addPopup.show = true      
      
    },   
    openViewPopup(item){
      this.openModifyPopup(item,'VIEW')
    },
    getPopupTitle(type){
      if(type == 'ADD') return '고객사 등록'
      if(type == 'MODIFY') return '고객사 수정'
      if(type == 'VIEW') return '고객사 정보'
    },
    async getUser() {
      
      const { page, itemsPerPage, sortBy, sortDesc } = this.users.options;
      try {
        let filters_or = []
        let filters_and = []
        let order_by = []
        if (this.users.search) {
          filters_or.push({name: 'customer_name', op: 'like', val: `%${this.users.search}%`})
        }
        if (sortBy.length) {
          for (let i=0; i<sortBy.length; i++) {
            order_by.push({field: sortBy[i], direction: sortDesc[i] ? 'desc' : 'asc'})
          }
        }else{
          order_by.push({field: "customer_idx", direction: 'asc'})
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
        
        let { data } = await this.$http.get("customer", { params });
        this.users.total = data.num_results;
        this.users.data = data.objects.map((v, i) => {
          v._index = i + (page - 1) * itemsPerPage + 1;
          return v;
        });
      } catch (err) {
        console.error(err);
      } finally {
        this.users.loading = false;
      }   
    },
    async addUser() {
      if(this.addPopup.form.customer_name == undefined || this.addPopup.form.customer_name.length < 5){
        alert("이름을 입력해 주세요!")
        return
      }
      if(this.addPopup.form.customer_tel == undefined || this.addPopup.form.customer_tel.length < 10){
        alert("전화번호를 입력해 주세요!")
        return
      }      
      if(this.addPopup.form.customer_address == undefined || this.addPopup.form.customer_address.length < 5){
        alert("주소를 입력해 주세요!")
        return
      }       
      let param = {
        customer_name: this.addPopup.form.customer_name,
        customer_tel: this.addPopup.form.customer_tel,
        customer_address: this.addPopup.form.customer_address,
      }
      if (this.addPopup.popup_type == 'ADD') {
        await this.$http.post("customer", param)
      } else {
        await this.$http.patch(`customer/${this.addPopup.form.customer_idx}`, param)  
      }
      this.getUser()
      this.addPopup.show = false;
    },
    popupUserData(e, {item}) {
      this.infoPopup.form = item;
      this.infoPopup.show = true;
    },
    // async modifyUserData() {
    //   let param = this.infoPopup.form;
    //   delete param.customer;
    //   await this.$http.patch(`user/${param.id}`, param)
    //   this.getUser()
    //   this.infoPopup.show = false;
    // },
    openDeletePopup(item) {
      if(!this.$session.isAdmin()){
        alert("권한이 없습니다.")
        return
      }        
      this.deletePopup.delTarget = item.customer_idx;
      this.deletePopup.show = true;
    },
    async deleteUser() {
      let param = this.deletePopup.delTarget;
      await this.$http.delete(`customer/${param}`)
      this.getUser()
      this.deletePopup.show = false;
    },
    async downloadExcel() {
      let params = {
        "page_name": "crm",
        "headers": (() => {
          let headers_text = []
          for (let i=1; i < this.users.headers.length-1; i++) {
            headers_text.push(this.users.headers[i].text)
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
        var download_file_name = "고객사목록_" + Date.now().toString() + ".xlsx"
        link.setAttribute('download', download_file_name)
        link.click()
      })
      .catch(() => console.log('error: excel download error'))
    }
  },
  mounted() {
    this.getUser()
  },
  watch: {
    "users.options": {
      handler() {
        this.getUser()
      },
      deep: true,
    },
  },
  data() {
    return {
      users: {
        headers: [
          {text: 'No.', value: 'customer_idx', sortable: false, align: 'center', width: 20 },
          {text: '고객사 이름', value: 'customer_name', sortable: false,align: 'center', width: 80},
          {text: "전화번호", value: "customer_tel",align: 'center', sortable: false, width: 60},
          {text: "주소", value: "customer_address",align: 'center', sortable: false, width: 40},
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
        form: {
          customer_idx:'',
          customer_name: '',
          customer_tel: '',
          customer_address: '',
        },
        loading:false,
        popup_type: 'ADD',
      },
      infoPopup: {
        show: false,
        form: {}
      },
      deletePopup: {
        show: false,
        delTarget: ''
      },   
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
