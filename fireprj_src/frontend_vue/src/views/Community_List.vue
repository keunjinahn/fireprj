<template>
  <main-layout>
    <template v-slot>
      <div class="main-panel">
        <v-toolbar
            color="light-blue darken-4"
            dark
            flat
        >
          <v-toolbar-title>커뮤니티</v-toolbar-title>

          <v-spacer></v-spacer>

          <template v-slot:extension>
            <v-tabs
                v-model="selected_tab_item"
                align-with-title
                slider-size="6"
            >
              <v-tabs-slider color="yellow"></v-tabs-slider>

              <v-tab @change="change_tab_item(type_tab_items[0])">
                {{type_tab_items[0]}}
              </v-tab>
              <v-tab @change="change_tab_item(type_tab_items[1])">
                {{type_tab_items[1]}}
              </v-tab>
              <v-tab @change="change_tab_item(type_tab_items[2])">
                {{type_tab_items[2]}}
              </v-tab>

<!--              <v-tab-->
<!--                  v-for="item in type_tab_items"-->
<!--                  :key="item"-->
<!--                  @change="change_tab_item(item)"-->
<!--              >-->
<!--                {{ item }}-->
<!--              </v-tab>-->
            </v-tabs>
          </template>
        </v-toolbar>
        <v-tabs-items v-model="selected_tab_item">
          <v-tab-item
              v-for="(type_item,index) in type_tab_items"
              :key="type_item">
            <v-card flat>
              <br>
              <v-toolbar rounded dense class="elevation-1">
                <v-text-field outlined dense hide-details
                              placeholder="검색어를 입력하세요"
                              append-icon="mdi-magnify"
                              v-model="community.search_text"
                              @keydown.enter="getCommunity(type_item)"
                              class="m-right"
                />
                <v-btn depressed dark big
                       color="light-blue darken-2"
                       @click="getCommunity(type_item)">
                  <v-icon small>mdi-magnify</v-icon>
                  <div class="ml-1">조회</div>
                </v-btn>
                <v-btn v-show="$session.hasPermission([1]) || index ==1 " depressed dark big class="s-left"
                       color="light-blue darken-2"
                       @click="onMakeCommunityDialog()">
                  <v-icon small>mdi-plus</v-icon>
                  <div class="ml-1">작성</div>
                </v-btn>
              </v-toolbar>
              <v-data-table
                :headers="getHeaders(type_item)"
                :items="community.data"
                :loading="community.loading"
                :options.sync="community.options"
                :server-items-length="community.total"
                :items-per-page="10"
                :footer-props="{'items-per-page-options': [5, 10, 15,20,25,30,-1]}"
                class="elevation-1 mt-4 "
              >
                <template v-slot:item="row" v-if="index == 0">
                  <tr class="clickable-row" @click="onCommunityModifyHandler(row.item)">
                    <td>{{ row.item._index }}</td>
                    <td>{{ row.item.user_id }}</td>
                    <td>{{ row.item.user_name }}</td>
                    <td>{{ row.item.title }}</td>
                    <td v-show="$session.hasPermission([1])">{{ getOpenRange(row.item.open_range)}}</td>
                    <td>{{ row.item.view_cnt}}</td>
                    <td>{{ row.item.created_date | moment('YYYY-MM-DD HH:mm:ss') }}</td>
                    <td>{{ row.item.updated_date | moment('YYYY-MM-DD HH:mm:ss') }}</td>
                    <td @click.stop> <v-btn  :disabled="checkPermission(row)" outlined x-small rounded color="red" @click="delCommunity(row)">삭제</v-btn></td>
                  </tr>
                </template>
                <template v-slot:item="row" v-else-if="index == 1">
                  <tr class="clickable-row" @click="onCommunityModifyHandler(row.item)">
                    <td>{{ row.item._index }}</td>
                    <td>{{ row.item.user_id }}</td>
                    <td>{{ row.item.user_name }}</td>
                    <td>{{ row.item.title }}</td>
                    <td>{{ row.item.view_cnt}}</td>
                    <td>{{(row.item.open == 1)? '공개':'비공개'}}</td>
                    <td>{{ getAttachFileName(row.item.attatch_file_name)}}</td>
                    <td>{{ row.item.created_date | moment('YYYY-MM-DD HH:mm:ss') }}</td>
                    <td>{{ row.item.updated_date | moment('YYYY-MM-DD HH:mm:ss') }}</td>
                    <td v-if="row.item.response_id > 0" @click.stop style="cursor: pointer;color:blue;text-underline:#0d47a1"><span @click="onResponseDialog(row.item)">답글확인</span></td>
                    <td v-else @click.stop></td>
                    <td @click.stop> <v-btn :disabled="row.item.response_id > 0 || !$session.hasPermission([1])" x-small rounded color="primary" @click="responseCommunity(row.item)">답글쓰기</v-btn></td>
                    <td @click.stop> <v-btn :disabled="checkPermission(row)" outlined x-small rounded color="red" @click="delCommunity(row)">삭제</v-btn></td>
                  </tr>
                </template>
                <template v-slot:item="row" v-else>
                  <tr class="clickable-row" @click="onCommunityModifyHandler(row.item)">
                    <td>{{ row.item._index }}</td>
                    <td>{{ row.item.user_id }}</td>
                    <td>{{ row.item.user_name }}</td>
                    <td>{{ row.item.title }}</td>
                    <td v-show="$session.hasPermission([1])">{{ getOpenRange(row.item.open_range)}}</td>
                    <td>{{ row.item.view_cnt}}</td>
                    <td>{{ getAttachFileName(row.item.attatch_file_name)}}</td>
                    <td>{{ row.item.created_date | moment('YYYY-MM-DD HH:mm:ss') }}</td>
                    <td>{{ row.item.updated_date | moment('YYYY-MM-DD HH:mm:ss') }}</td>
                    <td @click.stop> <v-btn :disabled="checkPermission(row)" outlined x-small rounded color="red" @click="delCommunity(row)">삭제</v-btn></td>
                  </tr>
                </template>
              </v-data-table>
            </v-card>
          </v-tab-item>

        </v-tabs-items>
      </div>
      <v-dialog v-model="community.dialog.show" persistent max-width="600px" :key="community.dialog.id">
        <v-card :loading="loading" :disabled="loading">
          <v-card-title class="pt-2 pb-1 primary white--text">
            <span class="body-1">{{getCommunityTitle()}}</span>
          </v-card-title>
          <v-divider />
          <v-card-text>
            <v-container :key="community.dialog.id">
              <v-row>
                <v-col cols="12" sm="6">
                  <v-text-field outlined dense hide-details
                                label="글쓴이 아이디"
                                placeholder=""
                                disabled
                                v-model="community.dialog.user_id"
                  />
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field outlined dense hide-details
                                label="글쓴이 이름"
                                placeholder=""
                                disabled
                                v-model="community.dialog.user_name"
                  />
                </v-col>
                <v-col cols="12" sm="12">
                  <v-text-field outlined dense hide-details
                                label="제목"
                                placeholder=""
                                v-model="community.dialog.title"
                                :disabled="!community.dialog.canModify"
                  />
                </v-col>
                <v-col cols="12">
                  <v-textarea
                      outlined
                      name="input-7-4"
                      label="내용입력"
                      value=""
                      v-model="community.dialog.contents"
                      :disabled="!community.dialog.canModify"
                  ></v-textarea>
                </v-col>
                <v-col cols="4" v-show="community.dialog.community_type==2">
                  <v-select outlined dense hide-details
                            v-model="community.dialog.selected_open"
                            :items="community.dialog.open_list"
                            label="공개여부"
                            :disabled="!community.dialog.canModify"
                            item-text="name"
                            item-value="code"
                            @change="onChangeOpen(community.dialog.selected_open)"
                  />
                </v-col>
                <v-col cols="6" v-show="$session.hasPermission([1]) && (community.dialog.community_type ==1 || community.dialog.community_type ==3)">
                  <v-select outlined dense hide-details
                            v-model="community.dialog.selected_open_range"
                            :items="community.dialog.open_range_list"
                            label="공개범위"
                            item-text="name"
                            item-value="code"
                            @change="onChangeOpenRange(community.dialog.selected_open_range)"
                  />
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-text v-show="selected_tab_item != 0">
            <v-row>
              <v-col cols="12" sm="9">
                <v-file-input
                    truncate-length="50"
                    v-model="community.dialog.file_input"
                    color="deep-purple accent-4"
                    :placeholder="community.dialog.file_name"
                    :disabled="!community.dialog.canFileModify"
                ></v-file-input>
              </v-col>
              <v-col cols="12" sm="3">
                <v-btn
                    color="light-blue darken-2"
                    style="margin-top: 15px"
                    tile
                    dark
                    depressed
                    @click="attach_download(community.dialog.file_path)"
                >
                  파일다운로드
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions>
            <v-btn
                color="light-blue darken-2"
                class="flex-grow-1"
                text
                @click="onCommunityDialogClose()"
            >
              닫기
            </v-btn>
            <v-btn
                color="primary"
                class="flex-grow-1"
                tile
                :disabled="!community.dialog.canModify"
                depressed
                @click="submitHandler"
            >
              작성
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog v-model="community.dialog_response.show" persistent max-width="600px" :key="community.dialog_response.id">
        <v-card :loading="loading" :disabled="loading">
          <v-card-title class="pt-2 pb-1 primary white--text">
            <span class="body-1">Q&A답변</span>
          </v-card-title>
          <v-divider />
          <v-card-text>
            <v-container :key="community.dialog_response.id">
              <v-row>
                <v-col cols="12" sm="6">
                  <v-text-field outlined dense hide-details
                                label="글쓴이 아이디"
                                placeholder=""
                                disabled
                                v-model="community.dialog_response.user_id"
                  />
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field outlined dense hide-details
                                label="글쓴이 이름"
                                placeholder=""
                                disabled
                                v-model="community.dialog_response.user_name"
                  />
                </v-col>
                <v-col cols="12" sm="12">
                  <v-text-field outlined dense hide-details
                                label="제목"
                                placeholder=""
                                v-model="community.dialog_response.title"
                                :disabled="!community.dialog_response.canModify"
                  />
                </v-col>
                <v-col cols="12">
                  <v-textarea
                      outlined
                      name="input-7-4"
                      label="내용입력"
                      value=""
                      v-model="community.dialog_response.contents"
                      :disabled="!community.dialog_response.canModify"
                  ></v-textarea>
                </v-col>
                <v-col cols="12">
                  <v-textarea
                      outlined
                      name="input-7-4"
                      label="답변내용"
                      value=""
                      v-model="community.dialog_response.response_contents"
                      :disabled="!$session.hasPermission([1])"
                  ></v-textarea>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-text v-show="selected_tab_item != 0">
            <v-row>
              <v-col cols="12" sm="9">
                <v-file-input
                    truncate-length="50"
                    v-model="community.dialog_response.file_input"
                    color="deep-purple accent-4"
                    :placeholder="community.dialog_response.file_name"
                    :disabled="!community.dialog_response.canFileModify"
                ></v-file-input>
              </v-col>
              <v-col cols="12" sm="3">
                <v-btn
                    color="light-blue darken-2"
                    style="margin-top: 15px"
                    tile
                    dark
                    depressed
                    @click="attach_download(community.dialog_response.file_path)"
                >
                  파일다운로드
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions>
            <v-btn
                color="light-blue darken-2"
                class="flex-grow-1"
                text
                @click="onCommunityReponseDialogClose()"
            >
              닫기
            </v-btn>
            <v-btn
                color="primary"
                class="flex-grow-1"
                tile
                depressed
                @click="submitResponseHandler"
            >
              작성
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog v-model="community.dialog.del_show" max-width="500px">
        <v-card>
          <v-card-title>선택한 내용을 삭제하시겠습니까?</v-card-title>
          <v-card-actions>
            <v-btn tile depressed class="flex-grow-1" @click="deleteCommunity(community.dialog.del_item)">삭제</v-btn>
            <v-btn tile depressed class="flex-grow-1" @click="community.dialog.del_show = false">취소</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="community.dialog.deleted_show" max-width="500px">
        <v-card>
          <v-card-title>유저가 삭제되었습니다.</v-card-title>
          <v-card-actions>
            <v-btn tile depressed class="flex-grow-1" @click="community.dialog.deleted_show = false">확인</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="community.dialog.alert_show" max-width="500px">
        <v-card>
          <v-card-title>작성되었습니다.</v-card-title>
          <v-card-actions>
            <v-btn tile depressed class="flex-grow-1" @click="community.dialog.alert_show = false">확인</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </template>
  </main-layout>
