<template>
  <main-layout>
    <template v-slot>
      <div class="main-panel">
        <v-toolbar color="light-blue darken-4" dark flat>
          <v-toolbar-title>사용자 관리</v-toolbar-title>
        </v-toolbar>

        <v-card flat>
          <v-toolbar rounded dense class="elevation-1">
            <v-col cols="10"></v-col>
            <v-col cols="2">
              <v-btn depressed dark big
                      color="light-blue darken-2"
                      @click="addPopup.show=true"
                      class="m-left">
                <div class="ml-1">추가</div>
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
          :items-per-page="5"
          :footer-props="{'items-per-page-options': [5, 10, 15,20,25,30,-1]}"
          @click:row="popupUserData"
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
              <span class="body-1">사용자 추가</span>
            </v-card-title>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="사용자 식별자"
                                  placeholder="사용자 식별자"
                                  v-model="addPopup.form.user_id"
                    />
                  </v-col>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="사용자 비밀번호"
                                  placeholder="사용자 비밀번호"
                                  v-model="addPopup.form.user_pwd"
                    />
                  </v-col>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="사용자 성명"
                                  placeholder="사용자 성명"
                                  v-model="addPopup.form.user_name"
                    />
                  </v-col>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="사용자 상태"
                                  placeholder="사용자 상태"
                                  v-model="addPopup.form.user_status"
                    />
                  </v-col>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="사용자 권한"
                                  placeholder="사용자 권한"
                                  v-model="addPopup.form.user_role"
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
                      @click="addUser()">
                추가  
              </v-btn>
            </v-card-action>
          </v-card>
        </v-dialog>

        <v-dialog v-model="infoPopup.show" persistent max-width="600px">
          <v-card>
            <v-card-title class="pt-2 pb-1 primary white--text">
              <span class="body-1">사용자 정보</span>
            </v-card-title>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="사용자 식별자"
                                  placeholder="사용자 식별자"
                                  v-model="infoPopup.form.user_id"
                    />
                  </v-col>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="사용자 비밀번호"
                                  placeholder="사용자 비밀번호"
                                  v-model="infoPopup.form.user_pwd"
                                  type="password"
                    />
                  </v-col>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="사용자 성명"
                                  placeholder="사용자 성명"
                                  v-model="infoPopup.form.user_name"
                    />
                  </v-col>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="사용자 상태"
                                  placeholder="사용자 상태"
                                  v-model="infoPopup.form.user_status"
                    />
                  </v-col>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="사용자 권한"
                                  placeholder="사용자 권한"
                                  v-model="infoPopup.form.user_role"
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
                      @click="modifyUserData()">
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
export default {
  props: {
  },
  components: {},
  methods: {
    async getUser() {

      let {data} = await this.$http.get("user")
      this.users.data = data.objects;
    },
    async addUser() {
      // 2번 호출되서 서버에 objectDeletedError 뜸
      let param = this.addPopup.form;
      await this.$http.post("user", param)
      this.getUser()
      this.addPopup.show = false;
    },
    popupUserData(e, {item}) {
      this.infoPopup.form = item;
      this.infoPopup.show = true;
    },
    async modifyUserData() {
      let param = this.infoPopup.form;
      delete param.customer;
      await this.$http.patch(`user/${param.id}`, param)
      this.getUser()
      this.infoPopup.show = false;
    },
    openDeletePopup(item) {
      this.deletePopup.delTarget = item.id;
      this.deletePopup.show = true;
    },
    async deleteUser() {
      let param = this.deletePopup.delTarget;
      await this.$http.delete(`user/${param}`)
      this.getUser()
      this.deletePopup.show = false;
    }
  },
  mounted() {
    this.getUser()
  },
  watch: {
  },
  data() {
    return {
      users: {
        headers: [
          {text: '사용자 식별자', value: 'user_id', sortable: false,align: 'center', width: 80},
          {text: "사용자 비밀번호", value: "user_pwd",align: 'center', sortable: false, width: 60},
          {text: "사용자 성명", value: "user_name",align: 'center', sortable: false, width: 40},
          {text: "사용자 상태", value: "user_status",align: 'center', sortable: false, width: 20},
          {text: "사용자 권한", value: "user_role",align: 'center', sortable: false, width: 20},
          {text: "삭제 여부", value: "delete",align: 'center', sortable: false, width: 20},
        ],
        data: [],
        options: {"page":1,"itemsPerPage":5,"sortBy":[],"sortDesc":[],"groupBy":[],"groupDesc":[],"mustSort":false,"multiSort":false},
        loading: false,
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
