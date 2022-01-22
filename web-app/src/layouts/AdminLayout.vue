<template>
  <el-container class="container-body">
    <el-aside class="sideBar">
      <div class="logoWrap">
      </div>
      <div class="menu-scroll">
        <el-menu
          :default-active="activeMenu"
          text-color="#253036"
          active-text-color="#0bc7b4">
          <router-link to="/">
            <el-menu-item class="menu_item mb-15" index="1">
              <i class="el-icon-menu"></i>
              <span>Tổng quan</span>
            </el-menu-item>
          </router-link>
          <el-menu-item-group title="QUẢN LÝ" class="mb-15">
            <router-link to="/posts">
              <el-menu-item index="2" class="menu_item">
                <i class="el-icon-tickets"></i>
                <span>Quản lý bài đăng</span>
              </el-menu-item>
            </router-link>
            <router-link to="/users">
              <el-menu-item index="3" class="menu_item">
                <i class="el-icon-user"></i>
                <span>Quản lý tài khoản</span>
              </el-menu-item>
            </router-link>
          </el-menu-item-group>
        </el-menu>
      </div>
    </el-aside>

    <el-container class="content">
      <el-header class="header">
        <div class="headerLeftWrap">
          {{ title }}
        </div>
        <div class="headerRightWrap">
          <el-dropdown>
            <span class="el-avatar el-avatar--medium el-avatar--circle">
                          <img src="../assets/images/user_default.png" alt="">
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item divided @click.native="logout">
                Đăng xuất
              </el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </el-header>

      <el-main class="main">
        <router-view/>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import {mapMutations, mapActions, mapState, mapGetters} from 'vuex'
// import api from '../api'
// import _ from 'lodash'

export default {
  name: 'AdminLayout',
  methods: {
    ...mapMutations('auth', ['updateAuthUser','updatePermissions']),
    ...mapMutations('home', ['updateUnread', 'updateActiveMenu']),
    ...mapActions('auth', ['logout']),
  },
  data(){
    return{
      role: {},
      endTimeCurrentPack: '',
      statusCurrentPack: null,
    }
  },
  computed: {
    ...mapState([
      'title'
    ]),
    ...mapState('home', [
      'unread', 'activeMenu'
    ]),
    ...mapState('auth', [
      'authUser'
    ]),
    ...mapGetters('auth', [
      'hasPermission'
    ])
  },
  mounted() {
    // api.getAuthUser().then((response) => {
    //   if (response) {
    //     this.updateAuthUser(response.data)
    //     if (this.$route.name == "Home") {
    //     }
    //   }
    // })
  },
  watch: {
    // $route() {
    //   if (this.$route.name === "Home") {
    //
    //   }
    // }
  }
}
</script>

<style lang="scss" scoped>
@import "../assets/styles/variables";
.container-body{
  height: 100vh;
}
.sideBar {
  width: 250px !important;
  height: 100vh;
  background: $colorSideBarBg;
  box-shadow: inset -10px 0 10px -5px rgba(0, 0, 0, 0.1);
  position: relative;
  outline: none;
  overflow: hidden;

  .logoWrap {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #fff;
    flex-shrink: 0;
    min-height: 58px;
    width: 230px;

    img {
      padding-top: 10px;
      width: 150px;
    }
  }
  .menu-scroll {
    height: 85%;
    outline: none;
    overflow-y: hidden;

    &::-webkit-scrollbar {
      width: 10px;
      height: 10px;
    }

    &::-webkit-scrollbar-thumb {
      background-color: #C0C4CC;
      border-radius: 8px;
    }

    &::-webkit-scrollbar-track {
      background-image: linear-gradient(to right, #F8F8F8 , #EAEAEA);
    }

    &:hover {
      overflow-y: scroll;

      .el-menu {
        box-shadow: inset -10px 0 10px -14px rgba(0, 0, 0, 0.1);
      }
    }
    .el-menu {
      padding-bottom: 50px;
      border: none;
      box-shadow: inset -10px 0 10px -5px rgba(0, 0, 0, 0.1);

      a {
        color: rgb(255, 255, 255);
        text-decoration: none;

        .menu_item:hover {
          background-color: #0bc7b41c !important;
        }
      }
    }
  }

  .is-active {
    background-color: #0bc7b41c !important;
  }

  .customBadge {
    background-color: #f56c6c;
    border-radius: 10px;
    color: #fff;
    display: inline-block;
    font-size: 12px;
    height: 18px;
    line-height: 18px;
    padding: 0 6px;
    text-align: center;
    white-space: nowrap;
    border: 1px solid #fff;
    margin-left: 5px;
  }
}

.content {
  .header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid $colorStroke;
    height: 60px;
    background: $colorHeaderBg;
    padding: 0 24px;

    .headerLeftWrap {
      display: flex;
      align-items: center;
      font-size: 24px;
      font-weight: bold;
    }

    .headerRightWrap {
      display: flex;
      align-items: center;

      .notification {
        margin-right: 40px;
        font-size: 24px;
        color: gray;
      }

      .notification:hover {
        color: $colorSecondary;
      }
    }
  }
}

.el-main {
  overflow-x: scroll;
  overflow-y: auto;
  max-height: calc(100vh - 66px);
  padding: 20px 20px 15px 20px;

}

.el-main::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

.el-main::-webkit-scrollbar-thumb {
  background-color: #C0C4CC;
  border-radius: 8px;
}

.profileUser {
  color: rgb(255, 255, 255);
  text-decoration: none;
}

.mb-15 {
  margin-bottom: 15px;
}
.pb-0 {
  padding-bottom: 0;
}
.footer{
  position: fixed;
  bottom: 0;
  text-align: center;
  background-color: white;
  padding: 5px 20px;
  box-shadow: inset -10px 0 10px -5px rgb(0 0 0 / 10%);
  width: 210px;
  p{
    margin: 5px 0;
    color: #9da1a8;
    font-size: 14px;
    a{
      text-decoration: none;
      color: #F05A24;
    }
  }
}
.el-menu-item-group::v-deep .el-menu-item:focus{
  background-color: #ffffff00 !important;
}
.sideBar .menu-scroll .el-menu a .is-active{
  background-color: #0bc7b41c !important;
}
</style>
