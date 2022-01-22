<template>
  <div id="app">
    <AdminLayout v-if="isAuthenticated"/>
    <LoginLayout v-else />
  </div>
</template>

<script>
  import AdminLayout from './layouts/AdminLayout'
  import LoginLayout from './layouts/LoginLayout'
  import {mapState} from 'vuex'

  export default {
    name: 'App',
    computed: {
      ...mapState('auth', ['isAuthenticated']),
    },
    components: {
      AdminLayout,
      LoginLayout
    }
  }
</script>

<style lang="scss">
@import "./assets/styles/variables";

#app {
  font-family:Arial;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: $colorDefault;
}

body {
  margin: 0;
  background-color: #EDEEF0;

  .el-table__row, .el-table__header{
    .cell{
      word-break: normal;
      .column-name{
        cursor: pointer;
        text-decoration: none;
      }
      .el-button{
        padding: 8px!important;
        font-size: small!important;
      }
    }

  }

  .el-select-dropdown__item{
    span{
      i{
        color: $colorOrange;
      }
    }
  }
}

.el-upload{
  display: block!important;
  .el-upload-dragger{
    margin: 0 auto;
    width: 100% !important;
    height: 230px!important;
    background-color: #F8F8F8;
  }
  .el-upload-dragger:hover {
    border-color: #0bc7b4;
  }
}

.deleteConfirm{
  background-color: $colorRed!important;
  outline: none;
  border-color: $colorRed!important;
}
.el-table__body-wrapper{
  overflow-y: scroll!important;
}
.el-table__body-wrapper::-webkit-scrollbar {
  width: 10px;
  height: 10px;
  background-color: #FFF;
  border: none;
}

.el-table__body-wrapper::-webkit-scrollbar-thumb {
  background-color: #C0C4CC;
  border-radius: 8px;
}
.no1{
  .rank-user {
    width: 55px;
  }
  .user-name{
    color: $colorRed;
    font-weight: bold;
  }
  td{
    padding: 5px 0 0 0 !important;
  }
}
.no2{
  .rank-user {
    width: 60px;
  }
  .user-name{
    color: $colorMain;
    font-weight: bold;
  }
  td{
    padding: 5px 0 0 0!important;
  }
}
.no3{
  .rank-user {
    width: 60px;
  }
  .user-name{
    color: $colorGreen;
    font-weight: bold;
  }
  td{
    padding: 5px 0 0 0!important;
  }
}
.option {
  .el-radio__input.is-checked+.el-radio__label {
    color: #0bc7b4!important;
  }
  .el-radio__input.is-checked .el-radio__inner {
    border-color: #0bc7b4!important;
    background: #0bc7b4!important;
  }
  .el-radio__inner:hover {
    border-color: #0bc7b4!important;
  }
}
#ads-dialog {
  display: flex;
  align-items: center;
  justify-content: center;
  .el-dialog {
    background: #ffffff00;
    box-shadow: none;
    margin-top: 0vh!important;
    margin: 0;
    .el-dialog__body {
      padding: 0;
    }
    .el-dialog__close {
      color: white;
      width: 5px;
      height: 5px;
    }
    .el-dialog__close::before {
      background: $colorGray;
      border-radius: 50%;
      border: 1px solid white;
      padding: 5px;
    }
    .image-dialog {
      width: 21.75rem;
      height: 27rem;
      object-fit: cover;
    }
  }
}
.complaint-warp{
  .cell{
    padding-top: 5px!important;
  }
}

#variants{
  input{
    border-radius: 0!important;
    border-color: transparent;
  }
  .el-input-group__append{
    border-radius: 0!important;
    border-color: transparent;
  }
}
#inputOriginalPrice{
  border-radius: 5px 0 0 5px;
}
#inputPrice{
  border-radius: 0;
}
#inputQuantity{
  border-radius: 0 5px 5px 0;
}
.el-upload--picture-card{
  margin-right: 10px;
}
#description_intro {
  min-height: 160px !important;
}
.dialog-contact {
  .el-dialog {
    width: 500px;
    height: 400px;
  }
}
.air-seo-banner {
  .el-dialog{
    .el-dialog__header{
      button{
        top: 32px;
        right: 165px;
      }
    }
    .el-dialog__body{
      width: 85%;
      text-align: center;
      img{
        width: 100%;
      }
    }
  }
  div {
    text-align: center;
    background: none;
    box-shadow:none;
    margin: 80px auto !important;
    padding: 0 !important;
  }
}
</style>
