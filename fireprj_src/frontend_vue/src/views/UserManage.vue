<template>
  <main-layout>
    <template v-slot>
      <div class="main-panel">
        <v-toolbar color="light-blue darken-4" dark flat>
          <v-toolbar-title>사용자 관리</v-toolbar-title>
        </v-toolbar>

        <v-card flat height="100">
          <v-toolbar rounded dense class="elevation-1" height="100">
            <v-col cols="7">
              <v-text-field outlined dense hide-details
                            placeholder="사용자 검색"
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
          class="elevation-1 mt-4 clickable-row">
          <template v-slot:[`item.user_pwd`]="{item}">
            *****
          </template>           
          <template v-slot:[`item.user_status`]="{item}">
            {{user_status_list.find(v=>v.code==item.user_status).name}}
          </template>           
          <template v-slot:[`item.user_role`]="{item}">
            {{user_role_list.find(v=>v.code==item.user_role).name}}
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
              <span class="body-1">{{(addPopup.popup_type == 'ADD')? '사용자 등록':'사용자 수정'}}</span>
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
                            <th class="s-h" colspan="2" rowspan="1">사용자 식별자</th>
                            <td colspan="2">
                               <input type="text" placeholder="영문 아이디" class="abl-input" v-model="addPopup.form.user_id"/>
                            </td>
                        </tr>          
                        <tr>
                          <th class="s-h" colspan="2" rowspan="1">사용자 비밀번호</th>
                          <td colspan="2">
                            <input type="text" placeholder="*******" class="abl-input" v-model="addPopup.form.user_pwd"/>
                          </td>
                        </tr>   
                        <tr>
                          <th class="s-h" colspan="2" rowspan="1">사용자 성명</th>
                          <td colspan="2">
                            <input type="text" placeholder="사용자 성명" class="abl-input" v-model="addPopup.form.user_name"/>
                          </td>
                        </tr>   
                        <tr>
                          <th class="s-h" colspan="2" rowspan="1">사용자 상태</th>
                          <td colspan="2">
                              <v-select dense hide-details
                                  v-model="addPopup.selected_status"
                                  :items="user_status_list"
                                  item-text="name"
                                  item-value="code"
                                  @change="onChangeUserStatus"
                                >
                              </v-select>
                          </td>
                        </tr>     
                        <tr>
                          <th class="s-h" colspan="2" rowspan="1">사용자 권한</th>
                          <td colspan="2">
                              <v-select dense hide-details
                                  v-model="addPopup.selected_role"
                                  :items="user_role_list"
                                  item-text="name"
                                  item-value="code"
                                  @change="onChangeUserRole"
                                >
                              </v-select>
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
                  @click="addUser"
              >
              {{(addPopup.popup_type == 'ADD')? '사용자 등록':'사용자 수정'}}
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
          user_id: '',
          user_pwd: '',
          user_name: '',
          user_status: '',
          user_role: '',
        }      
    },
    openAddPopup() {
      this.clearUser()
      this.addPopup.selected_status = this.user_status_list[0]
      this.addPopup.selected_role = this.user_role_list[0]
      this.addPopup.popup_type = 'ADD'
      this.addPopup.show = true
    },
    openModifyPopup(item) {
      this.addPopup.selected_status = this.user_status_list.find(v => v.code == item.user_status)
      this.addPopup.selected_role = this.user_role_list.find(v => v.code == item.user_role)
      this.addPopup.form.user_id = item.user_id
      this.addPopup.form.user_pwd = '*****'
      this.addPopup.form.user_name = item.user_name
      this.addPopup.form.id = item.id
      this.addPopup.popup_type = 'MODIFY'
      this.addPopup.show = true      
      
    },
    onChangeUserStatus(status) {
      this.addPopup.form.user_status = status
    },
    onChangeUserRole(role) {
      this.addPopup.form.user_role = role
    },    
    async getUser() {

      const { page, itemsPerPage, sortBy, sortDesc } = this.users.options;
      try {
        let filters_or = []
        let filters_and = []
        let order_by = []
        if (this.users.search) {
          filters_or.push({name: 'user_id', op: 'like', val: `%${this.users.search}%`})
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

        let { data } = await this.$http.get("user", { params });
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
      let param = {
        user_id: this.addPopup.form.user_id,
        user_pwd: this.addPopup.form.user_pwd,
        user_name: this.addPopup.form.user_name,
        user_status: this.addPopup.form.user_status,
        user_role: this.addPopup.form.user_role,
      }
      if (this.addPopup.popup_type == 'ADD') {
        await this.$http.post("user", param)
      } else {
        await this.$http.patch(`user/${this.addPopup.form.id}`, param)  
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
      this.deletePopup.delTarget = item.id;
      this.deletePopup.show = true;
    },
    async deleteUser() {
      let param = this.deletePopup.delTarget;
      await this.$http.delete(`user/${param}`)
      this.getUser()
      this.deletePopup.show = false;
    },
    async downloadExcel() {
      let params = {
        "page_name": "user",
        "headers": (() => {
          let headers_text = []
          for (let i=0; i < this.users.headers.length-1; i++) {
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
        var download_file_name = "사용자목록_" + Date.now().toString() + ".xlsx"
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
          {text: 'No.', value: 'id', sortable: false, align: 'center', width: 20 },
          {text: '사용자 식별자', value: 'user_id', sortable: false,align: 'center', width: 80},
          {text: "사용자 비밀번호", value: "user_pwd",align: 'center', sortable: false, width: 60},
          {text: "사용자 성명", value: "user_name",align: 'center', sortable: false, width: 40},
          {text: "사용자 상태", value: "user_status",align: 'center', sortable: false, width: 20},
          {text: "사용자 권한", value: "user_role",align: 'center', sortable: false, width: 20},
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
          user_id: '',
          user_pwd: '',
          user_name: '',
          user_status: '',
          user_role: '',
          id:''
        },
        loading:false,
        popup_type: 'ADD',
        selected_status: null,
        selected_role:null
      },
      infoPopup: {
        show: false,
        form: {}
      },
      deletePopup: {
        show: false,
        delTarget: ''
      },
      user_status_list: [
        { name:'미사용',code: 0},        
        { name: '사용', code: 1 }
      ],
      user_role_list: [
        { name:'조회',code: 0},        
        { name: '관리', code: 1 }
      ]      
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
