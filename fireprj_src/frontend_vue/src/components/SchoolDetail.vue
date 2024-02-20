<template>
  <div>
    <v-card :loading="loading" :disabled="loading">
      <v-card-text>
<!--      <v-btn elevation="1" color="secondary" small class="school-save" @click="saveDamagePast()">-->
<!--        <v-icon>mdi-cloud-upload</v-icon><span>서버 저장</span>-->
<!--      </v-btn>-->
        <v-btn elevation="1" color="secondary" small class="report-download" @click="saveToPDF()">
          <v-icon>mdi-cloud-download</v-icon><span>보고서 다운로드</span>
        </v-btn>
      <abl-document class="abl-page"  :key="refresh_id" ref="report">
        <div class="abl-doc-title">
          <div class="title-text">{{getCheckSchoolName()}} {{(school.sub2_sdate != '')? school.sub2_sdate.substring(0,4) : ''}}년도 세부 피해 내역 보고서</div>
        </div>

        <div class="abl-doc-body">
          <table class="abl-table-empty">
            <colgroup>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
            </colgroup>
            <tr>
              <th class="s-t-blank" colspan="2"><div class="d-flex"><div>1.</div><div class="t1">학 교 명</div><div class="pr-3">:</div></div></th>
              <td colspan="4">{{getCheckSchoolName()}}({{school.disaster_num}})</td>
              <th class="s-t-blank" colspan="2"><div class="d-flex"><div>2.</div><div class="t1">소 재 지</div><div class="pr-3">:</div></div></th>
              <td colspan="4">{{getCheckAddress()}}</td>
            </tr>
            <tr>
              <th class="s-t-blank" colspan="2"><div class="d-flex"><div>3.</div><div class="t1">설 립 구 분</div><div class="pr-3">:</div></div></th>
              <td colspan="4">{{school.establish_gubun_name}}</td>
              <th class="s-t-blank" colspan="2"><div class="d-flex"><div>4.</div><div class="t1">기 관 종 류</div><div class="pr-3">:</div></div></th>
              <td colspan="4">{{school.organ_gubun2_name}}</td>
            </tr>
<!--            <tr>-->
<!--              <th class="s-t-blank" colspan="1"><div class="d-flex"><div>5.</div><div class="t1">재 해 종 별</div><div class="pr-3">:</div></div></th>-->
<!--              <td colspan="5">{{school.sub2_disaster_cause}}</td>-->
<!--            </tr>-->
          </table>
          <br>
          <span class="abl-table-subtitle">5. 사고발생정보</span>
          <table class="abl-table-ts">
            <colgroup>
              <col style="width:20%"/>
              <col style="width:30%"/>
              <col style="width:20%"/>
              <col style="width:30%"/>
            </colgroup>
            <tr>
              <th colspan="1">발생일시</th>
              <td colspan="1" class="image-default-h"><span>{{school.sub2_accept_date1}}</span></td>
              <th colspan="1">재해종별 피해원인</th>
              <td colspan="1"><span>{{school.sub2_disaster_naming}}</span></td>
            </tr>
            <tr>
              <th colspan="1">피해경위</th>
              <td colspan="3" class="image-default-h"><span>{{school.sub2_damage_detail}}</span></td>
            </tr>
<!--            <tr>-->
<!--              -->
<!--              -->
<!--              <td colspan="8"><span>{{school.sub2_damage_detail}}</span></td>-->
<!--            </tr>-->
          </table>
          <br>
          <div>
            <span class="abl-table-subtitle">6. 피해내용</span>
          </div>
          <div>
            <span class="abl-table-subtitle">1) 건물 피해 현황</span>
          </div>
          <table class="abl-table-ts">
            <colgroup>
            </colgroup>
            <tr>
              <th colspan="1">건물명</th>
              <th colspan="1">피해구분</th>
              <th colspan="1">구조부 피해</th>
              <th colspan="1">세부 피해부분</th>
              <th colspan="1">주요피해공정</th>
              <th colspan="1">피해유형</th>
              <th colspan="1">피해면적</th>
              <th colspan="1">지급액</th>
            </tr>
            <tr v-for="(item,index) in s3_data_json.s3_1" :key="index">
              <td colspan="1" class="image-default-h"><span>{{item.s3_data1_1}}</span></td>
              <td colspan="1"><span>{{item.s3_data2_1}}</span></td>
              <td colspan="1"><span>{{item.s3_data13}}</span></td>
              <td colspan="1"><span>{{item.s3_data15}}</span></td>
              <td colspan="1"><span>{{item.s3_data16}}</span></td>
              <td colspan="1"><span>{{item.s3_data17}}</span></td>
              <td colspan="1"><span>{{check_area(item.s3_data21)}}</span></td>
              <td colspan="1"><span>{{getJsonGroup12(index,'final_total') | makeComma}}</span></td>
            </tr>
          </table>
          <span class="abl-table-subtitle">2) 기본담보 피해 현황</span>
          <table class="abl-table-ts">
            <colgroup>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
              <col style="width:8.33%"/>
            </colgroup>
            <tr>
              <th colspan="3">기본교구</th>
              <th colspan="3">기본설비</th>
              <th colspan="3">기본부속물</th>
              <th colspan="1">지급액</th>
            </tr>
            <tr>
              <td colspan="1" class="image-default-h td-bold">명칭</td>
