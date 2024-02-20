<template>
  <main-layout>
    <template v-slot:left>
        <div key="result" class="sub-menu elevation-2">
          <dl class="filter-panel">
            <dd>
              <v-btn-toggle v-model="search.type" 
                color="primary"
                dense mandatory class="mb-3 d-flex"
                @change="searchTypeChangeHandler">
                <v-btn value="01" class="flex-grow-1">과거 태풍 검색</v-btn>
                <!-- <v-btn value="02">현재태풍</v-btn> -->
                <v-btn value="03" class="flex-grow-1">태풍 피해 예측</v-btn>

              </v-btn-toggle>
            </dd>
            <dd>
              <div class="d-flex" style="align-items: center;">
                <div class="" style="flex-grow: 1;">
                  <template v-if="search.type === '01'">
                    <v-select outlined dense hide-details 
                      v-model="search.inp1" 
                      :items="search.items1" 
                      label="발생연도" 
                      item-text="name" 
                      item-value="code" 
                      @change="inp1ChangeHandler"
                    />
                    <div style="width:10px; height: 10px;"></div>
                    <v-select outlined dense hide-details
                      v-model="search.inp2"
                      :items="search.items2" 
                      :disabled="!search.inp1" 
                      :label="search.inp1 ? '태풍' : '태풍를 선택해주세요'" 
                      item-text="name" 
                      item-value="code" 
                    />
                  </template>
                  <!-- <template v-if="search.type === '02'">
                    <v-select outlined dense hide-details disabled
                      v-model="search.inp1" 
                      :items="search.items1"  
                      label="발생연도" 
                      item-text="name" 
                      item-value="code" 
                      @change="inp1ChangeHandler"
                    />
                    <div style="width:10px; height: 10px;"></div>
                    <v-select outlined dense hide-details
                      v-model="search.inp2"
                      :items="search.items2" 
                      :disabled="!search.inp1" 
                      :label="search.inp1 ? '태풍' : '태풍를 선택해주세요'" 
                      item-text="name" 
                      item-value="code" 
                    />
                  </template> -->
                  <template v-if="search.type === '03'">
                    <!-- <v-select outlined dense hide-details
                      v-model="search.inp1" 
                      :items="search.items1" 
                      label="발생연도" 
                      item-text="name" 
                      item-value="code" 
                      @change="inp1ChangeHandler"
                    /> -->
                    <div style="width:10px; height: 10px;"></div>
                    <v-select outlined dense hide-details 
                      v-model="search.inp2"
                      :items="search.items2" 
                      :disabled="!search.inp1" 
                      :label="search.inp1 ? '태풍' : '태풍를 선택해주세요'" 
                      item-text="name" 
                      item-value="code"
                    />
                  </template>
                </div>
              </div>
            </dd>
            <dd>
              <div class="d-flex mt-4">
                <v-btn text small class="flex-grow-1" @click="resetClickHandler">
                  초기화
                </v-btn>
                <v-btn rounded small depressed color="primary" class="flex-grow-1" @click="searchClickHandler">
                  검색
                </v-btn>
              </div>
            </dd>
          </dl>
        </div>

        <div key="filter" class="sub-menu elevation-2 mt-2">
          <dl class="filter-panel">
            <dt>
              <div class="result-panel-title">태풍피해 상세 내역</div>
            </dt>
            <dd>
              <div class="summary-row">
                <div class="summary-label"><span v-if="search.type === '03'">예상</span> 피해학교수</div>
                <div class="summary-value">
                  <count-up
                    :delay="1000"
                    :endVal="summary.count"
                    :options="{suffix: '개교'}"
                    @onReady="(instance) => summary.instCount = instance"
                  />
                </div>
              </div>
              <div class="summary-row">
                <div class="summary-label"><span v-if="search.type === '03'">예상</span> 피해금액</div>
                <div class="summary-value">
                  <count-up
                    :delay="1000"
                    :endVal="summary.cost/1000000"
                    :options="{suffix: '백만원'}"
                    @onReady="(instance) => summary.instTotal = instance"
                  />
                </div>
              </div>
            </dd>
          </dl>
          <v-divider dark />
          <div class="text-center" v-if="tableData.loading">
            <span class="grey--text text--darken-1 py-4">LOADING...</span>
          </div>
          <div class="summary-table" color="transparent" v-else>
            <div style="max-height:400px; overflow-y: auto;">
              <transition-group name="flip-list" tag="div" v-bind:css="false"
                v-on:before-enter="listTransitionBeforeEnter"
                v-on:enter="listTransitionEnter"
                v-on:leave="listTransitionLeave">
                <div
                  v-for="(row, index) in tableData.items" :key="row.id" 
                  class="d-flex justify-space-between damaged-item px-4 py-1"
                  :class="$getTextColor(row.total_cost)"
                  :data-index="index" 
                  @click="viewDetail(row)">
                  <div class="flex-grow-1 text-caption text-truncate">{{row.school_name}}</div>
                  <div class="flex-grow-1 text-caption text-right">{{row.total_cost | makeComma}}원</div>
                  <!--<div class="flex-grow-1 text-caption text-right">{{$getCostRange(row.total_cost)}}</div> -->
                  
                </div>
              </transition-group>
            </div>
          </div>
        </div>
    </template>

    <template v-slot>
      <v-container fluid class="fill-height dashboard-container pa-0" :class="{'map-view': mapView}">
        <vue-daum-map
          :appKey="kakaomap.appKey"
          :center.sync="kakaomap.center"
          :level.sync="kakaomap.level"
          :mapTypeId="kakaomap.mapTypeId"
          :libraries="kakaomap.libraries"
          :style="kakaomap.style"
          @load="loadedMap"
          @zoom_changed="zoomUpdate"
        />
      </v-container>
      <div class="detail-view-2">
        <v-card flat elevation="1" class="mb-2 detail-view-path_2">
          <div class="no-m">
            <table>
              <tr>
                <td class="cost_color_1_">규모 1<br>관심</td>
                <td class="cost_color_2_">규모 2<br>주의</td>
                <td class="cost_color_3_">규모 3<br>경계</td>
                <td class="cost_color_4_">규모 4<br>위험</td>
                <td class="cost_color_5_">규모 5<br>심각</td>
              </tr>
            </table>
          </div>
        </v-card>
      </div>
      <div class="detail-view" v-if="current.typhoon">

        <template v-if="(current.typhoon.paths.length - 1) === current.selectedPath">
          <div class="summary-view" v-if="panels.total && (current.typhoon.paths.length - 1) === current.selectedPath">
            <v-card flat color="rgba(255,255,255,0.86)" elevation="2">
              <v-system-bar dark color="blue darken-2" class="cursor-pointer" @click="viewPanel('total', false)">
                <div>태풍 피해 현황(누적)</div>
                <v-spacer/>
                <v-icon>mdi-eye-off</v-icon>
              </v-system-bar>
              <v-card-text class="pa-2">
                <div class="chart-label">지역별 <span v-if="current.typhoon.typhoon_v_type === 1">예상</span> 피해 규모</div>
                <highcharts 
                  constructor-type="chart"
                  :options="chartDamageByRegion"
                />
                <v-divider class="mb-2"/>
                <div class="chart-label">학교급별 <span v-if="current.typhoon.typhoon_v_type === 1">예상</span> 피해 규모</div>
                <highcharts 
                  constructor-type="chart"
                  :options="chartDamageByType"
                />
              </v-card-text>
            </v-card>
          </div>
        </template>
        <template v-else>
          <div class="detail-view-chart" v-if="panels.onpath && current.selectedPath >= 0">
            <v-card flat color="rgba(255,255,255,0.86)" elevation="2">
              <v-system-bar class="cursor-pointer" @click="viewPanel('onpath', false)">
                <div>태풍 피해 현황(누적)</div>
                <v-spacer/>
                <v-icon>mdi-eye-off</v-icon>
              </v-system-bar>
              <v-card-text class="pa-2">
                <div class="chart-label">지역별 <span v-if="current.typhoon.typhoon_v_type === 1">예상</span> 피해 규모</div>
                <highcharts 
                  v-if="tableData.items.length"
                  constructor-type="chart"
                  :options="chartDamageByRegion"
                />
                <div v-else class="text-center text-caption font-italic py-10">현 경로에 피해 시설 없음</div>
                <v-divider class="mb-2"/>
                <div class="chart-label">학교급별 <span v-if="current.typhoon.typhoon_v_type === 1">예상</span> 피해 규모</div>
                <highcharts 
                  v-if="tableData.items.length"
                  constructor-type="chart"
                  :options="chartDamageByType"
                />
                <div v-else class="text-center text-caption font-italic py-10">현 경로에 피해 시설 없음</div>
              </v-card-text>
            </v-card>
          </div>
        </template>
        <div>
          <template v-if="(current.typhoon.paths.length - 1) === current.selectedPath">
            <v-card flat elevation="2" class="mb-2" v-if="!panels.total">
              <v-system-bar class="cursor-pointer" dark color="blue darken-2" @click="viewPanel('total', true)">
                <div>태풍 피해 현황(누적)</div>
                <v-spacer/>
                <v-icon>mdi-eye</v-icon>
              </v-system-bar>
            </v-card>
          </template>
          <template v-else>
            <v-card flat elevation="2" class="mb-2" v-if="!panels.onpath && current.selectedPath >= 0">
              <v-system-bar class="cursor-pointer" @click="viewPanel('onpath', true)">
                <div>태풍 피해 현황(누적)</div>
                <v-spacer/>
                <v-icon>mdi-eye</v-icon>
              </v-system-bar>
            </v-card>
          </template>

          <v-card flat elevation="2" class="mb-2 detail-view-path" v-if="!panels.paths">
            <v-system-bar class="cursor-pointer" @click="viewPanel('paths', true)">
              <div>태풍 경로</div>
              <v-spacer/>
              <v-icon>mdi-eye</v-icon>
            </v-system-bar>
          </v-card>

          <v-card flat elevation="2" class="detail-view-path" color="rgba(255,255,255,0.86)" v-else>
            <v-system-bar class="cursor-pointer" @click="viewPanel('paths', false)">
              <div>태풍 경로</div>
              <v-spacer/>
              <v-icon>mdi-eye-off</v-icon>
            </v-system-bar>
            <div class="path-list-wrap">
              <v-list dense color="transparent" max-height="690" class="py-0">
                <v-list-item v-for="(path, idx) in currentTyphoonPaths" :key="path.id" three-line
                  :class="{'v-list-item--active': current.selectedPath === idx}"
                  @click="onPathClickHandler(current.typhoon.typhoon_id, idx)">
                  <v-list-item-avatar>
                    <v-icon :style="{transform: `rotate(${convDirToDeg(path.direction)}deg)`}">mdi-arrow-up</v-icon>
                  </v-list-item-avatar>

                  <v-list-item-content>
                    <v-list-item-title>위도:{{path.latlng[0]}} 경도:{{path.latlng[1]}}</v-list-item-title>
                    <v-list-item-subtitle>이동속도:{{path.move_speed_h}}km/h</v-list-item-subtitle>
                    <v-list-item-subtitle>풍속: {{path.max_speed_s}}m/s 강도: {{path.storm_radius}} </v-list-item-subtitle>
                    <v-list-item-subtitle>중심압력: {{path.center_pressure}}hPa</v-list-item-subtitle>
                    <!-- <v-list-item-subtitle>풍속: {{path.max_speed_s}}m/s, {{path.max_speed_h}}km/h</v-list-item-subtitle> -->
                  </v-list-item-content>
                </v-list-item>
                <v-list-item v-if="currentTyphoonPaths.length === 0">
                  <v-list-item-content>
                    <v-list-item-subtitle>경로정보가 없습니다</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </div>
            <div class=""></div>
          </v-card>
        </div>
      </div>

      <v-dialog v-model="predict.confirm" max-width="420">
        <v-card>
          <v-card-title>태풍피해예측</v-card-title>
          <v-card-text>
            태풍피해예측을 시작하시겠습니까?
          </v-card-text>
          <v-card-actions>
            <v-btn text class="flex-grow-1" @click="predict.confirm = false">취소</v-btn>
            <v-btn tile class="flex-grow-1" color="primary" @click="requestPredict">네</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <div v-show="$session.hasPermission([5,6])" class="sw-func-btn">
        <v-switch
            v-model="ext_param.school_include"

            :label="getSwitchTitle()"
        ></v-switch>
      </div>
      <div class="dsh-func-btn" v-if="current.typhoon">
        <div class="dsh-func-btn-controls d-flex">
          <v-btn icon dark @click="resetScenario()">
            <v-icon large>mdi-skip-previous</v-icon>
          </v-btn>
          <v-btn icon dark
            class="ml-2"
            :loading="predict.progress.onPlay"
            @click="startScenario()">
            <v-icon large>mdi-play</v-icon>
          </v-btn>
          <v-btn icon dark class="ml-2" @click="pauseScenario()">
            <v-icon large>mdi-pause</v-icon>
          </v-btn>
          <v-btn icon dark class="ml-2" @click="resetScenario()">
            <v-icon large>mdi-stop</v-icon>
          </v-btn>
          <v-divider vertical dark inset class="mx-4"/>
          <v-icon large dark>mdi-clock-fast</v-icon>
          <v-btn icon :color="predict.progress.duration === 5000/2 ? 'red accent-2' : 'white'" class="mx-0" @click="predict.progress.duration = 5000/2"><v-icon large>mdi-numeric-1</v-icon></v-btn>
          <v-btn icon :color="predict.progress.duration === 6750/2 ? 'red accent-2' : 'white'" class="mx-0" @click="predict.progress.duration = 6750/2"><v-icon large>mdi-numeric-2</v-icon></v-btn>
          <v-btn icon :color="predict.progress.duration === 8500/2 ? 'red accent-2' : 'white'" class="mx-0" @click="predict.progress.duration = 8500/2"><v-icon large>mdi-numeric-3</v-icon></v-btn>
          <v-btn icon :color="predict.progress.duration === 10250/2 ? 'red accent-2' : 'white'" class="mx-0" @click="predict.progress.duration = 10250/2"><v-icon large>mdi-numeric-4</v-icon></v-btn>
          <v-btn icon :color="predict.progress.duration === 12000/2 ? 'red accent-2' : 'white'" class="mx-0" @click="predict.progress.duration = 12000/2"><v-icon large>mdi-numeric-5</v-icon></v-btn>
        </div>

        <v-btn rounded dark depressed
          v-if="[1].includes(current.typhoon.typhoon_v_type)"
          color="deep-orange accent-4"
          class="ml-2"
          :disabled="predict.progress.show"
          @click="predict.confirm = true">
          태풍 피해 예측
        </v-btn>

      </div>

      <v-bottom-sheet v-model="predict.progress.show" inset hide-overlay>
        <v-sheet class="text-center" height="120px">
          <div class="mx-4">
            <v-subheader>태풍 피해를 계산 중 입니다</v-subheader>
            <v-progress-linear v-model="predict.progress.value" :indeterminate="predict.progress.loading" query color="blue-grey" height="25">
              <template v-slot:default="{value}">
                <strong>{{value}}%</strong>
              </template>
            </v-progress-linear>
          </div>
        </v-sheet>
      </v-bottom-sheet>
      <v-dialog v-model="schooldetail.show" persistent max-width="1060px" max-height="500px">
        <div class="school-detail-container">
          <v-btn fab x-small dark depressed color="grey darken-1" class="school-detail-close" @click="onSchoolDetailCloseHandler()">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <school-detail v-if="schooldetail.data" :accident="schooldetail.data" />
        </div>
      </v-dialog>
    </template>
  </main-layout>
