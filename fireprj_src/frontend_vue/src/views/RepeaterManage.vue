<template>
  <main-layout>
    <template v-slot>
      <div class="main-panel">
        <v-toolbar color="light-blue darken-4" dark flat>
          <v-toolbar-title>중계기 관리</v-toolbar-title>
        </v-toolbar>

        <v-card flat>
          <v-toolbar rounded dense class="elevation-1">
            <v-col cols="5">
              <v-text-field outlined dense hide-details
                            placeholder="중계기 검색"
                            append-icon="mdi-magnify"
                            v-model="repeater.search"
                            @keydown.enter="getRepeater()"
                            class="m-right"
              />
            </v-col>
            <v-col cols="1">
              <v-btn depressed dark big
                      color="light-blue darken-2"
                      @click="getRepeater()">
                
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
          :headers="repeater.headers"
          :items="repeater.data"
          :loading="repeater.loading"
          :options.sync="repeater.options"
          :server-items-length="repeater.total"
          :items-per-page="5"
          :search="repeater.search"
          :footer-props="{'items-per-page-options': [5, 10, 15,20,25,30,-1]}"
          @click:row="popupRepeaterData"
          class="elevation-1 mt-4 clickable-row"
          @input="onSelectedChnage">
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
              <span class="body-1">중계기 추가</span>
            </v-card-title>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="중계기 식별자"
                                  placeholder="중계기 식별자"
                                  v-model="addPopup.form.repeater_idx"
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
                                  label="수신기 번호"
                                  placeholder="수신기 번호"
                                  v-model="addPopup.form.receiver_id"
                    />
                  </v-col>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="계통 번호"
                                  placeholder="계통 번호"
                                  v-model="addPopup.form.system_id"
                    />
                  </v-col>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="중계기 번호"
                                  placeholder="중계기 번호"
                                  v-model="addPopup.form.repeater_id"
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
                      @click="addRepeater()">
                추가  
              </v-btn>
            </v-card-action>
          </v-card>
        </v-dialog>

        <v-dialog v-model="infoPopup.show" persistent max-width="600px">
          <v-card>
            <v-card-title class="pt-2 pb-1 primary white--text">
              <span class="body-1">중계기 정보</span>
            </v-card-title>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="중계기 식별자"
                                  placeholder="중계기 식별자"
                                  v-model="infoPopup.form.repeater_idx"
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
                                  label="수신기 번호"
                                  placeholder="수신기 번호"
                                  v-model="infoPopup.form.receiver_id"
                    />
                  </v-col>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="계통 번호"
                                  placeholder="계통 번호"
                                  v-model="infoPopup.form.system_id"
                    />
                  </v-col>
                  <v-col cols="6" sm="6">
                    <v-text-field outlined dense hide-details
                                  label="중계기 번호"
                                  placeholder="중계기 번호"
                                  v-model="infoPopup.form.repeater_id"
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
                      @click="modifyRepeaterData()">
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
                      @click="deleteRepeater()">
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
    async getRepeater() {

      let {data} = await this.$http.get("repeater")
      this.repeater.data = data.objects;
    },

    // async getRepeater () {
    //   this.users.loading = true;
    //   const { page, itemsPerPage ,sortBy, sortDesc  } = this.repeater.options;
    //   let order_by = []
    //   let filters_or = [];
    //   let filters_and = [];
    //   var api_name = 'repeater'

    //   // 정렬 선택이 있을 경우
    //   if (sortBy.length) {
    //     for (let i=0; i<sortBy.length; i++) {
    //       order_by.push({field: sortBy[i], direction: sortDesc[i] ? 'desc' : 'asc'})
    //     }
    //   }
    //   // 정렬 선택이 없을 경우 id를 기본으로 정렬
    //   else order_by.push({field: 'id', direction: 'desc'})
    //   filters_or.push({"name": "repeater_idx", "op": "like", "val": "%"+this.repeater.search+"%"});

    //   if(this.repeater.search.length > 0) {
    //     filters_or.push({"name": "fk_customer_idx", "op": "like", "val": "%" + this.repeater.search + "%"});
    //   }

    //   try {
    //     let q = JSON.stringify({
    //       filters: [{or:filters_or},{and:filters_and}],
    //       order_by
    //     })
    //     let params = {
    //       q: q,
    //       results_per_page: itemsPerPage,
    //       page: page,
    //     }

    //     let { data } = await this.$http.get(api_name, { params })
    //     this.repeater.total = data.num_results;
    //     this.repeater.data = data.objects.map((v, i) => {
    //       v._index = i + (page - 1) * itemsPerPage + 1;
    //       return v; });
    //   } 
    //   catch (err) {
    //     console.error(err);
    //   } 
    //   finally {
    //     this.repeater.loading = false;
    //   }
    // },

    // onSelectedChnage(){
    //   this.repeater.data.forEach(v=>v.enable=false)
    //   this.repeater.selected.forEach(v=>v.enable=true)
    // },
    async addRepeater() {
      let param = this.addPopup.form;
      await this.$http.post("repeater", param)
      this.getRepeater()
      this.addPopup.show = false;
    },
    popupRepeaterData(e, {item}) {
      this.infoPopup.form = item;
      this.infoPopup.show = true;
    },
    async modifyRepeaterData() {
      let param = this.infoPopup.form;
      delete param.customer;
      await this.$http.patch(`repeater/${param.id}`, param)
      this.getRepeater()
      this.infoPopup.show = false;
    },
    openDeletePopup(item) {
      this.deletePopup.delTarget = item.id;
      this.deletePopup.show = true;
    },
    async deleteRepeater() {
      let param = this.deletePopup.delTarget;
      await this.$http.delete(`repeater/${param}`)
      this.getRepeater()
      this.deletePopup.show = false;
    }
  },
  mounted() {
    this.getRepeater()
  },
  watch: {
    "repeater.options": {
      handler() {
      },
      deep: true,
    },
  },
  data() {
    return {
      repeater: {
        selected: [],
        headers: [
          {text: '중계기 식별자', value: 'repeater_idx', sortable: false,align: 'center', width: 80},
          {text: "고객식별자", value: "fk_customer_idx",align: 'center', sortable: false, width: 60},
          {text: "수신기 번호", value: "receiver_id",align: 'center', sortable: false, width: 40},
          {text: "계통 번호", value: "system_id",align: 'center', sortable: false, width: 20},
          {text: "중계기 번호", value: "repeater_id",align: 'center', sortable: false, width: 20},
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
          repeater_idx: '',
          fk_customer_idx: '',
          receiver_id: '',
          system_id: '',
          repeater_id: '',
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
