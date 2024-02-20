<template>
    <div class="typ" :class="{focused, instep: step.n >= 0}" :style="styles">
        <svg class="typ-icon" @click="onClickHandler" :fill="color" :width="size" :height="size" viewBox="0 0 100 100" y="0px" x="0px">
            <path 
                id="path2"
                d="m 40.1,76 c 1,-0.2 2,-0.4 3,-0.6 -0.7,2.5 -2,4.8 -3.9,6.8 C 33.4,88 24,88.1 18,82.5 29.8,94 48.9,93.9 60.6,82.2 c 3.9,-3.9 6.5,-8.6 7.8,-13.6 1.8,1.8 3.2,4.1 3.9,6.8 2.1,8 -2.5,16.2 -10.4,18.5 16,-4.5 25.4,-21 21.1,-37.1 -1.4,-5.3 -4.2,-9.9 -7.8,-13.6 0.7,-0.2 1.3,-0.3 2,-0.4 0.1,0 0.2,0 0.3,0 0.1,0 0.2,0 0.3,0 0.8,-0.1 1.6,-0.1 2.5,0 0.2,0 0.5,0 0.7,0.1 0.1,0 0.2,0 0.3,0 0.1,0 0.1,0 0.2,0 0.5,0.1 1,0.2 1.5,0.3 8.1,2.2 12.9,10.3 10.9,18.2 0,-0.1 0.1,-0.3 0.1,-0.4 0,0.1 -0.1,0.3 -0.1,0.4 C 98,45.3 88.4,28.9 72.3,24.6 c -0.7,-0.2 -1.4,-0.3 -2,-0.5 -1.1,-0.2 -2.3,-0.4 -3.4,-0.5 -1.6,-0.1 -3.1,-0.1 -4.6,0 -0.5,0 -1,0.1 -1.4,0.1 -0.2,0 -0.4,0 -0.5,0.1 -1.2,0.2 -2.5,0.4 -3.7,0.7 0.7,-2.5 2,-4.8 3.9,-6.8 C 66.5,12 75.9,11.9 81.8,17.6 70,6 50.9,6.1 39.2,17.8 35.3,21.7 32.7,26.4 31.4,31.4 29.6,29.6 28.2,27.3 27.5,24.6 25.4,16.6 30,8.4 37.9,6.1 c -16,4.5 -25.4,21 -21.1,37.1 1.4,5.3 4.2,9.9 7.8,13.6 -0.4,0.1 -0.8,0.2 -1.2,0.3 -0.1,0 -0.2,0 -0.2,0 -0.2,0 -0.3,0.1 -0.5,0.1 -0.2,0 -0.4,0.1 -0.7,0.1 -0.8,0.1 -1.6,0.1 -2.5,0 -0.2,0 -0.5,0 -0.7,-0.1 -0.1,0 -0.2,0 -0.3,0 -0.2,0 -0.4,-0.1 -0.6,-0.1 C 17.5,57 17.2,56.9 16.8,56.9 8.8,54.8 4,46.7 6,38.7 6,38.8 5.9,39 5.9,39.1 5.9,39 6,38.8 6,38.7 c -4.1,16.1 5.5,32.5 21.6,36.8 0.7,0.2 1.4,0.3 2,0.5 1.1,0.2 2.3,0.4 3.4,0.5 1.6,0.1 3.1,0.1 4.6,0 0.2,0 0.5,0 0.7,-0.1 0.1,0 0.2,0 0.4,0 0.2,0 0.4,0 0.6,-0.1 0.1,-0.2 0.5,-0.2 0.8,-0.3 z" 
            />
        </svg>
        <div class="typ-info-box" @click="onClickHandler">
            <div class="typ-title">{{info.typhoon_name}}</div>
            <div class="typ-detail">
                <div class="typ-item">중심압력: {{step.path.center_pressure}} hPa</div>
                <div class="typ-item">풍속: 시속 {{step.path.max_speed_h}} km/h, 초속 {{step.path.max_speed_s}} m/s</div>
                <div class="typ-item">강도: {{step.path.storm_radius}}</div>
                <div class="typ-item">이동속도: {{step.path.move_speed_h}} km/h</div>
                <div class="typ-item"><span v-if="root.search.type === '03'">예상</span>피해 학교 수: {{root.summary.count  | makeComma}}개교</div>
                <div class="typ-item"><span v-if="root.search.type === '03'">예상</span>피해 금액: {{Number((root.summary.cost/1000000).toFixed(0)) | makeComma}}백만원</div>
            </div>
        </div>
    </div>
