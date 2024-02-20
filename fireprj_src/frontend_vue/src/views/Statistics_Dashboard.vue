<template>
  <main-layout>
    <template v-slot>
      <div class="main-panel">
        <v-toolbar dark flat color="light-blue darken-4">
          <v-toolbar-title>태풍 피해 통계 현황</v-toolbar-title>
          <v-spacer></v-spacer>
          <template v-slot:extension>
            <v-tabs v-model="selected_tab_item" align-with-title slider-size="6">
              <v-tabs-slider color="yellow"></v-tabs-slider>
              <v-tab
                v-for="item in type_tab_items"
                :key="item"
                @change="change_tab_item(item)">
                {{ item }}
              </v-tab>
            </v-tabs>
          </template>
        </v-toolbar>

        <v-tabs-items v-model="selected_tab_item">
          <v-tab-item
              v-for="type_item in type_tab_items"
              :key="type_item">
            <v-card flat>
              <br>

              <v-container fluid class="data-table-container">
                <div class="d-flex justify-space-between mb-4">
                  <div class="flex-grow-1 d-flex align-center">
                    <div class="filter-label">연도별</div>
                    <div class="filter-year">
                      <v-select outlined dense hide-details light
                        v-model="search.yearFrom"
                        :items="search.yearlist"
                        class="flex-grow-0"
                        item-text="name"
                        item-value="code"
                        @change="onChangeYearRange()"
                      />
                    </div>
                    <div class="filter-divider"><pre>  ~</pre></div>
                    <div class="filter-year">
                      <v-select outlined dense hide-details light
                        v-model="search.yearTo"
                        :items="search.yearlist"
                        class="flex-grow-0"
                        item-text="name"
                        item-value="code"
                        @change="onChangeYearRange()"
                      />
                    </div>
                    <v-divider vertical class="ml-6 mr-2"/>
                    <div class="filter-label">태풍별</div>
                    <div class="filter-typhoon">
                      <v-select dense hide-details outlined light multiple
                        v-model="search.typhoons"
                        :items="meta.typhoons"
                        placeholder="태풍"
                        item-text="typhoon_name"
                        item-value="id">
                        <template v-slot:prepend-item>
                          <v-list-item
                              ripple
                              @click="onChangeTyphoons"
                          >
                            <v-list-item-action>
                              <v-icon v-if="search.typhoons.length === meta.typhoons.length " color="primary">
                                mdi-checkbox-marked
                              </v-icon>
                              <v-icon v-else>
                                mdi-checkbox-blank-outline
                              </v-icon>
                            </v-list-item-action>
                            <v-list-item-content>
                              <v-list-item-title>
                                전체
                              </v-list-item-title>
                            </v-list-item-content>
                          </v-list-item>
                          <v-divider class="mt-2"></v-divider>
                        </template>
                        <template v-slot:selection="{item, index}">
                          <template v-if="index === 0">{{item.typhoon_name}}</template>
                          <span class="grey--text text-caption ml-2" v-if="index === 1">{{search.typhoons.length}}개 선택</span>
                        </template>
                      </v-select>
                    </div>
                    <v-divider vertical class="ml-6 mr-2"/>
                    <div class="filter-label">지역별</div>
                    <div class="filter-region">
                      <v-select dense hide-details outlined light return-object multiple
                        v-model="search.regions"
                        :items="meta.regions"
                        placeholder="지역">
                        <template v-slot:prepend-item>
                          <v-list-item
                              ripple
                              @click="onChangeRegions"
                          >
                            <v-list-item-action>
                              <v-icon v-if="search.regions.length === meta.regions.length " color="primary">
                                mdi-checkbox-marked
                              </v-icon>
                              <v-icon v-else>
                                mdi-checkbox-blank-outline
                              </v-icon>
                            </v-list-item-action>
                            <v-list-item-content>
                              <v-list-item-title>
                                전체
                              </v-list-item-title>
                            </v-list-item-content>
                          </v-list-item>
                          <v-divider class="mt-2"></v-divider>
                        </template>

                        <template v-slot:selection="{item, index}">
                          <template v-if="index === 0">{{item.text}}</template>
                          <span class="grey--text text-caption ml-2" v-if="index === 1">{{search.regions.length}}개 선택</span>
                        </template>
                      </v-select>
                    </div>
                  </div>
                  <div>
                    <v-btn color="primary" @click="submitHandler"><div class="px-8">검색</div></v-btn>
                  </div>
                </div>
                <template v-if="search.description">
                  <!-- <div class="mt-8 mb-2" v-html="search.description"></div> -->
                  <v-row>
                    <v-col cols="6">
                      <v-card light outlined color="white">
                        <v-card-title class="body-1 font-weight-bold py-2">연도별 교육시설 피해 현황</v-card-title>
                        <v-divider/>
                        <v-card-text>
                          <highcharts
                            constructor-type="chart"
                            :options="chart1Option"
                          />
                        </v-card-text>
                      </v-card>
                    </v-col>
                    <v-col cols="6">
                      <v-card light outlined color="white">
                        <v-card-title class="body-1 font-weight-bold py-2">지역별 교육시설 피해 현황</v-card-title>
                        <v-divider/>
                        <v-card-text>
                          <highcharts
                            constructor-type="chart"
                            :options="chart5Option"
                          />
                        </v-card-text>
                      </v-card>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12">
                      <v-card light outlined color="white">
                        <v-card-title class="body-1 font-weight-bold py-2">태풍별 교육시설 피해 현황</v-card-title>
                        <v-divider/>
                        <v-card-text>
                          <highcharts
                            constructor-type="chart"
                            :options="chart2Option"
                          />
                        </v-card-text>
                      </v-card>
                    </v-col>
                  </v-row>

                  <v-row>
                    <v-col cols="6">
                      <v-card light outlined color="white" >
                        <v-card-title class="body-1 font-weight-bold py-2">설립별 교육시설 피해 현황</v-card-title>
                        <v-divider/>
                        <v-card-text>
                          <highcharts
                              constructor-type="chart"
                              :options="chart6Option"
                          />
                        </v-card-text>
                      </v-card>
                    </v-col>
                    <v-col cols="6">
                      <v-card light outlined color="white">
                        <v-card-title class="body-1 font-weight-bold py-2">학교급별 교육시설 피해 현황</v-card-title>
                        <v-divider/>
                        <v-card-text>
                          <highcharts
                              constructor-type="chart"
                              :options="chart7Option"
                          />
                        </v-card-text>
                      </v-card>
                    </v-col>
                  </v-row>