</template>

<script>
import _ from 'lodash'
import moment from 'moment'
import numeral from 'numeral'
import VueDaumMap from 'vue-daum-map'
import Velocity from 'velocity-animate'

import Typhoon from '@/components/Typhoon'
import SchoolDetail from '@/components/SchoolDetail'
import Vue from 'vue'

const TyphoonComponent = Vue.extend(Typhoon)

export default {
  components: { VueDaumMap, SchoolDetail},
  methods: {
    async getPathData () {
      let params = {type: this.search.type,fk_user_id: this.$session.getUserIndex()}
      if (this.search.inp1) params.h1 = this.search.inp1
      if (this.search.inp2) params.h2 = this.search.inp2

      let {data} = await this.$http.get('dashboard/paths', {params})
      this.paths = data

      for (let tid in this.overlays) {
        this.overlays[tid].unset()
        delete this.overlays[tid]
      }

      if (window.kakao) {
        let kakao = window.kakao
        let params = []
        let firstTp = null
        data.forEach((v, idx) => {
          if (!v.paths.length) return console.error(`경로정보가 없음 (${v.typhoon_name})`);
          if (firstTp === null) firstTp = v
          let startedAt = v.paths[0]

          const instance = new TyphoonComponent({
            propsData: {
              info: v, 
              color: this.colors[idx % 9],
              kakao: kakao,
              map: this.kakaomap.map,
              root: this,
              ext_param:this.ext_param
            }
          })

          instance.$on('click', this.onTyphoonClickHandler.bind(this))
          instance.$on('school-detail', this.onSchoolDetailHandler.bind(this))
          instance.$mount()
          this.overlays[v.typhoon_id] = instance
          params.push({latlng: startedAt.latlng})
        })

        let bounds = this.getBounds(params)
        if (bounds) this.kakaomap.map.setBounds(bounds)

        if (firstTp) {
          this.$nextTick(() => {
            this.onTyphoonClickHandler(firstTp.typhoon_id, firstTp)
          })
        }
      }
      
      return;
    },
    async getMetaData () {
      let params = {type: this.search.type,fk_user_id:this.$session.getUserIndex()}
      if (this.search.inp1) params.h = this.search.inp1
      let {data} = await this.$http.get('dashboard/filter', {params})
      _.remove(data, v => /없음/.test(v.name))
      if (this.search.inp1 && !this.search.inp2) {
        this.search.items2 = data
      }
      else {
        this.search.items1 = data
        
        if (!this.defLoad) {
          this.search.inp1 = data[0]
          this.searchClickHandler()
          this.defLoad = true
        }
      }
      return;
    },
    inp1ChangeHandler () {
      this.getMetaData()
      this.search.items2 = []
      this.search.inp2 = null
    },
    inpAllChangeHandler () {
      this.search.inp2 = this.search.inp1
    },
    searchClickHandler () {
      if (!this.search.inp1) return;
      this.getPathData()
      this.search.show = true
    },
    resetClickHandler () {
      this.search.inp1 = null
      this.search.inp2 = null
      this.search.inp3 = null

      this.summary.total = 0
      this.summary.cost = 0
      this.summary.count = 0
    },
    setFilterByName (name) {
      this.search.inp1 = null
      this.search.inp2 = null
      this.search.inp3 = name

      this.summary.total = 0
      this.summary.cost = 0
      this.summary.count = 0

      this.getData()
    },
    loadedMap (map) {
      map.setMinLevel(11)
      this.kakaomap.map = map
      this.getMetaData()
    },
    zoomUpdate() {
      console.log(`ZOOM: ${this.kakaomap.level}`)
    },
    viewDetail (row) {
      if (!row.id) return;
      console.log(row)
      // this.$router.push({name: 'dashboard-detail', params: {cmpyId: row.item.id}})
    },
    searchTypeChangeHandler () {
      if (this.search.type === '03') this.search.inp1 = moment().format('YYYY')
      else this.search.inp1 = null
      this.search.inp2 = null

      this.summary.total = 0
      this.summary.cost = 0
      this.summary.count = 0

      this.getMetaData()
    },
    getBounds (list) {
      if (!list.length) return;
      if (!window.kakao) return;
      let kakao = window.kakao
      let lat = list.map(v => v.latlng[0])
      let lng = list.map(v => v.latlng[1])

      let sw = new kakao.maps.LatLng(_.min(lat), _.min(lng))
      let ne = new kakao.maps.LatLng(_.max(lat), _.max(lng))
      return new kakao.maps.LatLngBounds(sw, ne)
    },

    unsetAllOverlays () {
      for (let tid in this.overlays) {
        this.overlays[tid].blur()
      }
    },
    async onTyphoonClickHandler (tid, typhoon) {
      this.current.show = false
      this.unsetAllOverlays()
      this.overlays[tid].focus()
      this.current.typhoon = typhoon
      this.current.selectedPath = -1
      this.current.show = true
    },
    async onSchoolDetailHandler (schoolData) {
      if (this.current.typhoon && [0].includes(this.current.typhoon.typhoon_v_type)){
        this.schooldetail.data = schoolData
        this.schooldetail.show = true
      }else{
        let filters_or = []
        let filters_and = []
        filters_and.push({name: 'school_num', op: 'eq', val: schoolData.school_number})
        let q = {
          filters: [{or: filters_or}, {and: filters_and}],
          order_by: [{field: 'sub2_sdate', direction: 'desc'}]
        }
        let params = {q: JSON.stringify(q), results_per_page: 1, page: 1}
        let {data} = await this.$http.get("accidentpast", {params});
        if(data.objects.length == 0){
          this.$session.$emit('modal-alert', '해당 학교의 과거 피해 내역은 없으나 약 ' + schoolData.total_cost.toLocaleString('ko-KR') + '원의 피해가 예상됩니다.')
          return
        }
        this.schooldetail.data = data.objects[0]
        console.log("schooldetail :" + JSON.stringify(this.schooldetail.data))
        this.schooldetail.show = true
      }
    },
    onSchoolDetailCloseHandler () {
      this.schooldetail.show = false
      this.schooldetail.data = null
    },
    onPathClickHandler (tid, step) {
      this.current.selectedPath = step
      this.overlays[tid].set(step)
    },
    convDirToDeg (dir) {
      return ({
        '북': 0,
        '북북동': 22.5,
        '북동': 45,
        '동북동': 67.5,
        '동': 90,
        '동남동': 112.5,
        '남동': 135,
        '남남동': 157.5,
        '남': 180,
        '남남서': 202.5,
        '남서': 225,
        '서남서': 247.5,
        '서': 270,
        '서북서': 292.5,
        '북서': 315,
        '북북서': 337.5
      })[dir]
    },
    listTransitionBeforeEnter (el) {
      el.style.opacity = 0
      el.style.height = 0
    },
    listTransitionEnter (el, done) {
      var delay = el.dataset.index * 150
      setTimeout(function () {
        Velocity(
          el,
          { opacity: 1, height: '1.6em' },
          { complete: done }
        )
      }, delay)
    },
    listTransitionLeave (el, done) {
      var delay = el.dataset.index * 150
      setTimeout(function () {
        Velocity(
          el,
          { opacity: 0, height: 0 },
          { complete: done }
        )
      }, delay)
    },
    async requestPredict () {
      if (!this.current.typhoon) return;
      if (this.predict.progress.t) {
        clearInterval(this.predict.progress.t)
        this.predict.progress.t = null
      }

      this.predict.confirm = false
      this.predict.progress.loading = true
      this.predict.progress.step = -1
      this.predict.progress.value = 0
      this.predict.progress.show = true
      
      let params = {
        typhoon_id: this.current.typhoon.typhoon_id,
        typhoon_radius: 100,
        user_id:this.$session.getUserId()
      }
      try {
        let tid = this.current.typhoon.typhoon_id        
        await this.overlays[tid].initLocation()
        await this.$http_ai.get('search_school',{params}).then(res => {
          this.getPathData()
          this.startScenario()
        })
        
      }
      catch (err) {
        this.$session.$emit('modal-alert', '예측데이터를 생성하지 못했습니다!')
        this.predict.progress.show = false
      }
      finally {
        this.predict.progress.loading = false
      }
    },
    startScenario () {
      console.log('step: ' + this.predict.progress.step)
      let max = this.current.typhoon.paths.length - 1
      let tid = this.current.typhoon.typhoon_id
      this.predict.progress.onPlay = true
      if (this.predict.progress.step < 0) {
        this.predict.progress.step = 0
        this.predict.progress.value = '0.0'
      }
      
      const nextStep = () => {
        this.onPathClickHandler(tid, this.predict.progress.step)
        if (this.predict.progress.step < max) {
          this.predict.progress.t = setTimeout(() => {
            this.predict.progress.step += 1
            this.predict.progress.value = (this.predict.progress.step / max * 100).toFixed(2)
            this.overlays[tid].animationTo(this.predict.progress.step, this.predict.progress.duration, nextStep.bind(this))
          }, 2000)
        }
        else {
          console.log('%c> SCENARIO ENDED', 'color:#0095de')
          this.stopScenario()
        }
      }
      console.log('%c> SCENARIO START', 'color:#0095de')
      nextStep()
    },
    pauseScenario () {
      if (!this.predict.progress.onPlay) return;
      let tid = this.current.typhoon.typhoon_id
      this.overlays[tid].animationPause()
      clearTimeout(this.predict.progress.t)
      this.predict.progress.onPlay = false
      this.predict.progress.show = false
      this.predict.progress.step -= 1
      console.log('%c> SCENARIO PAUSED', 'color:#0095de')

      if (this.current.typhoon.typhoon_v_type === 1) {
        this.current.typhoon.typhoon_v_type = 3
        console.log('%c> TEST TYPHOON CHANGE TYPE: 3', 'color:#0095de')
      }
    },
    stopScenario () {
      let tid = this.current.typhoon.typhoon_id
      this.overlays[tid].animationStop()
      clearTimeout(this.predict.progress.t)
      this.predict.progress.onPlay = false
      this.predict.progress.show = false
      this.predict.progress.step = 0
      this.predict.progress.value = '0.0'
      console.log('%c> SCENARIO STOPED', 'color:#0095de')

      if (this.current.typhoon.typhoon_v_type === 1) {
        this.current.typhoon.typhoon_v_type = 3
        console.log('%c> TEST TYPHOON CHANGE TYPE: 3', 'color:#0095de')
      }
    },
    resetScenario () {
      this.stopScenario()
      let tid = this.current.typhoon.typhoon_id
      this.onPathClickHandler(tid, 0)
    },
    viewPanel (key, value) {
      this.panels[key] = value
    },
    getSwitchTitle(){
      if(this.$session.hasPermission([5])){
        return '관내학교 확인하기'
      }else if(this.$session.hasPermission([6])){
        return '우리학교 확인하기'
      }
    }
  },
  computed: {
    currentTyphoonPaths () {
      if (!this.current.typhoon) return {}

      return this.current.typhoon.paths
      // if (this.current.typhoon.typhoon_v_type === 1) {
      //   return this.current.typhoon.paths.slice(0, this.predict.progress.step + 1)
      // }
      // else return this.current.typhoon.paths
    },
    chartDamageByRegion () {
      let groupByRegion = _.groupBy(this.tableData.items, 'area')
      let categories = Object.keys(groupByRegion)
      let values = []
      for (let key of categories) {
        let cost = Math.floor(groupByRegion[key].reduce((a, v) => a + v.total_cost, 0) / 1000000)
        values.push([
          groupByRegion[key].length,
          cost,
          numeral(cost).format('0,0')
        ])
      }

      let obj = {
        chart: {backgroundColor: 'transparent', type: 'column', height: 200},
        title: {text: null},
        credits: {enabled: false},
        legend: {enabled: false},
        xAxis: {categories},
        yAxis: {title:{enabled: false}, labels: {enabled: false}},
        tooltip: {
          pointFormat: '피해 학교 수 : {point.count}개교<br/>피해 금액 : {point.read}백만원'
        },
        plotOptions: {
          series: {
            keys: ['count', 'y', 'read']
          },
          showInLegend: true
        },
        series: [{
          data: values,
          name: '피해 금액',
          maxPointWidth: 10,
          dataLabels: {enabled: true, format: '{point.count:,f}'}
        }]
      }
      return obj
    },
    chartDamageByType () {
      let groupByType = _.groupBy(this.tableData.items, 'school_type')
      let values = Object.keys(groupByType).map(name => {
        let cost = groupByType[name].reduce((a, v) => a + v.total_cost, 0)
        return { name, y: groupByType[name].length, cost, costPrint: numeral(Math.floor(cost / 1000000)).format('0,0') }
      })

      let obj = {
        chart: {backgroundColor: 'transparent', type: 'pie', height: 400,width:300},
        plotOptions: {
          pie: {
            allowPointSelect: true,
            colors: ['#0f487f', '#346da4', '#5891c8', '#7cb5ec', '#a0d9ff', '#c4fdff'],
            dataLabels: {
              format: '{point.name}<br>{point.y}개교',
              distance: '10%',
              enabled: true,
              // filter: { property: 'percentage', operator: '>', value: 4 }
            },
            showInLegend: true
          },

        },
        title: {text: null},
        credits: {enabled: false},
        tooltip: {
          pointFormat: '피해 학교 수 : {point.y}개교<br/>피해 금액 : {point.costPrint}백만원'
        },
        series: [{
          data: values,
          name: '피해 학교 수',
          showInLegend: true,
          colorByPoint: true,
          dataLabels: {enabled: true, format: '{point.y:,f}'},
        }]
      }
      return obj
    },

  },
  mounted() {
    console.log('[M]')
  },
  beforeDestroy () {
    if (this.predict.progress.t) clearInterval(this.predict.progress.t)
  },
  data() {
    return {
      defLoad: false,
      mapView: false,
      kakaomap: {
        // appKey: 'fcd4fd0313991ddfaeb845ab6f480827',
        appKey: 'faea7c1211312bb306dc708fa0977848',
        center: {lat: 36.03619336254938, lng: 126.74274880533342},
        level: 12,
        mapTypeId: VueDaumMap.MapTypeId.NORMAL,
        libraries: ['clusterer'],
        map: null,
        clusterer: null,
        style: {
          width: '100%',
          height: '100%'
        }
      },
      navermap: {
        clientId: 'bzyk20jcxc', // X-NCP-APIGW-API-KEY-ID
        clientSecret: 'ccgG1CPWtG4iHb6PlGa9ynoMG5bV1NXNKtPP5vdZ' // X-NCP-APIGW-API-KEY
      },
      showMap: true,
      tableSelectedIndex: 0,
      summary: {
        cost: 0,
        count: 0,
        max: 0,
        avg: 0
      },
      tableData: {
        loading: false,
        headers: [
          { text: "태풍/학교명", value: "school_name", align: "left", width: 120, sortable: false },
          {
            text: "예상피해금액",
            value: "total_cost",
            align: "right",
            sortable: true
          }
        ],
        items: [],
        options: {
          sortBy: ['id'],
          sortDesc: [true],
          groupBy: [],
          groupDesc: [],
          itemsPerPage: 10,
          multiSort: false,
          mustSort: true,
          page: 1
        }
      },
      locations: [],
      paths: null,
      search: {
        show: false,
        type: "01",
        inp1: null,
        inp2: null,
        inp3: '',
        items1: [],
        items2: []
      },
      overlays: {},
      colors: [
        '#4572A7', '#AA4643', '#89A54E', '#80699B', '#3D96AE',
        '#DB843D', '#92A8CD', '#A47D7C', '#B5CA92'
      ],
      current: {
        show: false,
        typhoon: null,
        selectedPath: 0
      },
      predict: {
        confirm: false,
        progress: {
          show: false ,
          onPlay: false,
          loading: false,
          step: -1,
          value: 0,
          t: null,
          duration: 5000
        }
      },
      schooldetail: {
        show: false,
        data: null
      },
      panels: {
        paths: true,
        onpath: true,
        total: true,
      },
      ext_param:{
        school_include:false
      },
    }
  }
};
</script>