</template>

<script>
import School from '@/components/School'
import SchoolPanel from '@/components/SchoolPanel'
import Vue from 'vue'

const SchoolComponent = Vue.extend(School)
const SchoolPanelComponent = Vue.extend(SchoolPanel)

const NUMPADD = 1000000, delay = 20
const animationState = {
    t: null,
    fn: null,
    i: 0
}

export default {
    props: {
        info: {
            type: Object,
            required: true
        },
        color: {
            type: String,
            required: true
        },
        size: {
            type: Number,
            default: 80
        },
        kakao: {
            type: Object,
            required: true
        },
        map: {
            type: Object,
            required: true
        },
        root: {
            type: Object,
            required: true
        },
        ext_param: {
          type: Object,
          required: true
        },

    },
    methods: {
        set (step) {
            if (typeof animationState.fn === 'function') return;

            if (typeof step === 'number') {
                this.step.n = step
                this.step.path = this.info.paths[step]

                let center = new this.kakao.maps.LatLng(this.step.path.latlng[0], this.step.path.latlng[1])
                this.overlay.setPosition(center)
                this.map.setCenter(center)

                if (this.step.area) this.step.area.setMap(null)


                this.step.area = new this.kakao.maps.Circle({
                    center : center,
                    radius: this.step.path.wind_radius * 1000, // 미터 단위의 원의 반지름입니다
                    strokeWeight: 1, // 선의 두께입니다
                    strokeColor: this.color, // 선의 색깔입니다
                    strokeOpacity: 0.4, // 선의 불투명도 입니다 1에서 0 사이의 값이며 0에 가까울수록 투명합니다
                    strokeStyle: 'dotted', // 선의 스타일 입니다
                    fillColor: this.color, // 채우기 색깔입니다
                    fillOpacity: 0.3  // 채우기 불투명도 입니다  
                })

                this.step.area_hist.push(new this.kakao.maps.Circle({
                  center : center,
                  radius: this.step.path.wind_radius * 100, // 미터 단위의 원의 반지름입니다
                  strokeWeight: 1, // 선의 두께입니다
                  strokeColor: this.color, // 선의 색깔입니다
                  strokeOpacity: 0.4, // 선의 불투명도 입니다 1에서 0 사이의 값이며 0에 가까울수록 투명합니다
                  strokeStyle: 'dotted', // 선의 스타일 입니다
                  fillColor: this.color, // 채우기 색깔입니다
                  fillOpacity: 0.4  // 채우기 불투명도 입니다
                }))

                if (this.focused) this.step.area.setMap(this.map)
                if (this.focused) this.step.area_hist.map(v=>v.setMap(this.map))
            }
            else {
                let path = this.info.paths[0]
                let center = new this.kakao.maps.LatLng(path.latlng[0], path.latlng[1])
                this.overlay.setPosition(center)
                this.map.setCenter(center)
            }
            this.root.tableData.loading = true
            this.overlay.setMap(this.map)
            this.redrawEstate()
        },
        unset () {
            this.overlay.setMap(null)
            this.route.setMap(null)
            if (this.step.area) this.step.area.setMap(null)
            this.step.area_hist.map(v=>v.setMap(null))
            for (let key in this.estates) {
                this.estates[key].unset()
            }
        },
        animationTo (step, duration=5000, fn) {
            if (animationState.t) clearInterval(animationState.t)
            if (typeof animationState.fn === 'function') {
                animationState.t = setInterval(animationState.fn, delay)
                return;
            }

            let from = this.step.n >= 0 ? this.step.path.latlng.slice() : this.info.paths[0].latlng.slice()
            let to = this.info.paths[step].latlng
            
            let lat_dist = Math.round((to[0] - from[0]) * NUMPADD)
            let lng_dist = Math.round((to[1] - from[1]) * NUMPADD)
            let keyframe = Math.ceil(duration / delay)

            let lat_inc = lat_dist / keyframe / NUMPADD
            let lng_inc = lng_dist / keyframe / NUMPADD

            animationState.i = 0;
            animationState.fn = () => {
                from[0] += lat_inc
                from[1] += lng_inc
                let center = new this.kakao.maps.LatLng(from[0], from[1])
                this.overlay.setPosition(center)
                if (keyframe < ++animationState.i) {
                    clearInterval(animationState.t)
                    animationState.fn = null
                    console.log('ANIMATION DONE')
                    if (typeof fn === 'function') fn()
                }
            }
            animationState.t = setInterval(animationState.fn, delay)
            this.map.panTo(new this.kakao.maps.LatLng(to[0], to[1]))
        },
        animationPause () {
            clearInterval(animationState.t)
            animationState.t = null
        },
        animationStop () {
            clearInterval(animationState.t)
            animationState.fn = null
            animationState.t = null
        },
        onClickHandler () {
            if (!this.focused) this.$emit('click', this.info.typhoon_id, this.info)
        },
        onSchoolEnterHandler (info) {
            if (info.inArea) {
                this.infopanel.set({...info, test: this.root.search.type === '03'})
            }
        },
        onSchoolLeaveHandler () {
            this.infopanel.unset()
        },
        onSchoolClickHandler (info) {
            this.$emit('school-detail', info)
        },
        async focus () {
            this.root.tableData.loading = true
            this.focused = true
            this.overlay.setZIndex(5)
            if (this.step.area) this.step.area.setMap(this.map)
            this.route.setMap(this.map)

            await this.initLocation()
            this.root.tableData.loading = false
            // if (this.info.typhoon_v_type !== 1) await this.initLocation()
            // else this.root.tableData.loading = false
        },
        async initLocation () {
            // if (!this.location.length) {
            //     let params = {tp: this.info.typhoon_id,fk_user_id:this.$session.getUserIndex()}
            //     let {data} = await this.$http.get('dashboard/location', {params})
            //     this.location = data
            // }
            let params = {tp: this.info.typhoon_id,fk_user_id:this.$session.getUserIndex()}
            let {data} = await this.$http.get('dashboard/location', {params})
            this.location = data
            this.setEstate(this.location)
            return true
        },
        blur () {
            this.focused = false
            this.overlay.setZIndex(4)
            for (let key in this.estates) {
                this.estates[key].unset()
            }
            if (this.step.area) this.step.area.setMap(null)
            this.step.area_hist.map(v=>v.setMap(null))
            this.route.setMap(null)
        },
        getRoute () {
            let points = this.info.paths.map(v => new this.kakao.maps.LatLng(v.latlng[0], v.latlng[1]))
            return new this.kakao.maps.Polyline({
                path: points,
                strokeWeight: 3,
                strokeColor: this.color, // 선의 색깔입니다
                strokeOpacity: 0.7, // 선의 불투명도 입니다 1에서 0 사이의 값이며 0에 가까울수록 투명합니다
                strokeStyle: 'dashed' // 선의 스타일입니다
            })
        },
        setEstate (estates) {
            for (let data of estates) {
                if (this.estates[data.id]) {
                    this.estates[data.id].set()
                }
                else {
                    const instance = new SchoolComponent({
                        propsData: {
                            info: data, 
                            color: this.color,
                            kakao: this.kakao,
                            map: this.map,
                            typhoon: this.info,
                            ext_param:this.ext_param
                        }
                    })
                    instance.$mount()
                    instance.$on('enter', this.onSchoolEnterHandler.bind(this))
                    instance.$on('leave', this.onSchoolLeaveHandler.bind(this))
                    instance.$on('detail', this.onSchoolClickHandler.bind(this))
                    this.estates[data.id] = instance
                }
            }
            this.$nextTick(this.updateCostTable.bind(this))
        },

        updateCostTable () {
            if (this.step.n >= 0) {
                let inArea = this.location.filter(v => v.inArea === true)
                this.root.tableData.items = inArea
                this.root.summary.count = inArea.length
                this.root.summary.cost = inArea.reduce((acc, cur) => (acc + cur.total_cost), 0)
                this.root.summary.max = inArea.reduce((acc, cur) => (acc < cur.total_cost ? cur.total_cost : acc), 0)
                this.root.summary.avg = Math.ceil(this.root.summary.cost / inArea.filter(v => v.total_cost > 0).length)
                this.root.tableData.loading = false
            }
            else {
                this.root.tableData.items = []
                this.root.summary.count = 0
                this.root.summary.cost = 0
                this.root.summary.max = 0
                this.root.summary.avg = 0
                this.root.tableData.loading = false
                // this.allShow = true
            }
        },

        redrawEstate () {
            for (let id in this.estates) {
                this.estates[id].set(this.step.n)
            }
            this.$nextTick(this.updateCostTable.bind(this))
        }
    },
    computed: {
        styles () {
            let size = `${this.size}px`
            return {width: size, height: size, 'margin-top': `-${this.size / 2}px`}
        }
    },
    mounted () {
        this.infopanel = new SchoolPanelComponent({propsData: {kakao: this.kakao, map: this.map}})
        this.infopanel.$mount()

        this.route = this.getRoute()
        this.overlay = new this.kakao.maps.CustomOverlay({
            map: null,
            clickable: true,
            content: this.$el,
            yAnchor: 0,
            zIndex: 4
        })
        this.set()
    },

    beforeDestroy () {
        this.animationStop()
        for (let id in this.estates) {
            this.estates[id].set(this.step.n).$destroy()
        }
    },

    data () {
        return {
            focused: false,
            overlay: null,
            infopanel: null,
            location: [],
            step: {
                n: -1,
                path: {},
                area: null,
                area_hist : []
            },
            route: null,
            estates: {}
        }
    }
}
</script>

<style lang="scss" scoped>
.typ {
    width: 50px; height: 50px;
    margin-top: -25px;
    opacity: 0.4;

    &.focused {
        opacity: 1;
        .typ-icon {
            animation: spin 4s linear infinite;
        }
    }
    &.instep {
        .typ-info-box {
            top: -158px;
            box-shadow: 0px 4px 16px rgb(0 0 0 / 40%);
            > .typ-detail { display: block !important; }
        }
    }
    .typ-info-box {
        position: absolute;
        top: -70px; left: 36px;
        padding: 10px;
        background-color: rgba(255,255,255,0.8);
        box-shadow: 0px 4px 16px rgb(0 0 0 / 20%);
        z-index: 600;
        cursor: pointer;
        border-radius: 3px;
        user-select: none;
    }
    .typ-icon {
        // margin-top: -20px;
        transition: opacity 1s;
        cursor: pointer;
    }
    .typ-icon:hover + .typ-info-box {
        display: block !important;
    }
    .typ-title {
        font-size: 16px;
    }
    .typ-detail {
        display: none;
    }
    .typ-item {
        
        font-size: 10px;
        color: #7a7a7a;
    }
}

@keyframes spin {
    100% { transform: rotate(-360deg); }
}
</style>