<!--              <td colspan="2"><span>{{getS3_2Group('s3_data1_2')s3_data_json.s3_2_group check_null(item.s3_data1_2)}}</span></td>-->
              <td colspan="2"><span>{{getJsonValue('s3_2_group','s3_data1_2')}}</span></td>
              <td colspan="1" class="td-bold">명칭</td>
              <td colspan="2"><span>{{getJsonValue('s3_2_group','s3_data1_3')}}</span></td>
              <td colspan="1" class="td-bold">명칭</td>
              <td colspan="2"><span>{{getJsonValue('s3_2_group','s3_data1_4')}}</span></td>
              <td colspan="1"><span>{{check_total(school.sub6_gubun234)  | makeComma }}</span></td>
<!--              <td colspan="1"><span>{{getJsonGroupsTotalValue('s3_2_group','s3_total_3','s3_total_4') | makeComma}}</span></td>-->
            </tr>
          </table>

          <span class="abl-table-subtitle">3) 부속물 및 물품 피해 현황</span>
          <table class="abl-table-ts">
            <colgroup>
              <col style="width:8.3%"/>
              <col style="width:8.3%"/>
              <col style="width:8.3%"/>
              <col style="width:8.3%"/>
              <col style="width:8.3%"/>
              <col style="width:8.3%"/>
              <col style="width:8.3%"/>
              <col style="width:8.3%"/>
              <col style="width:8.3%"/>
              <col style="width:8.3%"/>
              <col style="width:8.3%"/>
              <col style="width:8.3%"/>
            </colgroup>
            <tr>
              <th colspan="6">부속물</th>
              <th colspan="6">물품</th>
            </tr>
            <tr>
              <td colspan="1" class="image-default-h td-bold">부속물명</td>
              <td colspan="3"><span>{{getJsonValue('s3_5_group','s3_data1_7')}}</span></td>
              <td colspan="1" class="td-bold">지급액</td>
<!--              <td colspan="1"><span>{{getJsonGroupTotalValue('s3_5_group','s3_total_7') | makeComma}}</span></td>-->
              <td colspan="1"><span>{{check_total(school.sub6_gubun7)  | makeComma }}</span></td>
              <td colspan="1" class="td-bold">물품명</td>
              <td colspan="3"><span>{{getJsonValue('s3_5_group','s3_data1_5')}}</span></td>
              <td colspan="1" class="td-bold">지급액</td>
<!--              <td colspan="1"><span>{{getJsonGroupTotalValue('s3_5_group','s3_total_5') | makeComma}}</span></td>-->
              <td colspan="1"><span>{{check_total(school.sub6_gubun5)  | makeComma }}</span></td>
            </tr>
          </table>

          <span class="abl-table-subtitle">4) 배상책임 발생 현황</span>
          <table class="abl-table-ts">
            <colgroup>
              <col style="width:14.2%"/>
              <col style="width:14.2%"/>
              <col style="width:14.2%"/>
              <col style="width:14.2%"/>
              <col style="width:14.2%"/>
              <col style="width:14.2%"/>
              <col style="width:14.2%"/>
            </colgroup>
            <tr>
              <th colspan="1">피해구분</th>
              <th colspan="1">피해유형</th>
              <th colspan="1">신분</th>
              <th colspan="3">피해내용</th>
              <th colspan="1">지급액</th>
            </tr>
            <tr v-for="(item,index) in s3_data_json.s3_9_10" :key="index">
              <td colspan="1" class="image-default-h"><span>{{check_9_10(item)}}</span></td>
              <td colspan="1"><span>{{check_9_10_1(item)}}</span></td>
              <td colspan="1"><span>{{check_9_10_2(item)}}</span></td>
              <td colspan="3"><span>{{check_9_10_4(item)}}</span></td>
              <td colspan="1" v-show="index == 0" :rowspan="8"><span>{{check_total(school.sub6_gubun910)  | makeComma }}</span></td>
