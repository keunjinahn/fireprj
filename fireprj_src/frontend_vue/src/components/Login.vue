<template>
  <v-content>
    <v-container class="fill-height" fluid>
      <v-row align="center" justify="center">
        <v-col cols="12" sm="8" md="4">
          <v-card class="elevation-12">
            <v-toolbar color="blue darken-2" dark flat dense>
              <v-toolbar-title>리더스테크 통합화재감시시스템 플랫폼</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form>
                <v-text-field
                  v-model="form.userid"
                  label="아이디"
                  name="login"
                  prepend-icon="person"
                  type="text"
                  color="grey"
                  autofocus
                  @keypress.enter="login"
                />
                <v-text-field
                  v-model="form.userpw"
                  id="password"
                  label="비밀번호"
                  name="password"
                  prepend-icon="lock"
                  color="grey"
                  type="password"
                  @keypress.enter="login"
                />
              </v-form>
            </v-card-text>
            <v-card-actions>
              <div class="flex-grow-1"></div>
              <v-btn color="primary" @click="login" :loading="loading">로그인</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-content>
</template>

<script>
export default {
  methods: {
    async login() {
      this.loading = true;
      try {
        await this.$session.login(this.form);
        //this.$control.connect();

      } catch (e) {
        this.$session.$emit('modal-alert', e.toString())
      } finally {
        this.loading = false;
      }
    }
  },
  data() {
    return {
      loading: false,
      form: {
        userid: "",
        userpw: ""
      }
    };
  }
};
</script>