</template>

<script>
import moment from "moment";
import XLSX from "xlsx";
import exportCSV from '@/plugins/exportCSV'
import axios from 'axios'
export default {
  props: {
    fstatus: { type: [Number, String], default: 0 }
  },
  methods: {
    async getCommunity(commnuity_type_value=null) {
      this.community.loading = true;
      const { page, itemsPerPage,sortBy, sortDesc } = this.community.options;
      let filters_and = [];
      let filters_or = [];
      let order_by = []
      if(commnuity_type_value == this.type_tab_items[0]) {
        filters_and.push({"name": "community_type", "op": "eq", "val": 1});
        this.selected_tab_item = 0
      }else if(commnuity_type_value == this.type_tab_items[1]) {
        filters_and.push({"name": "community_type", "op": "eq", "val": 2});
        if(this.$session.hasPermission([1]) == false){
          //관리자가 아닌경우는 자기가 쓴내용또는 공개인경우만 조회
          filters_or.push({"name": "user_id", "op": "eq", "val": this.$session.getUserId()});
          filters_or.push({"name": "open", "op": "eq", "val": 1});
        }
        this.selected_tab_item = 1
      }else if(commnuity_type_value == this.type_tab_items[2]) {
        filters_and.push({"name": "community_type", "op": "eq", "val": 3});
        this.selected_tab_item = 2
      }

      if(this.$session.hasPermission([2,3,4])){
        filters_and.push({"name": "open_range", "op": "in", "val": [0,1]});
      }else if(this.$session.hasPermission([5,6])){
        filters_and.push({"name": "open_range", "op": "in", "val": [0,2]});
      }

      if(this.community.search_text != ''){
        filters_or.push({"name": "user_id", "op": "like", "val": "%"+this.community.search_text+"%"});
        filters_or.push({"name": "user_name", "op": "like", "val": "%"+this.community.search_text+"%"});
        filters_or.push({"name": "title", "op": "like", "val": "%"+this.community.search_text+"%"});
        filters_or.push({"name": "contents", "op": "like", "val": "%"+this.community.search_text+"%"});
      }
      if (sortBy.length) {
        for (let i=0; i<sortBy.length; i++) {
          order_by.push({field: sortBy[i], direction: sortDesc[i] ? 'desc' : 'asc'})
        }
      }
      else order_by.push({field: 'id', direction: 'desc'})

      let q = {
        filters: [{or:filters_or},{and:filters_and}],
        order_by
      }
      let params = {q: JSON.stringify(q), results_per_page: itemsPerPage, page: page}

      try {
        let { data } = await this.$http.get("community", { params });
        this.community.total = data.num_results;
        this.community.data = data.objects.map((v, i) => {
          v._index = i + (page - 1) * itemsPerPage + 1;
          return v;
        });
      } catch (err) {
        console.error(err);
      } finally {
        this.community.loading = false;
      }
    },

    change_tab_item(item){
      this.getCommunity(item);
    },
    onMakeCommunityDialog(){
      this.community.dialog.id = -1
      this.community.dialog.contents = ''
      this.community.dialog.title = ''
      this.community.dialog.user_id = this.$session.getUserId()
      this.community.dialog.user_name = this.$session.getUserName()
      this.community.dialog.file_path = ''
      this.community.dialog.file_name = ''
      this.community.dialog.file_input = ''
      this.community.dialog.show = true
      this.community.dialog.canModify = true
      this.community.dialog.canFileModify = true
      this.community.dialog.community_type = this.selected_tab_item + 1
      this.community.dialog.current_job = "MAKE"
      this.community.dialog.selected_open = this.community.dialog.open_list[0]
      this.community.dialog.selected_open_range = this.community.dialog.open_range_list[0]
    },
    onCommunityDialogClose() {
      this.getCommunity(this.type_tab_items[this.selected_tab_item])
      this.community.dialog.show = false
    },
    onCommunityReponseDialogClose() {
      this.getCommunity(this.type_tab_items[this.selected_tab_item])
      this.community.dialog_response.show = false
    },
    async submitHandler(){
      let msg = [];

      if (this.community.dialog.title.length == 0){
        this.$session.$emit('modal-alert','제목을 입력하여 주세요!')
        return
      }
      if (this.community.dialog.contents.length == 0){
        this.$session.$emit('modal-alert', '내용을 입력하여 주세요!')
        return
      }
      let params = {}
      params.title = this.community.dialog.title;
      params.contents = this.community.dialog.contents;
      params.user_id = this.$session.getUserId();
      params.user_name = this.$session.getUserName();
      let today = moment().format('YYYY-MM-DD HH:mm:ss')
      params.updated_date = today
      params.open = this.community.dialog.selected_open.code
      if(this.selected_tab_item == 1 && this.community.dialog.current_job == "MAKE") {
        params.community_type = this.selected_tab_item + 1
      }
      else
        params.community_type =this.selected_tab_item + 1

      if(this.community.dialog.file_input != '' && this.community.dialog.file_input != null) {
        const fd = new FormData()
        fd.append('file', this.community.dialog.file_input)
        let {data} = await this.$http.post('upload_file', fd)
        if (!data || !data.result || !data.filename)
          return alert("이미지 저장실패!!")
        params.attatch_file_path = data.filename
        params.attatch_file_name = data.src_filename
      }

      if(this.$session.hasPermission([1]) && this.selected_tab_item != 1){
        params.open_range = this.community.dialog.selected_open_range_code
      }

      if(this.community.dialog.current_job == "MAKE") {
        params.created_date = today
        await this.$http.post(`community`, params)
      }
      else{
        await this.$http.patch(`community/${this.community.dialog.id}`, params)
      }
      this.getCommunity(this.type_tab_items[this.selected_tab_item])
      this.community.dialog.show = false
      this.community.dialog.alert_show = true
    },
    async submitResponseHandler(){
      let params = {}
      params.title = this.community.dialog_response.title;
      params.contents = this.community.dialog_response.contents;
      params.user_id = this.community.dialog_response.user_id;
      params.user_name = this.community.dialog_response.user_name;
      params.contents = this.community.dialog_response.contents;
      params.response_contents = this.community.dialog_response.response_contents;
      let today = moment().format('YYYY-MM-DD HH:mm:ss')
      params.updated_date = today
      params.community_type = 4
      if(this.community.dialog_response.file_input != '' && this.community.dialog_response.file_input != null) {
        const fd = new FormData()
        fd.append('file', this.community.dialog_response.file_input)
        let {data} = await this.$http.post('upload_file', fd)
        if (!data || !data.result || !data.filename)
          return alert("이미지 저장실패!!")
        params.attatch_file_path = data.filename
        params.attatch_file_name = data.src_filename
      }
      params.created_date = today
      params.parent_id = this.community.dialog_response.parent_id

      if(this.community.dialog_response.current_job == "RESPONSE_MAKE") {
        params.created_date = today
        params.parent_id = this.community.dialog_response.parent_id
        await this.$http.post(`community`, params)
      }
      else{
        if(this.$session.hasPermission([1]))
          await this.$http.patch(`community/${this.community.dialog_response.id}`, params)
      }
      this.getCommunity(this.type_tab_items[this.selected_tab_item])
      this.community.dialog_response.show = false
      if(this.$session.hasPermission([1]))
        this.community.dialog.alert_show = true
    },
    getAttachFileName(attach_file){
      if(attach_file != undefined && attach_file.length > 0){
        return "유"
      }
      return '무'
    },
    async onCommunityModifyHandler(item){
      this.community.dialog.show = true
      this.community.dialog.id = item.id
      this.community.dialog.title = item.title
      this.community.dialog.user_id = item.user_id
      this.community.dialog.user_name = item.user_name
      this.community.dialog.contents = item.contents
      this.community.dialog.file_path = item.attatch_file_path
      this.community.dialog.file_name = item.attatch_file_name
      this.community.dialog.canModifile_namefy = false
      this.community.dialog.community_type = item.community_type
      this.community.dialog.selected_open = this.community.dialog.open_list[item.open]
      this.community.dialog.canModify = false
      this.community.dialog.canFileModify = false
      if(this.$session.getUserId() == item.user_id) {
        this.community.dialog.canModify = true
        this.community.dialog.canFileModify = true
      }

      if(this.$session.hasPermission([1]) && this.selected_tab_item != 2){
        this.community.dialog.selected_open_range = this.community.dialog.open_range_list[item.open_range]
      }
      this.community.dialog.current_job = "MODIFY"
      let params = {}
      params.view_cnt = item.view_cnt + 1;
      await this.$http.patch(`community/${item.id}`, params)
   },

   async onResponseDialog(item){
     let {data} = await this.$http.get(`community/${item.response_id}`)
     this.community.dialog_response.show = true
     this.community.dialog_response.id = item.response_id
     this.community.dialog_response.title = data.title
     this.community.dialog_response.user_id = data.user_id
     this.community.dialog_response.user_name = data.user_name
     this.community.dialog_response.contents = data.contents
     this.community.dialog_response.response_contents = data.response_contents
     this.community.dialog_response.file_path = data.attatch_file_path
     this.community.dialog_response.file_name = data.attatch_file_name
     this.community.dialog_response.community_type = data.community_type
     this.community.dialog_response.canModify = false
     this.community.dialog_response.canFileModify = false
     this.community.dialog_response.current_job = "RESPONSE_MODIFY"
    },
    delCommunity(row) {
      if(this.checkPermission(row)){
        this.$session.$emit('modal-alert', '작성자만 삭제할 수 있습니다.')
        return
      }
      this.community.dialog.del_show = true
      this.community.dialog.del_item = row.item
    },
    responseCommunity(item){
      if(this.$session.hasPermission([1]) == false){
        this.$session.$emit('modal-alert', '권한이 없습니다')
        return
      }
      this.community.dialog_response.show = true
      this.community.dialog_response.user_id = item.user_id
      this.community.dialog_response.user_name = item.user_name
      this.community.dialog_response.parent_id = item.id
      this.community.dialog_response.title = item.title
      this.community.dialog_response.contents = item.contents
      this.community.dialog_response.response_contents = ''
      this.community.dialog_response.file_path = ""
      this.community.dialog_response.file_name = ""
      this.community.dialog_response.canModify = true
      this.community.dialog_response.canFileModify = true
      this.community.dialog_response.current_job = "RESPONSE_MAKE"
      this.community.dialog_response.community_type = 4
      this.community.dialog_response.selected_open = this.community.dialog_response.open_list[0]
    },
    async deleteCommunity(item) {
      this.community.dialog.del_show = false
      await this.$http.delete(`community/${item.id}`)
      this.$session.$emit('modal-alert', '삭제되었습니다')
      this.getCommunity(this.type_tab_items[this.selected_tab_item])
    },
    async attach_download(attach_filename) {
      var url = '/api/monitor/v1/upload_file/' + attach_filename
      axios({
        method: 'get',
        url: url,
        // url: 'search_result.xlsx',
        responseType: 'blob'
      })
      .then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data], {
          type: 'application/vnd.ms-excel'
        }))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', attach_filename) // or any other extension
        document.body.appendChild(link)
        link.click()
      })
      .catch(() => console.log('error occured'))
    },
    getHeaders(type_item){
      if(type_item == this.type_tab_items[0]){
        if(!this.$session.hasPermission([1])){
          return this.community.headers_notice.filter(function (item) {
            return item.text != '공개범위';
          });
        }
        return this.community.headers_notice
      }else if(type_item == this.type_tab_items[1]){
        return this.community.headers_qna
      }else if(type_item == this.type_tab_items[2]){
        if(!this.$session.hasPermission([1])){
          return this.community.headers_datas.filter(function (item) {
            return item.text != '공개범위';
          });
        }
        return this.community.headers_datas
      }
    },
    getCommunityTitle(){
      return this.type_tab_items[this.selected_tab_item]
    },
    check_file(filepath){
      if(filepath != undefined && filepath.length > 0)
        return false
      return true
    },
    onChangeOpen(open_type){
      this.community.dialog.selected_open = this.community.dialog.open_list[open_type]
    },
    onChangeOpenRange(open_range_code){
      this.community.dialog.selected_open_range_code = open_range_code
    },
    getOpenRange(open_range_code){
      return this.community.dialog.open_range_list.find(v =>v.code == open_range_code).name
    },
    checkPermission(row){
      if(this.$session.hasPermission([1])
          || row.item.user_id == this.$session.getUserId()){
        return false
      }
      return true
    }
  },
  mounted() {
    this.selected_tab_item = this.fstatus
    if(!this.$session.hasPermission([1]))
      this.selected_tab_item = 1
    this.getCommunity(this.type_tab_items[this.selected_tab_item])
  },
  watch: {
    'users.options': {
      handler() {
        this.getCommunity(this.type_tab_items[this.selected_tab_item])
      },
      deep: true
    },
    fstatus () {
      this.selected_tab_item = this.fstatus
    }
  },
  data() {
    return {
      community: {
        headers_notice: [
          {text: 'No.', value: 'id', sortable: false, align: 'center', width: 40},
          {text: "글쓴이 아이디", value: "user_id", align: 'center',sortable: false},
          {text: "글쓴이 이름", value: "user_name",  align: 'center',sortable: false},
          {text: "제목", value: "title",  align: 'center',sortable: false},
          {text: "공개범위", value: "open_range",  align: 'center',sortable: false},
          {text: "조회수", value: "view_cnt",  align: 'center',sortable: false},
          {text: "작성일", value: "created_date",  align: 'center',sortable: false},
          {text: "수정일", value: "updated_date",  align: 'center',sortable: false},
          {text: "삭제", value: "",  align: 'center',sortable: false, width: 40}
        ],
        headers_qna: [
          {text: 'No.', value: 'id',  align: 'center',sortable: false, width: 40},
          {text: "글쓴이 아이디", value: "user_id",  align: 'center',sortable: false},
          {text: "글쓴이 이름", value: "user_name",  align: 'center',sortable: false},
          {text: "제목", value: "title",  align: 'center',sortable: false},
          {text: "조회수", value: "view_cnt",  align: 'center',sortable: false,},
          {text: "공개유무", value: "open",  align: 'center',sortable: false,},
          {text: "첨부파일유무", value: "attatch_file_name",  align: 'center',sortable: false},
          {text: "작성일", value: "created_date",  align: 'center',sortable: false},
          {text: "수정일", value: "updated_date",  align: 'center',sortable: false},
          {text: "답글유무", value: "parent_id",  align: 'center',sortable: false},
          {text: "답글", value: "",  align: 'center',sortable: false, width: 100},
          {text: "삭제", value: "",  align: 'center',sortable: false, width: 40}
        ],
        headers_datas: [
          {text: 'No.', value: 'id',  align: 'center',sortable: false, width: 40},
          {text: "글쓴이 아이디", value: "user_id",  align: 'center',sortable: false},
          {text: "글쓴이 이름", value: "user_name",  align: 'center',sortable: false},
          {text: "제목", value: "title",  align: 'center',sortable: false},
          {text: "공개범위", value: "open_range",  align: 'center',sortable: false},
          {text: "조회수", value: "view_cnt",  align: 'center',sortable: false},
          {text: "첨부파일유무", value: "attatch_file_name",  align: 'center',sortable: false},
          {text: "작성일", value: "created_date",  align: 'center',sortable: false},
          {text: "수정일", value: "updated_date",  align: 'center',sortable: false},
          {text: "삭제", value: "",  align: 'center',sortable: false, width: 40}
        ],
        search_text: '',
        data: [],
        options: {"page":1,"itemsPerPage":10,"sortBy":[],"sortDesc":[],"groupBy":[],"groupDesc":[],"mustSort":false,"multiSort":false},
        loading: false,
        dialog:{
          show:false,
          id:'',
          title:'',
          user_id:'',
          user_name:'',
          contents:'',
          file_input:null,
          file_path:null,
          file_name: '파일을 선택해 주세요',
          del_show:false,
          deleted_show:false,
          alert_show:false,
          del_item:null,
          canModify:false,
          canFileModify:false,
          parent_id:-1,
          community_type:0,
          selected_open:null,
          open_list:[
            {name:"비공개",code:0},
            {name:"공개",code:1},
          ],
          selected_open_range:null,
          selected_open_range_code:0,
          open_range_list:[
            {name:'전체',code:0},
            {name:'한국교육시설안전원',code:1},
            {name:'회원 및 학교',code:2},
          ],
          current_job:''
        },
        dialog_response:{
          show:false,
          id:'',
          title:'',
          user_id:'',
          user_name:'',
          contents:'',
          response_contents:'',
          file_input:null,
          file_path:null,
          file_name: '파일을 선택해 주세요',
          del_show:false,
          deleted_show:false,
          del_item:null,
          canModify:false,
          canFileModify:false,
          parent_id:-1,
          community_type:0,
          current_job:''
        }
      },
      popuptwo:{
        show: false,
        del_show: false,
        error: [],
        delItem:null
      },
      member_type:[
          "관리자",
          "기관사용자",
          "일반사용자"
     ],
     loading: false,
     selected_tab_item: null,
     type_tab_items: ['공지','Q & A','자료실'],

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
.datetime-wrap {
  position: relative;
}
.func-wrap {
  position: absolute;
  top: 10px;
  right: -200px;
  width: 200px;
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
.search-action {
  flex: 0 0 120px;
  margin-left: 10px;
  display: flex;
  align-items: center;
}
.m-right{margin-right: 20px;}
.s-left{
  text-align: left;
  margin-left: 10px;
}
td {
  text-align: center;
}
.swal-wide{
  font-size: 12px !important;

}
</style>