<!--              <td colspan="1" :rowspan="(index == 0)? s3_data_json.s3_9_10.length:1"><span>{{check_9_10_4(item)}}</span></td>-->
            </tr>
          </table>
          <br>
          <span class="abl-table-subtitle">5. 재난복구지원비</span>
          <table class="abl-table-ts">
            <colgroup>
              <col style="width:16.6%"/>
              <col style="width:16.6%"/>
              <col style="width:16.6%"/>
              <col style="width:16.6%"/>
              <col style="width:16.6%"/>
              <col style="width:16.6%"/>

            </colgroup>
            <tr>
              <th colspan="1">지급항목</th>
              <td colspan="3" class="image-default-h"><span>{{getJsonGroupNames(s3_data_json.s3_8[0])}}</span></td>
              <th colspan="1">지급액</th>
              <td colspan="1"><span>{{getJsonGroupTotal(s3_data_json.s3_8[0]) | makeComma}}</span></td>
            </tr>
          </table>
          <br>
          <span class="abl-table-subtitle">6. 재난현장 사진</span>
          <v-btn v-show="check_permission()"  height="20" elevation="1" color="secondary" small class="school-file-upload" @click="$refs.fileinput.click()">
            <v-icon>mdi-file-upload-outline</v-icon><span>이미지 추가</span>
          </v-btn>
          <table class="abl-table">
            <colgroup>
              <col style="width:50%"/>
            </colgroup>
            <tr>
              <th class="s-h"> <v-btn v-show="check_permission()" style="float:right" x-small rounded right class="ml-2" @click="deleteDialogShow(school.image_file_path1,'1')">x</v-btn></th>
              <th class="s-h"> <v-btn v-show="check_permission()" style="float:right" x-small rounded right class="ml-2" @click="deleteDialogShow(school.image_file_path2,'2')">x</v-btn></th>
            </tr>
            <tr >
              <td colspan="1" v-on:dblclick="onImageDownload(school.image_file_path1)"><abl-textarea :disabled="!check_permission()" class="image-left-m" @callBackImage="emitCallbackImage" v-model="school.image_file_path1" width="320px" height="200px" /></td>
              <td colspan="1" v-on:dblclick="onImageDownload(school.image_file_path2)"><abl-textarea :disabled="!check_permission()" class="image-left-m" @callBackImage="emitCallbackImage" v-model="school.image_file_path2"  width="320px" height="200px" /></td>
            </tr>
            <tr>
              <th class="s-h"> <v-btn v-show="check_permission()" style="float:right" x-small rounded right class="ml-2" @click="deleteDialogShow(school.image_file_path3,'3')">x</v-btn></th>
              <th class="s-h"> <v-btn v-show="check_permission()" style="float:right" x-small rounded right class="ml-2" @click="deleteDialogShow(school.image_file_path4,'4')">x</v-btn></th>
            </tr>
            <tr>
              <td colspan="1" v-on:dblclick="onImageDownload(school.image_file_path3)"><abl-textarea :disabled="!check_permission()" class="image-left-m" @callBackImage="emitCallbackImage" v-model="school.image_file_path3"  width="320px" height="200px" /></td>
              <td colspan="1" v-on:dblclick="onImageDownload(school.image_file_path4)"><abl-textarea :disabled="!check_permission()" class="image-left-m" @callBackImage="emitCallbackImage" v-model="school.image_file_path4"  width="320px" height="200px" /></td>
            </tr>
            <tr>
              <th class="s-h"> <v-btn v-show="check_permission()" style="float:right" x-small rounded right class="ml-2" @click="deleteDialogShow(school.image_file_path5,'5')">x</v-btn></th>
              <th class="s-h"> <v-btn v-show="check_permission()" style="float:right" x-small rounded right class="ml-2" @click="deleteDialogShow(school.image_file_path6,'6')">x</v-btn></th>
            </tr>
            <tr>
              <td colspan="1" v-on:dblclick="onImageDownload(school.image_file_path5)"><abl-textarea :disabled="!check_permission()" class="image-left-m" @callBackImage="emitCallbackImage" v-model="school.image_file_path5"  width="320px" height="200px" /></td>
              <td colspan="1" v-on:dblclick="onImageDownload(school.image_file_path6)"><abl-textarea :disabled="!check_permission()" class="image-left-m" @callBackImage="emitCallbackImage" v-model="school.image_file_path6"  width="320px" height="200px" /></td>
            </tr>
