<template>
  <!--begin::Login-->
  <div class="login login-2 login-signin-on d-flex flex-column flex-lg-row flex-column-fluid bg-white">
    <!--begin::Aside-->
    <div class="login-aside order-2 order-lg-2 d-flex flex-row-auto position-relative overflow-hidden">
      <!--begin: Aside Container-->
      <div class="d-flex flex-column-fluid flex-column justify-content-between loginWarp py-9 px-7 py-lg-13 px-lg-35">
        <!--begin::Logo-->
        <a href="#" class="text-center pt-2">
        </a>
        <!--end::Logo-->
        <!--begin::Aside body-->
        <div class="d-flex flex-column-fluid flex-column flex-center">
          <!--begin::Signin-->
          <div class="login-form login-signin py-11">
            <!--begin::Form-->
            <form class="form" novalidate="novalidate">
              <!--begin::Form group-->
              <div class="form-group">
                <label class="font-size-h6 font-weight-bolder text-dark">Tài khoản</label>
                <input class="form-control form-control-solid h-auto py-4 rounded-lg"  v-model="email" type="email" @keydown.enter="handleLogin()">
                <div v-if="this.errorEmail !== '' " class="error">
                  <span> {{ errorEmail }} </span>
                </div>
              </div>
              <!--end::Form group-->
              <!--begin::Form group-->
              <div class="form-group input-password">
                <div class="d-flex justify-content-between mt-n5">
                  <label class="font-size-h6 font-weight-bolder text-dark pt-5">Mật khẩu</label>
                </div>
                <input class="form-control form-control-solid h-auto py-4 rounded-lg" type="password" v-model="password" @keydown.enter="handleLogin()">
                <div v-if="this.errorPassword !== '' " class="error">
                  <span> {{ errorPassword }} </span>
                </div>
              </div>
              <!--end::Form group-->
              <!--begin::Action-->
              <div class="text-center pt-2">
                <button class="btn btn-dark font-weight-bolder btnSubmit font-size-h6 py-3" type="button"  @click="handleLogin()">ĐĂNG NHẬP</button>
              </div>
              <!--end::Action-->
            </form>
          <!--end::Form-->
          </div>
          <!--end::Signin-->
        </div>
        <!--end::Aside body-->
      </div>
      <!--end: Aside Container-->
    </div>
    <!--begin::Aside-->
    <!--begin::Content-->
    <div class="content order-1 order-lg-1 d-flex flex-column w-100 pb-0" style="background-color: #F8F8F8;">
      <!--end::Title-->
      <!--begin::Image-->
      <div class="content-img d-flex flex-row-fluid bgi-no-repeat bgi-position-y-bottom bgi-position-x-center" :style="{'background-image': 'url(' + require('../assets/images/login.svg') + ')' }"></div>
      <!--end::Image-->
    </div>
    <!--end::Content-->
  </div>
  <!--end::Login-->
</template>
<script>
import {mapMutations, mapState} from 'vuex';
import api from '../api'
import _ from 'lodash'
// import axios from 'axios'

export default {
  name: "Login",
  data() {
    return {
      errorEmail: '',
      errorPassword: '',
      email: '',
      password: '',
    }
  },
  computed: {
    ...mapState('auth', ['isAuthenticated'])
  },
  watch: {
    email() {
      this.errorEmail = ''
    },
    password() {
      this.errorPassword = ''
    }
  },
  methods: {
    ...mapMutations('auth', [
      'updateLoginStatus',
      'updateAccessToken',
        'updateAuthUser'
    ]),
    handleLogin() {
      if (this.isValidData()) {
        let data = new FormData
        data.append('username', this.email)
        data.append('password', this.password)
        api.login(data).then((response) => {
          if (response) {
            this.updateAccessToken(_.get(response, 'data.token'))
            this.updateLoginStatus(true)
            this.updateAuthUser(_.get(response, 'data.user'))
            this.$router.push({name: 'Home'})
          }
        }).catch(() => {
          this.$message({message: 'Thông tin tài khoản hoặc mật khẩu không chính xác', type: 'error'});
        })
      }
    },
    isValidData() {
      let error = false;
      this.errorEmail = '';
      this.errorPassword = '';

      if (this.email.length === 0) {
        error = true;
        this.errorEmail = 'Tài khoản không được để trống';
      }
      if (this.password.length === 0) {
        error = true;
        this.errorPassword = 'Mật khẩu không được để trống';
      }

      return !error
    }
  }
}
</script>
<style scoped src="../assets/styles/login/login-2.css"></style>
<style scoped src="../assets/styles/login/style.bundle.css"></style>
<style lang="scss" scoped>
@import "../assets/styles/variables";
.content-img{
  background-repeat: no-repeat;
  background-position: center;
}

.flex-center{
  justify-content: normal;
}

.btnSubmit{
  width: 100%;
  background-color: #00DDC6 !important;
  border-color: #00DDC6 !important;
}

.error {
  color: $colorRed;
  margin-top: 8px;
  font-size: 12px;
}

.tip {
  margin-top: 25px;
  display: flex;
  justify-content: center;
  font-size: 14px;
  color: $colorSecond;

  span {
    a {
      color: $colorZentSoft;
      text-decoration: none;
    }
  }
}

.loginWarp{
  background-color: #fff;
  .box-forgot {
    width: 100%;
    text-align: right!important;
    margin-top: 20px;
    .fotgot-password {
      color:#0080dd;
      cursor: pointer;
      font-weight: 400!important;
      padding: 5px 8px;
      margin-bottom: 0;
      font-size: .875rem;
      &:hover{
        background-color: #b3bac536;
      }
    }
  }
  
}
.form-group{
  label{
    font-size: 1rem !important;
    font-weight: 400;
  }
}
.input-password {
  margin-bottom: 10px!important;
}
</style>