<style lang="scss" scoped>
  .sub-menu {
    min-width: 300px; }

  .result-panel-title{
    padding: 0px 0px 10px;
  }
  .result-panel-close{
    position: absolute;
    top: 15px;
    right: 10px;
  }

  .path-list-wrap{
    overflow-y: auto
  }

  .row-label > div{
    width: 120px;
  }

  .dashboard-top-10 {
    width: 100%;
    display: flex;
    justify-content: normal;
    align-items: center;
    margin-top: 20px;
    box-shadow: 0px 3px 1px -2px rgba(0, 0, 0, 0.2), 0px 2px 2px 0px rgba(0, 0, 0, 0.14), 0px 1px 5px 0px rgba(0, 0, 0, 0.12);

    .top-10-col{
      flex: 1 1 auto;
      margin: 0 10px;
    }

    .top-10-title{
      padding: 8px;
    }
  }

  .infopanel {
    width: 100%;
    height: 100%;
    color: white;
    background: rgba(0, 0, 0, 0.63);
    padding: 5px 6px;
    margin-bottom: 5px;
    border-radius: 3px;
    font-size: 11px;
    display: flex;
    align-items: center;

    > img{
      width: 20px;
      margin-right:8px;
    }

    .mdi{
      position: absolute;
      top: -10px;
      left: -10px;
    }

    > span{
      display: block;
      padding: 5px 0 0;
      vertical-align: middle;
      white-space: nowrap;
      text-overflow: ellipsis;
      overflow: hidden;
    }
  }
  .dev-loc{
    position: absolute;
    top: 5px;
    right: 40px;
    background-color: red;
    color: white;
    font-size: 10px;
    padding: 0 10px;
  }

  .dashboard-grid {
    max-width: 100%;
    width: 100%;
    box-sizing: border-box;
    display: flex;
    flex-wrap: wrap;

    .map-view & {
      .dashboard-top_left{
        display: none;
      }
      .dashboard-top_right{
        border: 1px solid white;
        height: 100%;
      }
    }
  }

  .dashboard-top_right {
    flex: 1 1 auto;
    z-index: 1;
    position: relative;
    height: 700px;

    .map-fullscreen {
      position: absolute;
      top: 5px;
      right: 5px;
      z-index: 100;
    }
  }

  .dashboard-bottom {
    margin-top: 20px;
    width: 100%;
    display: flex;
  }

  @supports( grid-area: auto ) {
    .dashboard-grid {
      display: grid;
      grid-template-rows: auto 510px;
      grid-template-columns: 400px auto;
      grid-row-gap: 20px;
      grid-column-gap: 20px;
      grid-template-areas: "filter map" "table table";
      width: 100%;

      .map-view & {
        grid-template-rows: 800px auto;
        grid-template-columns: 400px auto;
        grid-template-areas: "map map" "filter filter" "table table";
      }
    }
    .dashboard-top_left {
      grid-area: filter;

      .filter-wrap {
        width: 100%;
        height: 100%;
        border-radius: 5px;
        background-color: #eeeeee;
        overflow-y: auto;
      }
    }
    .dashboard-top_right {
      grid-area: map;
      z-index: 1;
      position: relative;

      .map-fullscreen{
        position: absolute;
        top: 5px;
        right: 5px;
        z-index: 100;
      }
    }
    .dashboard-bottom{
      grid-area: table;
      display: flex;
    }
  }
  .filter-panel{
    width: 90%;
    margin: 0 auto;
    padding: 15px 0;

    dt {
      border-bottom: 1px dashed #c3c3c3;
      color: #4e4e4e;
      font-size: 14px;
    }
  }

  .summary-row{
    display: flex;
    justify-content: space-between;
    padding: 6px 0 0;
    font-size: 0.875rem;
    color: #4e4e4e;
  }
  .search-btn{
    width: 80px;
  }

  .summary-table {
    width: 100%;

    &::v-deep {
      .v-data-footer {
        padding: 9px 8px;
      } 
      .v-data-footer__select {
        display: none;
      }
    }
  }
  .incident-table{
    width: 40%;
  }

  .list-enter-active, .list-leave-active {transition: all 1s}
  .list-enter, .list-leave-to, .list-leave-active{
    opacity: 0;
    transform: translateY(30px);
  }

  .incident-message{
    font-size: 0.875rem;
    flex: 0 1 auto;
  }
  .incident-time{
    font-size: 0.875rem;
    flex: 0 1 auto;
  }

  .new-item {
    font-weight: bold;
    .incident-message {
      color: #5f5f5f;
      &:before {
        content: "+";
        color: #64ce23;
      }
    }
  }

  .incident-name {
    color: #58a5bb;
    cursor: pointer;
  }

