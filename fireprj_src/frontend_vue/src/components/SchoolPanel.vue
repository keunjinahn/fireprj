<template>
    <div class="schl-info-box">
        <div class="schl-info-cont">
            <div class="">{{getCheckSchoolName()}}</div>
            <div class="">
                <div class="schl-item" >회원명: {{getCheckMemName()}}</div>
                <div class="schl-item">지역: {{info.area}}</div>
                <div class="schl-item">학교급: {{info.school_type}}</div>
<!--                <div class="schl-item"><span v-if="info.test">예상</span>피해유형: </div>-->
<!--                <div class="schl-item">{{getAcciContents(0)}}</div>-->
<!--                <div class="schl-item">{{getAcciContents(1)}}</div>-->
<!--                <div class="schl-item">{{getAcciContents(2)}}</div>-->
                <div class="schl-item" v-if="info.test"><span >예상</span>피해규모: <span :class="$getCostColor(info.total_cost)">{{info.total_cost | makeComma }}원</span></div>
                <div class="schl-item" v-else >피해규모: <span :class="$getCostColor(info.total_cost)">{{info.total_cost | makeComma }}원</span></div>
            </div>
        </div>
      <div class="schl-img-cont">
        <v-img :width="200" :height="160" :src="getAcciThumImage()" />
      </div>
    </div>
</template>

<script>
export default {
    props: {
        kakao: {
            type: Object,
            required: true
        },
        map: {
            type: Object,
            required: true
        }
    },
    methods: {
        async set (info) {
            this.info = info
            let center = new this.kakao.maps.LatLng(info.latlng[0], info.latlng[1])
            this.overlay.setPosition(center)
            this.overlay.setMap(this.map)
            this.updateImageFilePath()
        },
        unset () {
            this.overlay.setMap(null)
        },
        async updateImageFilePath() {
          let params = {
            acci_id:this.info.id
          };
          let { data } = await this.$http.get("acci_image_path",{params});
          if(data.image_file_path1 != '')
            this.image_file_path = data.image_file_path1
          else if(data.image_file_path2 != '')
            this.image_file_path = data.image_file_path2
          else if(data.image_file_path3 != '')
            this.image_file_path = data.image_file_path3
          else if(data.image_file_path4 != '')
            this.image_file_path = data.image_file_path4
          else if(data.image_file_path5 != '')
            this.image_file_path = data.image_file_path5
          else if(data.image_file_path6 != '')
            this.image_file_path = data.image_file_path6
          // console.log("this.image_file_path1 :" + this.image_file_path1)
        },
        getAcciThumImage() {
          if(this.image_file_path != undefined
              && this.image_file_path.length > 10){
              return this.image_file_path
          }
          // var random_file_path = "/static/simg/"+ (this.info.id % 4) + ".jpg"
          // // console.log("random_file_path1 :" + random_file_path1)
          return null
        },
        getAcciContents(index){
          if(this.info.acci_contents !=  undefined && this.info.acci_contents != '')
            this.info.acci_contents.split(',')[index]
          return ''
        },
        getCheckSchoolName(){
          if(this.$session.hasPermission([5])) {
            if(this.$session.getUserId() != this.info.school_id){
              return "미공개"
            }
          }
          else if(this.$session.hasPermission([6])) {
            if(this.$session.getUserId() != this.info.school_number){
              return "미공개"
            }
          }
          return this.info.school_name + "(" +this.info.school_number + ")"
        },
        getCheckMemName(){
          if(this.$session.hasPermission([5])) {
            if(this.$session.getUserId() != this.info.school_id){
              return "미공개"
            }
          }else if(this.$session.hasPermission([6])) {
            if(this.$session.getUserId() != this.info.school_number){
              return "미공개"
            }
          }
          return this.info.mem_name + "(" + this.info.school_id + ")"
        }

    },
    mounted () {
        this.overlay = new this.kakao.maps.CustomOverlay({
            map: null, yAnchor: 0, zIndex: 4,
            content: this.$el
        })

    },
    beforeDestroy () {
        this.unset()
    },

    data () {
        return {
            info: {},
            overlay: null,
            image_file_path:null
        }
    }
}
</script>