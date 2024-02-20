<template>
    <div class="sch-dot" :class="{'in-area': inArea}" v-show="check_school_include()" @mouseenter="onEnterHandler" @mouseleave="onLeaveHandler" @click="onClickHandler">
        <div class="sch-circle" :class="level"></div>
      <!--        <div v-if="ext_param.school_include" class="sch-circle-2" :class="level"></div>-->
      <!--        <div v-else class="sch-circle" :class="level"></div>-->
    </div>
</template>

<script>
const kakao = window.kakao
export default {
    props: {
        info: {
            type: Object,
            required: true
        },    
        typhoon: {
            type: Object,
            required: true
        },
        color: {
            type: String,
            required: true
        },
        size: {
            type: Number,
            default: 30
        },
        kakao: {
            type: Object,
            required: true
        },
        map: {
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
            let center = new this.kakao.maps.LatLng(this.info.latlng[0], this.info.latlng[1])
            this.overlay.setPosition(center)
            this.overlay.setMap(this.map)
            if (typeof step === 'number') this.calcInArea(step)
        },
        unset () {
            this.overlay.setMap(null)
        },
        setColor () {
            this.level = this.$getColor(this.info.total_cost)
        },
        onEnterHandler () {
            // this.overlay.setZIndex(6)
            this.$emit('enter', this.info)
        },
        onLeaveHandler () {
            // this.overlay.setZIndex(1)
            this.$emit('leave', this.info)
        },
        onClickHandler () {
            this.$emit('detail', this.info)
        },
        calcInArea (step) {
            let v = (step >= this.step)
            this.inArea = v
            this.info.inArea = v
        },
        getShowStep () {
            let i
            for (i=0; i<this.typhoon.paths.length; i++) {
                let cp = this.typhoon.paths[i]
                if (!cp || !cp.latlng) continue;
                let tc = new this.kakao.maps.LatLng(this.info.latlng[0], this.info.latlng[1])
                let sc = new this.kakao.maps.LatLng(cp.latlng[0], cp.latlng[1])
                let dt = cp.wind_radius * 1000

                this.line.setPath([sc, tc])
                let ln = this.line.getLength()
                if (ln <= dt) break;
            }
            this.step = i
        },
        check_school_include(){
          if(this.ext_param.school_include == true){
            if(this.$session.getUserId() == this.info.school_id
              || this.$session.getUserId() == this.info.school_number
              ){
              return true
            }else{
              return false
            }
          }
          return true
        }
    },
    mounted () {
        this.setColor()
        this.overlay = new this.kakao.maps.CustomOverlay({
            map: null,
            clickable: true,
            content: this.$el,
            yAnchor: 0,
            zIndex: 1
        })
        this.line = new this.kakao.maps.Polyline({})
        this.getShowStep()
        this.set()
    },

    data () {
        return {
            overlay: null,
            line: null,
            route: null,
            estates: [],
            level: 'red',
            inArea: false,
            step: 0
        }
    }
}
</script>

<style lang="scss" scoped>
.sch-circle {
    width: 8px; height: 8px;
    border-radius: 4px;
    cursor: pointer;
}
.sch-circle-2 {
  width: 12px; height: 12px;
  border-radius: 6px;
  cursor: pointer;
}
.cost_color_1 {background-color:#03a9f4}
.cost_color_2 {background-color:#aeea00}
.cost_color_3 {background-color:#ffff00}
.cost_color_4 {background-color:#ff9800}
.cost_color_5 {background-color:#ff0000}
</style>