<!--                  <div>-->
<!--                    <v-btn elevation="1" color="secondary" small class="report-download" @click="saveToPDF()">-->
<!--                      <v-icon>mdi-cloud-download</v-icon><span>보고서 다운로드</span>-->
<!--                    </v-btn>-->
<!--                  </div>-->
<!--                  <abl-document style="width: 1480px" class="abl-page"  ref="report">-->
<!--                    <div class="abl-doc-title">-->
<!--                      <div class="title-text">태풍 피해 상세결과 보고서</div>-->
<!--                    </div>-->
<!--                    <div class="abl-doc-body">-->
<!--                      <table class="abl-table-ts" >-->
<!--                        <colgroup>-->
<!--                          <col style="width:7.1%"/>-->
<!--                          <col style="width:7.1%"/>-->
<!--                          <col style="width:7.1%"/>-->
<!--                          <col style="width:7.1%"/>-->
<!--                          <col style="width:7.1%"/>-->
<!--                          <col style="width:7.1%"/>-->
<!--                          <col style="width:7.1%"/>-->
<!--                          <col style="width:7.1%"/>-->
<!--                          <col style="width:7.1%"/>-->
<!--                          <col style="width:7.1%"/>-->
<!--                          <col style="width:7.1%"/>-->
<!--                          <col style="width:7.1%"/>-->
<!--                          <col style="width:7.1%"/>-->
<!--                          <col style="width:7.1%"/>-->
<!--                        </colgroup>-->
<!--                        <tr>-->
<!--                          <th colspan="2" rowspan="2"><pre> </pre></th>-->
<!--                          <th colspan="2" rowspan="1">2016</th>-->
<!--                          <th colspan="2" rowspan="1">2017</th>-->
<!--                          <th colspan="2" rowspan="1">2018</th>-->
<!--                          <th colspan="2" rowspan="1">2019</th>-->
<!--                          <th colspan="2" rowspan="1">2020</th>-->
<!--                          <th colspan="2" rowspan="1">합계</th>-->
<!--                        </tr>-->
<!--                        <tr>-->
<!--                          <th colspan="1" rowspan="1">피해 학교 수</th>-->
<!--                          <th colspan="1" rowspan="1">지급액<br>(백만원)</th>-->
<!--                          <th colspan="1" rowspan="1">피해 학교 수</th>-->
<!--                          <th colspan="1" rowspan="1">지급액<br>(백만원)</th>-->
<!--                          <th colspan="1" rowspan="1">피해 학교 수</th>-->
<!--                          <th colspan="1" rowspan="1">지급액<br>(백만원)</th>-->
<!--                          <th colspan="1" rowspan="1">피해 학교 수</th>-->
<!--                          <th colspan="1" rowspan="1">지급액<br>(백만원)</th>-->
<!--                          <th colspan="1" rowspan="1">피해 학교 수</th>-->
<!--                          <th colspan="1" rowspan="1">지급액<br>(백만원)</th>-->
<!--                          <th colspan="1" rowspan="1">피해 학교 수</th>-->
<!--                          <th colspan="1" rowspan="1">지급액<br>(백만원)</th>-->
<!--                        </tr>-->
<!--                        <tr :class="{'tr-c': index == 0}" v-for="(item,index) in data.by_area_detail" :key="index">-->
<!--                          <th colspan="2" >{{item.area_name}}</th>-->
<!--                          <td colspan="1" >{{item.count_2016}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_2016/1000000)|makeComma}}</td>-->
<!--                          <td colspan="1" >{{item.count_2017}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_2017/1000000)|makeComma}}</td>-->
<!--                          <td colspan="1" >{{item.count_2018}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_2018/1000000)|makeComma}}</td>-->
<!--                          <td colspan="1" >{{item.count_2019}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_2019/1000000)|makeComma}}</td>-->
<!--                          <td colspan="1" >{{item.count_2020}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_2020/1000000)|makeComma}}</td>-->
<!--                          <td colspan="1" >{{item.count_sum}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_sum/1000000)|makeComma}}</td>-->
<!--                        </tr>-->
<!--                        <tr :class="{'tr-c': index == 0}" v-for="(item,index) in data.by_typhoon_detail" :key="'a' + index">-->
<!--                          <th colspan="2" >{{item.typhoon_name}}</th>-->
<!--                          <td colspan="1" >{{item.count_2016}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_2016/1000000)|makeComma}}</td>-->
<!--                          <td colspan="1" >{{item.count_2017}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_2017/1000000)|makeComma}}</td>-->
<!--                          <td colspan="1" >{{item.count_2018}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_2018/1000000)|makeComma}}</td>-->
<!--                          <td colspan="1" >{{item.count_2019}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_2019/1000000)|makeComma}}</td>-->
<!--                          <td colspan="1" >{{item.count_2020}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_2020/1000000)|makeComma}}</td>-->
<!--                          <td colspan="1" >{{item.count_sum}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_sum/1000000)|makeComma}}</td>-->
<!--                        </tr>-->
<!--                        <tr :class="{'tr-c': index == 0}" v-for="(item,index) in data.by_establish_detail" :key="'b' + index">-->
<!--                          <th colspan="2" >{{item.establish_gubun_name}}</th>-->
<!--                          <td colspan="1" >{{item.count_2016}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_2016/1000000)|makeComma}}</td>-->
<!--                          <td colspan="1" >{{item.count_2017}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_2017/1000000)|makeComma}}</td>-->
<!--                          <td colspan="1" >{{item.count_2018}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_2018/1000000)|makeComma}}</td>-->
<!--                          <td colspan="1" >{{item.count_2019}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_2019/1000000)|makeComma}}</td>-->
<!--                          <td colspan="1" >{{item.count_2020}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_2020/1000000)|makeComma}}</td>-->
<!--                          <td colspan="1" >{{item.count_sum}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_sum/1000000)|makeComma}}</td>-->
<!--                        </tr>-->
<!--                        <tr :class="{'tr-c': index == 0}" v-for="(item,index) in data.by_scool_type_detail" :key="'c' + index">-->
<!--                          <th colspan="2" >{{item.school_type}}</th>-->
<!--                          <td colspan="1" >{{item.count_2016}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_2016/1000000)|makeComma}}</td>-->
<!--                          <td colspan="1" >{{item.count_2017}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_2017/1000000)|makeComma}}</td>-->
<!--                          <td colspan="1" >{{item.count_2018}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_2018/1000000)|makeComma}}</td>-->
<!--                          <td colspan="1" >{{item.count_2019}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_2019/1000000)|makeComma}}</td>-->
<!--                          <td colspan="1" >{{item.count_2020}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_2020/1000000)|makeComma}}</td>-->
<!--                          <td colspan="1" >{{item.count_sum}}</td>-->
<!--                          <td colspan="1" >{{Math.trunc(item.cost_sum/1000000)|makeComma}}</td>-->
<!--                        </tr>-->
<!--                        <tr class="tr-c">-->
<!--                          <th colspan="2" >{{data.by_total_detail.name}}</th>-->
<!--                          <th colspan="1" >{{data.by_total_detail.count_2016}}</th>-->
<!--                          <th colspan="1" >{{Math.trunc(data.by_total_detail.cost_2016/1000000)|makeComma}}</th>-->
<!--                          <th colspan="1" >{{data.by_total_detail.count_2017}}</th>-->
<!--                          <th colspan="1" >{{Math.trunc(data.by_total_detail.cost_2017/1000000)|makeComma}}</th>-->
<!--                          <th colspan="1" >{{data.by_total_detail.count_2018}}</th>-->
<!--                          <th colspan="1" >{{Math.trunc(data.by_total_detail.cost_2018/1000000)|makeComma}}</th>-->
<!--                          <th colspan="1" >{{data.by_total_detail.count_2019}}</th>-->
<!--                          <th colspan="1" >{{Math.trunc(data.by_total_detail.cost_2019/1000000)|makeComma}}</th>-->
<!--                          <th colspan="1" >{{data.by_total_detail.count_2020}}</th>-->
<!--                          <th colspan="1" >{{Math.trunc(data.by_total_detail.cost_2020/1000000)|makeComma}}</th>-->
<!--                          <th colspan="1" >{{data.by_total_detail.count_sum}}</th>-->
<!--                          <th colspan="1" >{{Math.trunc(data.by_total_detail.cost_sum/1000000)|makeComma}}</th>-->
<!--                        </tr>-->
<!--                      </table>-->
<!--                    </div>-->
<!--                  </abl-document>-->

                </template>
                <v-alert v-else text type="info" class="mt-4">
                  검색 조건을 선택해주세요
                </v-alert>
              </v-container>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
      </div>
    </template>
  </main-layout>