::v-deep {
  .map-info-box {
    &.status-1 {
      .status-dot {
        background-color:  #2fa1d2;
      }
      .status-info {
        border-color: #2fa1d2;
        background-color: #f0f7fa;
      }
    }
      
    &.status-2 {
      .status-dot {
        background-color: #c7c7c7;
      }
      .status-info {
        border-color: #c7c7c7;
        background-color: #fbfbfb;
        color: #afafaf;
      }
    }

    &.status-3 {
      .status-dot {
        background-color: #ff9e00;
      }
      .status-info {
        border-color: #ff9e00;
        background-color: #fbfbfb;
        color: #afafaf;
      }
    }
  }
    
  .status-dot {
    border-radius: 30px;
    width: 24px;
    height: 24px;
    border: 4px solid #ffffff;
  }
      
  .status-info {
    padding: 2px 8px;
    font-size: 12px;
    border-radius: 8px;
    box-shadow: 2px 6px 10px rgba(0,0,0,0.5);
    border-left-width: 12px;
    border-left-style: solid;
    border-color: #FF5722;
    background-color: #ffdfd5;
    cursor: pointer;
    user-select: none;
    transition: transform 0.2s;
    &:hover {
      transform: scale(1.4);
      z-index: 99;
    }
    .summary-detail {
      justify-content: space-between;
      align-items: center;
      font-size: 10px;
    }
  }
}

