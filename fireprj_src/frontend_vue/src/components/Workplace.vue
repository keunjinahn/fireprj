<template>
<v-menu
    v-model="menu"
    :close-on-content-click="false"
    :nudge-width="200"
    offset-x>
    <template v-slot:activator="{on}">
      <v-btn color="primary" text v-on="on" @click="clickHandler">
        <slot/>
      </v-btn>
    </template>

    <v-card :loading="loading">
      <template v-if="workplace">
        <v-list>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>{{workplace.CMPY_NM}}</v-list-item-title>
            </v-list-item-content>
            <v-list-item-avatar v-if="workplace.HEDOFC_YN === 'Y'">
              <v-avatar color="indigo" size="36">
                <span class="white--text body-2">본사</span>
              </v-avatar>
            </v-list-item-avatar>
          </v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>지번 주소</v-list-item-title>
              <v-list-item-subtitle>{{workplace.LN_ADRES}} {{workplace.LN_DTLADRES || '없음'}}</v-list-item-subtitle>
              <v-list-item-subtitle>{{workplace.LN_ZIP || '없음'}}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>도로명 주소</v-list-item-title>
              <v-list-item-subtitle>{{workplace.RN_ADRES || '없음'}}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>전화번호</v-list-item-title>
              <v-list-item-subtitle>{{workplace.TELNO || '없음'}}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>팩스번호</v-list-item-title>
              <v-list-item-subtitle>{{workplace.FAXNO || '없음'}}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>홈페이지</v-list-item-title>
              <v-list-item-subtitle>{{workplace.HMPG || '없음'}}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-textarea outlined hide-details
                label="메모"
                v-model="remark"
              />
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </template>
      <v-card-text v-else class="text-center">
        데이터를 불러오고 있습니다
      </v-card-text>

      <v-card-actions v-if="workplace">
        <v-spacer></v-spacer>
        <v-btn color="primary" text :disabled="remark === workplace.REMARK" @click="saveHandler">저장</v-btn>
        <v-btn color="primary" text @click="menu = false">닫기</v-btn>
      </v-card-actions>
    </v-card>
  </v-menu>
</template>

<script>
export default {
  props: {
    pk: {
      type: String,
      required: true
    }
  },
  methods: {
    async getData () {
      this.loading = true
      let {data} = await this.$http.get(`workplaces/${this.pk}`)
      this.workplace = data

      // 비교를 위해 선택
      this.remark = data.REMARK

      this.loading = false

    },
    clickHandler () {
      if (this.menu) return;
      this.getData()
    },
    async saveHandler () {
      this.loading = true
      try {
        let params = {
          REMARK: this.remark
        }
        await this.$http.put(`devices/${this.workplace.COLCTTRMNL_ID}`, params)
        this.workplace.REMARK = this.remark
      }
      catch (e) {
        console.error(e)
      }
      finally {
        this.loading = false
      }
    }
  },
  data () {
    return {
      loading: false,
      menu: false,
      workplace: null,
      remark: null
    }
  }
}
</script>