</template>

<script>
import _ from 'lodash'
import moment from 'moment'
// import AblDocument from '@/components/AblDocument'
import {jsPDF} from "jspdf";
const chartOptions = {
  chart: { zoomType: 'xy' },
  title: { text: null },
  colors: ['skyblue', 'orange'],
  xAxis: [{ categories: [], crosshair: true }],
  yAxis: [
    {
      labels: {format: '{value:,f}백만원'},
      title: {text: '공제급여 지급액'}
    },
    {
      title: {text: '피해학교수'},
      labels: {format: '{value:,f}개교'},
      opposite: true
    }
  ],
  credits: {enabled: false},
  tooltip: {shared: true, crosshair: true},
  series: [
    {
      type: 'column',
      yAxis: 1,
      pointWidth: 20,
      data: [],
      dataLabels: {enabled: true, format: '{point.y:,f}개교'},
      tooltip: {valueSuffix: '개교'}
    }, 
    {
      type: 'line',
      data: [],
      dataLabels: {enabled: true, format: '{point.y:,f}백만원'},
      tooltip: {valueSuffix: '백만원'}
    }
  ]
}

const pieOptions = {
  colors: ['#003f5c', '#58508d','#bc5090', '#ff6361', '#ffa600','#aa3f5c', '#aa508d','#aa5090', '#aa6361', '#aaa600'],
  chart: {
    plotBackgroundColor: null,
    plotBorderWidth: null,
    plotShadow: false,
    type: 'pie'
  },
  title: {
    text: ''
  },
  tooltip: {
    pointFormat: '<b>{point.name2}</b>: {point.y} 백만원'
  },
  accessibility: {
    point: {
      valueSuffix: '%'
    }
  },
  plotOptions: {
    pie: {
      allowPointSelect: true,
      cursor: 'pointer',
      dataLabels: {
        enabled: true,
        format: '<b>{point.name1}</b>: {point.y} 개교 '
      },
      showInLegend: true
    }
  },
  series: [{
    name: 'Brands',
    colorByPoint: true,
    data: []
  }],
}