.show-map-summary::v-deep .map-info-box .summary-detail {
  display: flex;
}

.show-map-name::v-deep {
  .status-info {display: block}
  .status-dot {display: none}
}

.show-map-dot::v-deep {
  .map-info-box:hover
    .status-info{display: block}
    .status-dot{display: none;}
}

.dsh-func-btn{
  position: absolute;
  bottom: 15px;
  left: 50%;
  width: 1px;
  z-index: 99;
  overflow: visible;
  display: flex;
  justify-content: center;
  align-items: center;
  .dsh-func-btn-controls {
    background-color: rgba(0,0,0,0.7);
    padding: 0 24px;
    height: 54px;
    align-items: center;
    border-radius: 30px;
  }
}

.sw-func-btn{
  position: absolute;
  bottom: 30px;
  left: 18%;
  width: 200px;
  z-index: 99;
  overflow: visible;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0,0,0,0.3);
  border-radius: 30px;
  height: 30px;
  .dsh-func-btn-controls {
    background-color: rgba(0,0,0,0.7);
    padding: 0 24px;
    height: 54px;
    align-items: center;
    border-radius: 30px;
  }
}

.flip-list-move{
  transition: transform 1s}

.detail-view{
  position: fixed;
  top: 103px;
  right: 10px;
  z-index: 5;

  display: flex;
  align-items: flex-start;
}

