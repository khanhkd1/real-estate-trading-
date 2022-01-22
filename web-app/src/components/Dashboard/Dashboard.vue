<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6">
        <div class="card">
          <div class="card-header">
            <div class="card-icon card-icon-danger">
              <i class="el-icon-money"></i>
            </div>
            <p class="card-category">Số lượng bài viết</p>
            <h3 class="card-title">
              {{ dashboard.number_posts ? dashboard.number_posts : 0}}
            </h3>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="card">
          <div class="card-header">
            <div class="card-icon card-icon-info">
              <i class="el-icon-coin"></i>
            </div>
            <p class="card-category">Số lượng tài khoản</p>
            <h3 class="card-title">
              {{ dashboard.number_users ? dashboard.number_users : 0}}
            </h3>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import {mapMutations, mapState} from "vuex";
import api from "@/api";
import _ from 'lodash'

export default {
  name: 'Dashboard',
  props: {
    msg: String
  },
  data() {
    return {
      loading: false,
      isOpenBanner: null,
      dashboard: {}
    }
  },
  computed: {
    ...mapState('auth', [
      'authUser', 'isAuthenticated'
    ])
  },
  methods: {
    ...mapMutations([
      'updateTitle'
    ]),
    ...mapMutations('home', [
      'updateActiveMenu'
    ]),
    getDashboard() {
      api.dashboard().then(response => {
        this.dashboard = _.get(response, 'data', {})
      })
    }
  },
  mounted() {
    this.updateTitle('Tổng quan')
    this.updateActiveMenu("1")
    this.getDashboard()
  },
  watch: {
    isBanner() {
      this.isOpenBanner = this.isBanner
    }
  }
}
</script>

<style scoped lang="scss">
.dashboard {
  .card {
    border: 0;
    margin-bottom: 30px;
    margin-top: 30px;
    border-radius: 6px;
    color: #333;
    background: #fff;
    width: 100%;
    box-shadow: 0 1px 4px 0 rgb(0 0 0 / 14%);
    position: relative;
    display: flex;
    flex-direction: column;
    min-width: 0;

    .card-header {
      margin: 0 15px;
      padding: 0;
      position: relative;
      text-align: right;

      .card-icon {
        border-radius: 3px;
        background-color: #999;
        padding: 15px;
        margin-top: -20px;
        margin-right: 15px;
        float: left;
        color: #fff;
        font-size: 28px;

        &.card-icon-warning {
          background: linear-gradient(60deg, #ffa726, #fb8c00);
          box-shadow: 0 4px 20px 0 rgb(0 0 0 / 14%), 0 7px 10px -5px rgb(255 152 0 / 40%)
        }

        &.card-icon-success {
          background: linear-gradient(60deg, #66bb6a, #43a047);
          box-shadow: 0 4px 20px 0 rgb(0 0 0 / 14%), 0 7px 10px -5px rgb(76 175 80 / 40%)
        }

        &.card-icon-danger {
          background: linear-gradient(60deg, #ef5350, #e53935);
          box-shadow: 0 4px 20px 0 rgb(0 0 0 / 14%), 0 7px 10px -5px rgb(244 67 54 / 40%)
        }

        &.card-icon-info {
          background: linear-gradient(60deg, #26c6da, #00acc1);
          box-shadow: 0 4px 20px 0 rgb(0 0 0 / 14%), 0 7px 10px -5px rgb(0 188 212 / 40%)
        }
      }

      .card-category {
        color: #999;
        font-size: 14px;
      }
    }
  }

  .box-title {
    font-weight: 300;
    color: #1C2B36;
    font-size: 20px;
    margin-top: 0;
  }

  .el-row {
    margin-bottom: 20px;
  }

  .product-img {
    width: 50px;
    height: 50px;
    object-fit: cover;
  }

  .paginationWarp {
    padding: 5px 20px;
    margin-bottom: 15px;
    .el-pagination {
      float: right;
    }

    .textInfo {
      p {
        font-size: .92857rem;
        margin: 10px 0;
      }
    }
  }
}
</style>