export default {
  props: {
    fstatus: { type: [Number, String], default: 0 }
  },
  // components: {AblDocument},
  methods: {
    async getMetaData () {
      let params = {type: '01',fk_user_id:this.$session.getUserIndex()}
      let {data} = await this.$http.get('dashboard/filter', {params})
      this.search.yearlist = data
      this.search.year = this.search.yearlist[0]
      this.search.yearFrom = this.search.yearlist[4]
      this.search.yearTo = this.search.yearlist[0]
      this.search.regions = this.meta.regions
      this.onChangeYearRange()
    },
    async getTyphoonList () {
      let filters = []
      filters.push({name: 'typhoon_v_type', op: 'eq', val: 0})
      filters.push({name: 'typhoon_start_date', op: 'gte', val: `${this.search.yearFrom}-01-01 00:00:00`})
      filters.push({name: 'typhoon_start_date', op: 'lte', val: `${this.search.yearTo}-12-31 23:59:59`})
      let q = JSON.stringify({filters})
      let params = {q}
      let {data} = await this.$http.get('typhoons', {params})
      this.meta.typhoons = data.objects
      this.search.typhoons = data.objects.map(v => v.id)
    },
    async submitHandler () {
      this.loading = true
      try {
        let params = {}
        // if (this.search.school_type) params.school_type = this.search.school_type
        // if (this.search.region) params.area = this.search.region.value

        if (this.search.yearFrom) params.year_from = this.search.yearFrom
        if (this.search.yearTo) params.year_to = this.search.yearTo
        params.areas = ''
        if (this.search.regions) this.search.regions.map(v => params.areas += v.value + ',')
        params.typhoons = ''
        if (this.search.typhoons) this.search.typhoons.map(v => params.typhoons += v + ',')
        let stats = await this.$http.get('report/stats', {params})
        // let top10 = await this.$http.get('report/top10', {params})

        // let currstats = stats.data[`summary_${this.search.year}`]
        // currstats.acci_cost = parseInt(currstats.acci_cost, 10)
        // currstats.school_cnt = parseInt(currstats.school_cnt, 10)
        // currstats.tp_cnt = parseInt(currstats.tp_cnt, 10)
        //
        // Object.assign(this.summary, currstats)
        // this.data.area = stats.data.area_data
        // this.data.tp = stats.data.tp_data
        // this.data.top10_areas = top10.data.top10_areas
        // this.data.top10_schools = top10.data.top10_schools

        // 추가
        this.data.by_region = stats.data.by_region
        this.data.by_year = stats.data.by_year
        this.data.by_typhoon = stats.data.by_typhoons
        this.data.by_establish = stats.data.by_establish
        this.data.by_school_type = stats.data.by_school_type
        // this.data.by_area_detail = stats.data.by_area_detail
        // this.data.by_typhoon_detail = stats.data.by_typhoon_detail
        // this.data.by_establish_detail = stats.data.by_establish_detail
        // this.data.by_scool_type_detail = stats.data.by_scool_type_detail
        // this.data.by_total_detail = stats.data.by_total_detail

        this.data.years = []
        for (let key in stats.data) {
          if (key.startsWith('summary_')) {
            this.data.years.push({
              year: parseInt(key.replace('summary_', ''), 10),
              acci_cost: parseInt(stats.data[key].acci_cost, 10),
              school_cnt: parseInt(stats.data[key].school_cnt, 10),
              tp_cnt: parseInt(stats.data[key].tp_cnt, 10)
            })
          }
        }
        
        let msg = `<span class="font-weight-bold blue--text">${this.search.year}</span>년도에 발생한 태풍에 의한`
        if (this.search.region) msg += ` <span class="font-weight-bold blue--text">${this.search.region.text}</span> 지역의`
        if (this.search.school_type) msg += ` <span class="font-weight-bold blue--text">${this.search.school_type}</span>`
        msg += ' 피해에 대한 통계입니다.'
        this.search.description = msg
        this.search.count += 1
      }
      catch (err) {
        console.error(err)
      }
      finally {
        this.loading = false
      }
    },
    change_tab_item(item){
      this.getMetaData()
      this.submitHandler()
    },
    onChangeYearRange () {
      if (this.search.yearFrom && this.search.yearTo) this.getTyphoonList()
    },
    async capture (width,height) {
      if (this.$refs['report']) {
        const report = this.$refs['report'].length ?  this.$refs['report'][0] : this.$refs['report']
        let blob = await report.capture(width,height)
        return blob
      }
      else return null
    },
    async saveToPDF () {
      // if(this.$session.hasPermission([5,6])){
      //   if(this.$session.hasPermission([5]) && this.$session.getUserId() != this.school.mem_num){
      //     this.$session.$emit('modal-alert', "권한이 없습니다.")
      //     return
      //   }
      //   if(this.$session.hasPermission([6]) && this.$session.getUserId() != this.school.school_number){
      //     this.$session.$emit('modal-alert', "권한이 없습니다.")
      //     return
      //   }
      // }
      let title ='상세피해내역보고서.pdf'
      const doc = new jsPDF({orientation: 'l', unit: 'mm', format: 'a4'})
      let image_data = await this.capture(1530,1100)
      const imgProps= doc.getImageProperties(image_data);
      const pdfWidth = doc.internal.pageSize.getWidth();
      const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
      //alert("pdfWidth :" + doc.internal.pageSize.getWidth() + ",pdfHeight" + doc.internal.pageSize.getHeight())
      //297,210

      // alert("pdfWidth :" + imgProps.width + ",pdfHeight" + imgProps.height)
      //const pdfHeight = 280;
      doc.addImage(image_data, 'png', 4, 0, pdfWidth, pdfHeight)
      doc.save(title)
    },
    onChangeRegions(){
      this.$nextTick(() => {
        if (this.search.regions.length === this.meta.regions.length ) {
          this.search.regions= []
        } else {
          this.search.regions = this.meta.regions.slice()
        }
      })
    },
    onChangeTyphoons(){
      this.$nextTick(() => {
        if (this.search.typhoons.length === this.meta.typhoons.length ) {
          this.search.typhoons= []
        } else {
          this.search.typhoons = this.meta.typhoons.slice()
        }
      })
    }
  },
  computed: {
    chart1Option () {
      let obj = _.cloneDeep(chartOptions)
      obj.chart.type = 'line'
      obj.xAxis[0].categories = this.data.by_year.map(v => v.year)
      obj.series[0].data = this.data.by_year.map(v => v.count)
      obj.series[0].name = '피해학교수'
      obj.series[1].data = this.data.by_year.map(v => (Math.floor(v.cost/1000000)))
      obj.series[1].name = '공제급여 지급액'

      return obj
    },
    chart2Option () {
      let obj = _.cloneDeep(chartOptions)
      obj.chart.type = 'line'
      obj.xAxis[0].categories = this.data.by_typhoon.map(v => v.typhoon)
      obj.series[0].data = this.data.by_typhoon.map(v => v.count)
      obj.series[0].name = '피해학교수'
      obj.series[1].data = this.data.by_typhoon.map(v => (Math.floor(v.cost/1000000)))
      obj.series[1].name = '공제급여 지급액'

      return obj
    },
    chart5Option () {
      let obj = _.cloneDeep(chartOptions)
      obj.chart.type = 'line'
      obj.xAxis[0].categories = this.data.by_region.map(v => v.area)
      obj.series[0].data = this.data.by_region.map(v => v.count)
      obj.series[0].name = '피해학교수'
      obj.series[1].data = this.data.by_region.map(v => (Math.floor(v.cost/1000000)))
      obj.series[1].name = '공제급여 지급액'
      return obj
    },
    chart6Option () {
      let obj = _.cloneDeep(pieOptions)
      obj.series[0].data = this.data.by_establish.map(v => ({name:v.establish_gubun_name,name1:v.establish_gubun_name,name2:'피해지급액',y:parseInt(v.count),z:(Math.floor(v.cost/1000000))}))
      obj.series[0].name = '피해학교수' + this.search.count
      return obj
    },
    chart7Option () {
      let obj = _.cloneDeep(pieOptions)
      obj.series[0].data = this.data.by_school_type.map(v => ({name:v.school_type,name1:v.school_type,name2:'피해지급액',y:parseInt(v.count),z:(Math.floor(v.cost/1000000))}))
      obj.series[0].name = '피해학교수' + this.search.count
      return obj
    }
  },
  watch: {
    fstatus () {
      console.log('fstatus: ' + this.fstatus)
      this.selected_tab_item = this.fstatus
    }
  },
  mounted () {
    this.getMetaData()
    // this.submitHandler()
    this.selected_tab_item = this.fstatus
  },
  data () {
    return {
      headers: [
        { text: 'Col1', value: 'calories' },
        { text: 'Col2', value: 'calories' },
        { text: 'Col3', value: 'calories' },
        { text: 'Col4', value: 'calories' },
        { text: 'Col5', value: 'calories' }
      ],
      loading: false,
      items: [],

      search: {
        yearFrom: moment().format('YYYY'),
        yearTo: moment().format('YYYY'),
        regions: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
        typhoons: [],

        year: moment().format('YYYY'),
        school_type: null,
        region: null,
        yearlist: [],
        description: null,
        count:0
      },

      summary: {
        school_cnt: 0,
        acci_cost: 0,
        tp_cnt: 0
      },

      data: {
        area: [],
        tp: [],
        top10_areas: [],
        top10_schools: [],
        years: [],
        by_typhoon: [],
        by_year: [],
        by_region: []
      },

      meta: {
        schoolTypes: [
          {value: null, text: '전체'},
          {value: '고등학교', text: '고등학교'},
          {value: '교육지원청', text: '교육지원청'},
          {value: '교육청', text: '교육청'},
          {value: '기타', text: '기타'},
          {value: '대학', text: '대학'},
          {value: '대학원', text: '대학원'},
          {value: '도서관', text: '도서관'},
          {value: '연구기관', text: '연구기관'},
          {value: '유치원(단/병)', text: '유치원(단/병)'},
          {value: '전문대학', text: '전문대학'},
          {value: '전시장', text: '전시장'},
          {value: '중학교', text: '중학교'},
          {value: '진흥원·교육연수원·수련시설', text: '진흥원·교육연수원·수련시설'},
          {value: '체육시설', text: '체육시설'},
          {value: '초등학교', text: '초등학교'},
          {value: '특수학교', text: '특수학교'},
          {value: '평생교육기관', text: '평생교육기관'}
        ],
        regions: [
          {value: 1, text: '강원'},
          {value: 2, text: '경기'},
          {value: 3, text: '경남'},
          {value: 4, text: '경북'},
          {value: 5, text: '광주'},
          {value: 6, text: '대구'},
          {value: 7, text: '대전'},
          {value: 8, text: '부산'},
          {value: 9, text: '서울'},
          {value: 10, text: '세종'},
          {value: 11, text: '울산'},
          {value: 12, text: '인천'},
          {value: 13, text: '전남'},
          {value: 14, text: '전북'},
          {value: 15, text: '제주'},
          {value: 16, text: '충남'},
          {value: 17, text: '충북'}
        ],
        typhoons: []
      },
      selected_tab_item: null,
      // type_tab_items: ['지역별 통계 현황','태풍별 통계 현황','설립별 통계 현황','학교급별 통계 현황','피해유형별 통계 현황','세부피해부분별 통계 현황'],
      type_tab_items: [''],
      refresh_id:0
    }
  }
}
</script>