.detail-view-2{
  position: fixed;
  top: 60px;
  right: 10px;
  z-index: 5;

  display: flex;
  align-items: flex-start;
}

.detail-view-path{
  width: 280px;
  height:690px;
}
.detail-view-path_2{
  width: 280px;
}

.detail-view-chart {
  width: 300px;
  margin-right: 10px;
}
.chart-label {
  display: inline-block;
  background-color: #c4fdff;
  padding: 0 6px;
}
.cursor-pointer {
  cursor: pointer;
}

.summary-view {
  width: 460px;
  margin-right: 10px;
}

.damaged-item {
  color: grey;
  &.high {
    color: orange;
    &.highest{color: red}
  }
}
.school-detail-container {
  position: relative;
}
.school-detail-close {
  position: absolute;
  top: 20px; right: 20px;
  z-index: 10;
}

</style>

<style lang="scss">
.sch-dot {
    opacity: 0;
    &.in-area { opacity: 1; }
    
}

.schl-info-box {
    position: absolute;
    top: -158px; left: 10px;
    padding: 10px;
    background-color: rgba(255,255,255,0.8);
    box-shadow: 0px 0px 4px rgba(0,0,0,0.2);
    z-index: 5;
    cursor: default;

    display: flex;

    .schl-icon {
        margin-top: -20px;
        z-index: 0;
        cursor: pointer;
    }
    .schl-icon:hover + .schl-info-box {
        display: block;
    }
    .schl-title {
        font-size: 16px;
    }
    .schl-info-cont {
        flex: 1 0 auto;
        padding-right: 20px;
    }
    .schl-img-cont {
        flex: 0 1 auto;
    }
    .schl-item {
        font-size: 10px;
        color: #7a7a7a;
    }
}
.cost_color_1 {color:#03a9f4}
.cost_color_2 {color:#aeea00}
.cost_color_3 {color:#ffff00}
.cost_color_4 {color:#ff9800}
.cost_color_5 {color:#ff0000}

.cost_color_1_ {background-color:#03a9f4;font-size: 10px;width: 60px;}
.cost_color_2_ {background-color:#aeea00;font-size: 10px;width: 60px;}
.cost_color_3_ {background-color:#ffff00;font-size: 10px;width: 60px;}
.cost_color_4_ {background-color:#ff9800;font-size: 10px;width: 60px;}
.cost_color_5_ {background-color:#ff0000;font-size: 10px;width: 60px;}
.no-m{
  background-color: skyblue;
  text-align: center;
  margin: 0 0px;
  border: 0px;
  width: 280px;
}
</style>
