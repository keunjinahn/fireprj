<template>
  <v-dialog v-model="value" persistent max-width="600px">
    <v-card :loading="loading">
      <v-card-title>
        <span class="headline">공지사항</span>
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-dialog
                ref="datedialog"
                v-model="dp.show"
                :return-value.sync="dp.date"
                persistent
                width="290px">
                <template v-slot:activator="{ on }">
                  <v-text-field
                    v-model="dp.date"
                    label="공지일"
                    prepend-icon="event"
                    readonly
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker v-model="dp.date" scrollable>
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="dp.show = false">Cancel</v-btn>
                  <v-btn text color="primary" @click="$refs.datedialog.save(dp.date)">OK</v-btn>
                </v-date-picker>
              </v-dialog>
            </v-col>
            <v-col cols="12">
              <v-text-field label="공지 제목*" v-model="form.NOTICE_SJ" hide-details required outlined></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-textarea label="공지 내용*" v-model="form.NOTICE_CN" hide-details required outlined></v-textarea>
            </v-col>
            <v-col cols="12" v-if="errorMessage">
              <span class="red--text">{{errorMessage}}</span>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="light-blue darken-2" dark @click="submit">저장</v-btn>
        <v-btn color="light-blue darken-2" text @click="cancel">취소</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import moment from 'moment'
export default {
  props: ['value', 'update'],
  methods: {
    async submit () {
      if (!this.validate()) return;
      this.loading = true
      try {
        let today = moment().format('YYYY-MM-DD HH:mm:ss')
        let params = {}
        if (this.form.NOTICE_SN) {
          params.UPDT_DT = today
          params.NOTICE_DT = moment(this.dp.date + ' 00:00:00').format('YYYY-MM-DD HH:mm:ss')
          params.RGSTER_NM = this.form.RGSTER_NM || 'test'
          params.NOTICE_SJ = this.form.NOTICE_SJ
          params.NOTICE_CN = this.form.NOTICE_CN
          params.RGSTER_ID = this.form.RGSTER_ID
          params.UPDUSR_ID = this.form.UPDUSR_ID
          await this.$http.put(`notices/${this.form.NOTICE_SN}`, params)
          this.$session.$emit('modal-alert', '공지가 수정되었습니다')
          this.$emit('complete', true)
        }
        else {
          params.NOTICE_DT = today // 수정해야됨
          params.RGSTER_NM = this.form.RGSTER_NM || 'test'
          params.NOTICE_SJ = this.form.NOTICE_SJ
          params.NOTICE_CN = this.form.NOTICE_CN
          params.RGSTER_ID = this.form.RGSTER_ID || 1
          params.RGST_DT = today
          params.UPDUSR_ID = this.form.UPDUSR_ID || 1
          await this.$http.post('notices', params)
          this.$session.$emit('modal-alert', '공지가 추가되었습니다')
          this.$emit('complete', true)
        }
        this.cancel()
      }
      catch (e) {
        console.error(e)
      }
      finally {
        this.loading = false
      }
    },
    validate () {
      if (!this.form.NOTICE_SJ) {
        this.errorMessage = '제목을 입력해 주세요'
        return false
      }
      if (!this.form.NOTICE_CN) {
        this.errorMessage = '내용을 입력해 주세요'
        return false
      }
      return true
    },
    cancel () {
      this.form.NOTICE_SN = null
      this.form.NOTICE_DT = null
      this.form.RGSTER_NM = null
      this.form.NOTICE_SJ = null
      this.form.NOTICE_CN = null
      this.form.RGSTER_ID = null
      this.form.RGST_DT = null
      this.form.UPDUSR_ID = null
      this.form.UPDT_DT = null
      this.close()
    },
    close () {
      this.$emit('input', false)
    }
  },
  watch: {
    value: {
      handler () {
        if (!this.value) return;
        this.errorMessage = null
        if (this.update) {
          this.form.NOTICE_SN = this.update.NOTICE_SN
          this.form.NOTICE_DT = this.update.NOTICE_DT
          this.form.RGSTER_NM = this.update.RGSTER_NM
          this.form.NOTICE_SJ = this.update.NOTICE_SJ
          this.form.NOTICE_CN = this.update.NOTICE_CN
          this.form.RGSTER_ID = this.update.RGSTER_ID
          this.form.RGST_DT = this.update.RGST_DT
          this.form.UPDUSR_ID = this.update.UPDUSR_ID
          this.form.UPDT_DT = this.update.UPDT_DT
          this.dp.date = moment(this.update.NOTICE_DT).format('YYYY-MM-DD')
        }
        else {
          this.dp.date = moment().format('YYYY-MM-DD')
        }
      }
    }
  },
  data () {
    return {
      loading: false,
      errorMessage: null,
      form: {
        NOTICE_SN: null, // 공지 순번
        NOTICE_DT: null, // 공지 일시
        RGSTER_NM: null, // 등록자 명
        NOTICE_SJ: null, // 공지 제목
        NOTICE_CN: null, // 공지 내용
        RGSTER_ID: null, // 등록자 ID
        RGST_DT: null, // 등록 일시
        UPDUSR_ID: null, // 수정자 ID
        UPDT_DT: null // 수정 일시
      },
      dp:{
        show: false,
        date: null
      }
    }
  }
}
</script>