<!--            <tr>-->
<!--              <td colspan="1">-->
<!--                &lt;!&ndash;                            <div style="min-height: 20px">&ndash;&gt;-->
<!--                <div class="image-default-h">-->
<!--                  <v-chip v-if="getBaseFile1(school.basefile1) != ''" small label dark color="orange darken-3" class="ml-1" :href="`/data/${getBaseFile1(school.basefile1)}`" download>-->
<!--                    <v-icon left>mdi-file-powerpoint-box</v-icon>-->
<!--                    <span>{{getBaseFile1(school.basefile1)}}</span>-->
<!--                  </v-chip>-->
<!--                </div>-->
<!--              </td>-->
<!--              <td colspan="1">-->
<!--                <div class="image-default-h">-->
<!--                  <v-chip v-if="getBaseFile1(school.image_path1) != ''" small label dark color="orange darken-3" class="ml-1" :href="`/data/${getBaseFile1(school.image_path1)}`" download>-->
<!--                    <v-icon left>mdi-file-powerpoint-box</v-icon>-->
<!--                    <span>{{getBaseFile1(school.image_path1)}}</span>-->
<!--                  </v-chip>-->
<!--                </div>-->
<!--              </td>-->
<!--            </tr>-->
<!--            <tr>-->
<!--              <td colspan="1">-->
<!--                <div class="image-default-h">-->
<!--                  <v-chip v-if="getBaseFile1(school.image_path2) != ''" small label dark color="orange darken-3" class="ml-1" :href="`/data/${getBaseFile1(school.image_path2)}`" download>-->
<!--                    <v-icon left>mdi-file-powerpoint-box</v-icon>-->
<!--                    <span>{{getBaseFile1(school.image_path2)}}</span>-->
<!--                  </v-chip>-->
<!--                </div>-->
<!--              </td>-->
<!--              <td colspan="1">-->
<!--                <div class="image-default-h">-->
<!--                  <v-chip v-if="getBaseFile1(school.image_path3) != ''" small label dark color="orange darken-3" class="ml-1" :href="`/data/${getBaseFile1(school.image_path3)}`" download>-->
<!--                    <v-icon left>mdi-file-powerpoint-box</v-icon>-->
<!--                    <span>{{getBaseFile1(school.image_path3)}}</span>-->
<!--                  </v-chip>-->
<!--                </div>-->
<!--              </td>-->
<!--            </tr>-->
<!--            <tr>-->
<!--              <td colspan="1">-->
<!--                <div class="image-default-h">-->
<!--                  <v-chip v-if="getBaseFile1(school.image_path5) != ''" small label dark color="orange darken-3" class="ml-1" :href="`/data/${getBaseFile1(school.image_path5)}`" download>-->
<!--                    <v-icon left>mdi-file-powerpoint-box</v-icon>-->
<!--                    <span>{{getBaseFile1(school.image_path5)}}</span>-->
<!--                  </v-chip>-->
<!--                </div>-->
<!--              </td>-->
<!--              <td colspan="1">-->
<!--                <div class="image-default-h">-->
<!--                  <v-chip v-if="getBaseFile1(school.image_path6) != ''" small label dark color="orange darken-3" class="ml-1" :href="`/data/${getBaseFile1(school.image_path6)}`" download>-->
<!--                    <v-icon left>mdi-file-powerpoint-box</v-icon>-->
<!--                    <span>{{getBaseFile1(school.image_path6)}}</span>-->
<!--                  </v-chip>-->
<!--                </div>-->
<!--              </td>-->
<!--            </tr>-->
<!--            <tr>-->
<!--              <td colspan="1">-->
<!--                <div class="image-default-h">-->
<!--                  <v-chip v-if="getBaseFile1(school.image_path7) != ''" small label dark color="orange darken-3" class="ml-1" :href="`/data/${getBaseFile1(school.image_path7)}`" download>-->
<!--                    <v-icon left>mdi-file-powerpoint-box</v-icon>-->
<!--                    <span>{{getBaseFile1(school.image_path7)}}</span>-->
<!--                  </v-chip>-->
<!--                </div>-->
<!--              </td>-->
<!--              <td colspan="1">-->
<!--                <div class="image-default-h">-->
<!--                  <v-chip v-if="getBaseFile1(school.image_path8) != ''" small label dark color="orange darken-3" class="ml-1" :href="`/data/${getBaseFile1(school.image_path8)}`" download>-->
<!--                    <v-icon left>mdi-file-powerpoint-box</v-icon>-->
<!--                    <span>{{getBaseFile1(school.image_path8)}}</span>-->
<!--                  </v-chip>-->
<!--                </div>-->
<!--              </td>-->
<!--            </tr>-->
          </table>
          <div>
            <span class="abl-table-subtitle">7) 재난안전 예방 바로가기</span>

            <table class="abl-table-ts">
              <colgroup>
              </colgroup>
              <tr>
                <th colspan="2">안내문구</th>
              </tr>
              <tr>
                <td colspan="2">
                  <span style="text-align: left">
                    풍수해 예방대책에 대한 온라인 안전교육 콘텐츠(단, 5분 만에 알아보는 재난·안전교육)를 다음과 안내하오니 교육시설의 안전 및 유지관리를 위해 적극 활용하시어 향후 유사 재난이 발생하지 않도록 만전을 기하여 주시기 바랍니다.<br>(홈페이지 : <a href="http://www.koies.or.kr/00163"  target="_blank">http://www.koies.or.kr/00163</a> 또는 유튜브 채널 “한국교육시설안전원”)
                  </span>
                </td>
              </tr>
              <tr>
                <th colspan="1">풍해정보 바로가기</th>
                <th colspan="1">수해정보 바로가기</th>
              </tr>
              <tr style="height:40px">
                <td colspan="1">
                  <v-btn elevation="1" color="primary" small :href="'https://www.youtube.com/watch?v=zisIzOebP4Q'" target="_blank">
                    <v-icon>mdi-arrow-right-bold-circle-outline</v-icon><span>풍해정보 바로가기</span>
                  </v-btn>
                </td>
                <td colspan="1">
                  <v-btn elevation="1" color="primary" small :href="'https://www.youtube.com/watch?v=s8RqEo100Uw'" target="_blank">
                    <v-icon>mdi-arrow-right-bold-circle-outline</v-icon><span>수해정보 바로가기</span>
                  </v-btn>
                </td>
              </tr>
            </table>
          </div>
          <br>
        </div>
      </abl-document>
      </v-card-text>
    </v-card>
    <v-dialog v-model="deleteDialog.show" max-width="500px">
      <v-card>
        <v-card-title>삭제하시겠습니까?</v-card-title>
        <v-card-actions>
          <v-btn tile depressed class="flex-grow-1" @click="delImageFilePath()">삭제</v-btn>
          <v-btn tile depressed class="flex-grow-1" @click="deleteDialog.show = false">취소</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="pdfDialog.show" max-width="500px">
      <v-card>
        <v-card-title>PDF 다운로드 하시겠습니까?</v-card-title>
        <v-card-actions>
          <v-btn tile depressed class="flex-grow-1" @click="pdfSave()">다운로드</v-btn>
          <v-btn tile depressed class="flex-grow-1" @click="pdfDialog.show = false;pdf_save_flag = false">취소</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <input type="file" ref="fileinput" accept=".png,.jpg,.jpeg" class="f-pos" @change="onFileChangeHandler($event)" onclick="this.value=null"/>
  </div>
</template>

<script>
import AblDocument from '@/components/AblDocument'
import AblTextarea from '@/components/AblTextarea'
import {jsPDF} from 'jspdf'
import axios from 'axios'
import moment from 'moment'
export default {
  props: {
    accident: { type: Object, required: true }
  },
  components: {AblDocument, AblTextarea},
  methods: {
    async getAccidentsPast() {
      this.loading = true
      try {
        if(this.accident.disaster_num == undefined)
          this.accident.disaster_num = this.accident.acci_number
        let q = JSON.stringify({ filters: [{name: 'disaster_num', op: 'eq', val: this.accident.disaster_num}] })
        let {data} = await this.$http.get('accidentpast', {params: {q}})
        if (data.objects.length) this.school = data.objects[0]
        else console.error('NO DATA')
        this.s3_data_json = JSON.parse(this.school.s3_data_json)
        console.log("s3_2_group : " + JSON.stringify(this.s3_data_json.s3_2_group))
        this.refresh_id += 1
      }
      catch (ex) {
        console.error(ex.message)
      }
      finally {
        this.loading = false
      }
    },
    getBaseFile1(basefile){
      if(basefile != undefined && basefile.length > 10) {
        var arrayData = basefile.split(';')
        if (arrayData.length > 0)
          return arrayData[arrayData.length - 1]
      }
      return ''
    },
    async emitCallbackImage(image_data){
      
      this.file_post_upload(image_data,true)
    },
    async file_post_upload(image_file,bInsertToUi=true) {
      const fd = new FormData()
      fd.append('file', image_file)
      let {data} = await this.$http.post('attachment', fd)
      console.log("data.filename :" + JSON.stringify(data.filename))
      if (!data || !data.result || !data.filename)
        return alert("이미지 저장실패!!")
      this.insertImage(`/api/monitor/v1/attachment/${data.filename}`)
      this.saveDamagePast()
    },
    async onFileChangeHandler (evt) {
      console.log("onFileChangeHandler1")
      if (evt.target && evt.target.files && evt.target.files[0]) {
        console.log("onFileChangeHandler2")
        // let data = await this.toDataUrl(evt.target.files[0])
        // this.insertImage(data)
        this.file_post_upload(evt.target.files[0],true)
      }
      else return null
    },
    insertImage (path) {
      console.log("path : " + path)
      
      console.log("document : " + document.querySelector("image_1"))
      document.execCommand('InsertHtml', false, `
                <div style="width: 260px; height:200px;">
                    <img src="${path}"  style="width: 250px; height:200px;">
                </div>
            `)
      this.refresh_id += 1
    },
    async saveDamagePast() {
      var params = {
        'acci_past_id':this.school.id,
        'image_file_path1':this.school.image_file_path1,
        'image_file_path2':this.school.image_file_path2,
        'image_file_path3':this.school.image_file_path3,
        'image_file_path4':this.school.image_file_path4,
        'image_file_path5':this.school.image_file_path5,
        'image_file_path6':this.school.image_file_path6,
      };
      let res = await this.$http.post(`update_damage_imagepath`, params)
      if(res.status == 200){
        // this.alert_dialog.show = true
        this.getAccidentsPast()
      }
    },
    get_payment_money(total_payment_money){
      if(total_payment_money == null){
        return ' '
      }
      return total_payment_money
    },
    check_null(data){
      if(data == null || data == undefined || data == '')
        return " "
      return data
    },
    check_cost(data){
      if(data == null || data == undefined || data == '')
        return " "
      return data + '원'
    },
    check_area(data){
      if(data != '' && data != null){
        return data + '㎡'
      }
      return ''
    },
    check_9_10(item){
      if(Object.keys(item).includes("s3_data2_9") == true)
        return "대인"
      else if(Object.keys(item).includes("s3_data2_10") == true)
        return "대물"
      return ''
    },
    check_9_10_1(item){
      if(Object.keys(item).includes("s3_data1_9") == true)
        return item.s3_data1_9
      else if(Object.keys(item).includes("s3_data1_10") == true)
        return item.s3_data1_10
      return ''
    },
    check_9_10_2(item){
      if(Object.keys(item).includes("s3_data2_9") == true)
        return item.s3_data2_9
      else if(Object.keys(item).includes("s3_data2_10") == true)
        return item.s3_data2_10
      return ''
    },
    check_9_10_4(item){
      if(Object.keys(item).includes("s3_data4_9") == true)
        return item.s3_data4_9
      else if(Object.keys(item).includes("s3_data4_10") == true)
        return item.s3_data4_10
      return ''
    },
    check_s3_5_group_total_sum(s3_5_group){
      let total = 0;
      for (let item in s3_5_group) {
        if(Object.keys(s3_5_group[item]).includes("s3_total_5") == true)
          total += s3_5_group[item].s3_total_5
      }
      return total
    },
    check_s3_7_group_total_sum(s3_5_group){
      let total = 0;
      for (let item in s3_5_group) {
        if(Object.keys(s3_5_group[item]).includes("s3_total_7") == true)
          total += s3_5_group[item].s3_total_7
      }
      return total
    },
    check_s3_2_group_total_sum(s3_2_group){
      let total = 0;
      for (let item in s3_2_group) {
        if(Object.keys(s3_2_group[item]).includes("s3_total_2") == true)
          total += s3_2_group[item].s3_total_2
        if(Object.keys(s3_2_group[item]).includes("s3_total_3") == true)
          total += s3_2_group[item].s3_total_3
      }
      return parseInt(total)
    },
    check_s3_1_group_total_sum(s3_1_group){
      let total = 0;
      for (let item in s3_1_group) {
        if(Object.keys(s3_1_group[item]).includes("s3_final_total") == true)
          total += s3_1_group[item].s3_final_total
      }
      return parseInt(total)
    },
    check_total(data){
      if(data == null || data == undefined || data == 0)
        return ''
      return data + '원'
    },
    getJsonValue(group,key){
      var value_list = this.s3_data_json[group].map(v=> v[key])
      var results = ''
      for(var i=0;i<value_list.length;i++){
        if(value_list[i] != undefined && value_list[i].length > 0){
          if(i == 0)
            results += value_list[i]
          else
            results += ',' +  value_list[i]
        }
      }
      return results
    },
    getJsonGroupsTotalValue(group,key1,key2){
      var value_list1 = this.s3_data_json[group].map(v=> v[key1])
      var value_list2 = this.s3_data_json[group].map(v=> v[key2])
      var total = value_list1.reduce((sum, item) => sum + item, 0) + value_list2.reduce((sum, item) => sum + item, 0);
      if(!isNaN(total))
        return Number(total) + '원'
      return '';
    },
    getJsonGroup12(index,key){
      if(this.s3_data_json['s3_12'].length >= index &&  Object.keys(this.s3_data_json['s3_12'][index]).includes(key)) {
        var total = this.s3_data_json['s3_12'][index][key]
        if (!isNaN(total))
          return Number(total) + '원'
      }
      return '';
    },
    getJsonGroupTotalValue(group,key1){
      var value_list1 = this.s3_data_json[group].map(v=> v[key1])
      var total = value_list1.reduce((sum, item) => sum + item, 0)
      if(!isNaN(total) && total != 0)
        return Number(total) + '원'
      return '';
    },
    getJsonGroupNames(group){
      var results = []
      if(Object.keys(group).includes("s3_data1_8") && group['s3_data1_8'] !='0')
        results.push('안전진단비')
      if(Object.keys(group).includes("s3_data2_8") && group['s3_data2_8'] !='0')
        results.push('급식지원비')
      if(Object.keys(group).includes("s3_data3_8") && group['s3_data3_8'] !='0')
        results.push('토사제거비')
      if(Object.keys(group).includes("s3_data4_8") && group['s3_data4_8'] !='0')
        results.push('이동·보관비')
      if(Object.keys(group).includes("s3_data5_8") && group['s3_data5_8'] !='0')
        results.push('석면해체비')
      if(Object.keys(group).includes("s3_data6_8") && group['s3_data6_8'] !='0')
        results.push('법정수수료')
      if(Object.keys(group).includes("s3_data7_8") && group['s3_data7_8'] !='0')
        results.push('법정수수료')
      if(Object.keys(group).includes("s3_data8_8") && group['s3_data8_8'] !='0')
        results.push('오염청소·소독비')
      if(Object.keys(group).includes("s3_data9_8") && group['s3_data9_8'] !='0')
        results.push('응급조치비')
      return results.join(',');
    },
    getJsonGroupTotal(group){
      var results = []
      if(Object.keys(group).includes("s3_data1_8") && group['s3_data1_8'] !='0')
        results.push(group['s3_data1_8'])
      if(Object.keys(group).includes("s3_data2_8") && group['s3_data2_8'] !='0')
        results.push(group['s3_data2_8'])
      if(Object.keys(group).includes("s3_data3_8") && group['s3_data3_8'] !='0')
        results.push(group['s3_data3_8'])
      if(Object.keys(group).includes("s3_data4_8") && group['s3_data4_8'] !='0')
        results.push(group['s3_data4_8'])
      if(Object.keys(group).includes("s3_data5_8") && group['s3_data5_8'] !='0')
        results.push(group['s3_data5_8'])
      if(Object.keys(group).includes("s3_data6_8") && group['s3_data6_8'] !='0')
        results.push(group['s3_data6_8'])
      if(Object.keys(group).includes("s3_data7_8") && group['s3_data7_8'] !='0')
        results.push(group['s3_data7_8'])
      if(Object.keys(group).includes("s3_data8_8") && group['s3_data8_8'] !='0')
        results.push(group['s3_data8_8'])
      if(Object.keys(group).includes("s3_data9_8") && group['s3_data9_8'] !='0')
        results.push(group['s3_data9_8'])

      var total = results.reduce((sum, item) => sum + item, 0)
      if(!isNaN(total) && total != 0)
        return Number(total) + '원'
      return '';
    },
    deleteDialogShow(image_file_path,image_index){
      if(image_file_path != ''){
        this.deleteDialog.show=true
        this.deleteDialog.delItem = image_index
      }
    },
    delImageFilePath(){
      if(this.deleteDialog.delItem == '1'){
        this.school.image_file_path1 = this.school.image_file_path2
        this.school.image_file_path2 = this.school.image_file_path3
        this.school.image_file_path3 = this.school.image_file_path4
        this.school.image_file_path4 = this.school.image_file_path5
        this.school.image_file_path5 = this.school.image_file_path6
        this.school.image_file_path6 = ''
      }
      if(this.deleteDialog.delItem == '2'){
        this.school.image_file_path2 = this.school.image_file_path3
        this.school.image_file_path3 = this.school.image_file_path4
        this.school.image_file_path4 = this.school.image_file_path5
        this.school.image_file_path5 = this.school.image_file_path6
        this.school.image_file_path6 = ''
      }
      if(this.deleteDialog.delItem == '3'){
        this.school.image_file_path3 = this.school.image_file_path4
        this.school.image_file_path4 = this.school.image_file_path5
        this.school.image_file_path5 = this.school.image_file_path6
        this.school.image_file_path6 = ''
      }
      if(this.deleteDialog.delItem == '4'){
        this.school.image_file_path4 = this.school.image_file_path5
        this.school.image_file_path5 = this.school.image_file_path6
        this.school.image_file_path6 = ''
      }
      if(this.deleteDialog.delItem == '5'){
        this.school.image_file_path5 = this.school.image_file_path6
        this.school.image_file_path6 = ''
      }
      if(this.deleteDialog.delItem == '6'){
        this.school.image_file_path6 = ''
      }
      this.refresh_id += 1
      this.saveDamagePast()
      this.deleteDialog.show = false
    },
    async capture (id) {
      if (this.$refs['report'] && this.$refs['report'].capture) {
        let blob = await this.$refs['report'].capture()
        return blob
      }
      else return null
    },
    saveToPDF () {
      this.pdf_save_flag = true
      this.pdfDialog.show = true

    },
    async pdfSave(){
      this.pdfDialog.show = false
      if(this.$session.hasPermission([5,6])){
        if(this.$session.hasPermission([5]) && this.$session.getUserId() != this.school.mem_num){
          this.$session.$emit('modal-alert', "권한이 없습니다.")
          return
        }
        if(this.$session.hasPermission([6]) && this.$session.getUserId() != this.school.school_number){
          this.$session.$emit('modal-alert', "권한이 없습니다.")
          return
        }
      }
      let title = this.school.school_name + this.school.sub2_sdate.substring(0,4) + '년도 세부 피해 내역 보고서.pdf'
      let image_data = await this.capture(0)
      let format = this.$refs.report.getDocumentSize()
      const doc = new jsPDF({orientation: 'p', unit: 'px', format})
      const imgProps= doc.getImageProperties(image_data);

      let pdfWidth, pdfHeight, docMargin = 20
      pdfWidth = doc.internal.pageSize.getWidth();
      pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
      if (pdfHeight > doc.internal.pageSize.getHeight()) {
        pdfHeight = doc.internal.pageSize.getHeight()
        pdfWidth = (imgProps.width * pdfHeight) / imgProps.height;
        // marginX = (doc.internal.pageSize.getWidth() - pdfWidth) / 2
      }
      doc.addImage(image_data, 'png', docMargin-5, docMargin, pdfWidth - (docMargin * 2), pdfHeight - (docMargin * 2))
      doc.save(title)
      this.pdf_save_flag = false
    },
    check_permission(){
      if(this.pdf_save_flag == true){
        return false
      }

      if(this.$session.hasPermission([1,2,3])){
        if(this.$session.hasPermission([1]))
          return true
        if(this.$session.hasPermission([2])){
          if(this.school.regional_code == 'A001'){ //공제사업처인경우 코드가 A001(본부)인경우 가능
            return true
          }else{
            return false
          }
        }
        if(this.$session.hasPermission([3])){
          var find_code = this.member_area_type.find(v=>v.value == this.$session.getUserArea()).code
          if(find_code == this.school.regional_code){
            return true
          }else{
            return false
          }
        }
      }
      return false
    },

    getCheckSchoolName(){
      if(this.$session.hasPermission([5])) {
        if(this.$session.getUserId() != this.school.mem_num){
          return "***"
        }
      }
      else if(this.$session.hasPermission([6])) {
        if(this.$session.getUserId() != this.school.school_num){
          return "***"
        }
      }
      return this.school.school_name
    },
    getCheckAddress(){
      if(this.$session.hasPermission([5])) {
        if(this.$session.getUserId() != this.school.mem_num){
          return "***"
        }
      }
      else if(this.$session.hasPermission([6])) {
        if(this.$session.getUserId() != this.school.school_num){
          return "***"
        }
      }
      return this.school.addr1
    },
    async onImageDownload(image_file_path){
      var first_idx = image_file_path.indexOf('src=')
      var end_idx = image_file_path.indexOf('.png')
      var url = this.$session.getWebURL() + image_file_path.substr(first_idx+5, end_idx - first_idx-1)
      axios({
        url: url,
        method: 'GET',
        responseType: 'blob',
      }).then((response) => {
        var fileURL = window.URL.createObjectURL(new Blob([response.data]));
        var fileLink = document.createElement('a');

        fileLink.href = fileURL;
        fileLink.setAttribute('download', 'image.png');
        document.body.appendChild(fileLink);
        fileLink.click();
      });
      // var base64 = await axios
      //     .get(url, {
      //       responseType: "arraybuffer"
      //     })
      //     .then(response =>
      //         Buffer.from(response.data, "binary").toString("base64")
      //     );
      // var img = new Image();
      // img.src = "data:image/jpeg;base64, " + base64;
    }
    // getCheckMemName(){
    //   if(this.$session.hasPermission([5])) {
    //     if(this.$session.getUserId() != this.info.school_id){
    //       return "미공개"
    //     }
    //   }else if(this.$session.hasPermission([6])) {
    //     if(this.$session.getUserId() != this.info.school_number){
    //       return "미공개"
    //     }
    //   }
    //   return this.school.mem_name + "(" + this.info.school_id + ")"
    // }
  },
  mounted () {
    // console.log(`[${this.accident.acci_number} school detail mounted]`)
    this.getAccidentsPast()
  },
  data () {
    return {
      preview: null,
      loading: false, 
      school: {},
      refresh_id:0,
      s3_data_json:null,
      deleteDialog:{
        show: false,
        delItem:''
      },
      previews:[],
      pdf_save_flag:false,
      pdfDialog:{
        show:false
      },
      member_area_type:[
        {text:'서울강원',value:'R001',code:'A002'},
        {text:'경기인천',value:'R002',code:'A003'},
        {text:'대전충청',value:'R003',code:'A004'},
        {text:'대구경북',value:'R004',code:'A005'},
        {text:'부산경남',value:'R005',code:'A006'},
        {text:'호남제주',value:'R006',code:'A007'},
      ],
    }
  }
}
</script>

<style lang="scss" scoped>
.t1 {
  text-align: justify;
  text-align-last: justify;
  flex: 1 0 auto;
  padding: 0 10px;
}
.abl-page {
  padding: 15px 30px;
}
.school-file-upload {
  position: relative;
  top: 0px; left: 10px;
  z-index: 10;
}
.school-save {
  position: relative;
  top: -10px; left:15px;
  z-index: 10;
}
.report-download {
  position: relative;
  top: -10px; left:780px;
  z-index: 10;
}
.image-left-m{
  overflow: hidden;
  text-align: center;
  display: block;
  margin-left: auto;
  margin-right: auto;
}
.td-bold{
  background-color: #e7e7e7;
}
.image-default-h{
  height:26px !important;
  text-align: center;
}
.f-pos{
  position: fixed;
  top: -1000px; left: 0;
}
</style>