<style lang="scss" scoped>
.main-panel {
  padding: 10px;
  height: calc(100vh - 80px);
  overflow-y: auto;
}

.summary-content {
  height: 100px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.data-table-container {
  // overflow-y: auto;
  // height: calc(100vh - 200px);
}

.filter-label {
  padding: 0 10px;
}
.filter-year {
  width: 100px;
}
.filter-typhoon {
  width: 280px;
}
.filter-region {
  width: 200px;
}
.filter-divider {
  padding: 0 10px;
}
.flex-grow-0{
  margin-left:10px;
  margin-bottom: 10px;
  margin-top: 7px;
  width:200px;
}
.abl-doc-body{
  width: 1480px;
}
.abl-page{
  width: 1000px;
}
.abl-doc-title {
  width:1480px;
  position: relative;
  padding: 15px 0 10px;
  text-align: center;
  .tmpl-no {
    position: absolute;
    top: 2px; left: 2px;
  }
  .tmpl-no-1 {
    position: absolute;
    top: 2px; left: 2px;
    text-align: center;
  }
  .title-text {
    font-size: 24px;
    border-collapse: collapse;
    border-bottom: 2px solid #a0a0a0;
    font-weight: normal;
    text-align: center;
    color: black;
  }
}
.abl-table-ts {
  width: 100%;
  border-collapse: collapse;
  border-top: 1.5px solid #333333;
  border-bottom: 1.5px solid #333333;
  tr {
    border-bottom: 1px solid #333333;
    height: 20px;
  }
  th {
    padding: 0px 0px;
    background-color: #bbbbbb;
    border: 1px solid #a0a0a0;
    font-weight: normal;
  }
  td {
    padding: 0px 0px;
    border: 1px solid #a0a0a0;
    text-align: center;
  }
  .m-h { background-color: #ebebeb; }
  .s-h { background-color: #ebebeb;}
  .w-h { background-color: #ffffff; }
  .dbl-t { border-top: 3px double #a0a0a0; }
  .dbl-b { border-bottom: 3px double #a0a0a0; }
  .area-a { width: 80% !important;}
  .textarea-context {
    display: flex;
    min-height: 280px;
  }
  .s-h-1 {float:left;background-color: #ebebeb;border-right: 1px solid #a0a0a0;width:50%;height:200px!important;line-height: 30px;padding-top: 65px;}
  .s-h-2 {float:right;background-color: #ebebeb;border-bottom: 1px solid #a0a0a0;width:50%;height:100px!important;line-height: 30px;}
  .s-h-3-1 {background-color: #ebebeb;border-bottom: 1px solid #a0a0a0;width:100%;height:100%!important;}
  .s-h-3-2 {background-color: #ebebeb;width:100%;height:100%!important;}
  .s-h-4 {float:left;background-color: white;border-right: 1px solid #a0a0a0;width:50%;height:240px!important;}
  .s-h-4-0 {float:left;background-color: white;border-right: 0px solid #a0a0a0;width:50%;height:240px!important;}
  .s-h-4-1 {background-color: white;border-bottom: 1px solid #a0a0a0;width:100%;height:30px!important;}
  .s-h-4-2 {background-color: white;border-bottom: 0px solid #a0a0a0;width:100%;height:60px!important;}
  .tr-c{
    //border-bottom: 2px solid black;
    border-top: 1.3px solid black;
  }
}
.report-download {
  position: relative;
  top: 40px; left:1330px;
  z-index: 10;
}
</style>
