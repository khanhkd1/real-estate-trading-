<template>
  <div class="shops">
    <el-card class="main">
      <el-table
          v-loading="loading"
          :data="users">
        <el-table-column
            align="center"
            label="Ảnh"
            width="150px">
          <template v-slot:default="shop">
            <img style="width: 100px; height: 100px" v-if="shop.row.avatar" :src="shop.row.avatar" alt="">
          </template>
        </el-table-column>
        <el-table-column
            prop="username"
            label="Tài khoản">
        </el-table-column>
        <el-table-column
            prop="email"
            label="Email">
        </el-table-column>
        <el-table-column
            prop="fullname"
            label="Họ tên">
        </el-table-column>
        <el-table-column
            prop="phone"
            label="Số điện thoại">
        </el-table-column>
        <el-table-column
            prop="address"
            label="Địa chỉ">
        </el-table-column>
        <el-table-column
            align="center"
            label="Hành động">
          <template scope="item">
            <el-button type="danger" icon="el-icon-delete" circle @click="handleDeleteUser(item.row.user_id)"></el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="paginationWarp" style="float: right; margin: 20px 0 20px 0">
        <el-col :xs="{span:24}" :sm="{span:14}" :md="{span:14}" :lg="{span:14}">
          <el-pagination
              @current-change="handleCurrentChange"
              :current-page="current_page"
              :page-size="20"
              layout="prev, pager, next"
              :total="total">
          </el-pagination>
        </el-col>
      </div>
    </el-card>
  </div>
</template>

<script>
import api from '../api';
import _ from "lodash";
import {mapMutations} from "vuex";

export default {
  name: "User",
  methods: {
    handleGetUsers(params = {}) {
      this.loading = true
      if (this.search) {
        params.search = this.search
      }
      api.getUsers(params).then(response => {
        this.users = _.get(response, "data", [])
        this.loading = false
      }).catch(() => {
        this.loading = false
      })
    },
    handleCurrentChange(val) {
      let params = {
        page: val
      }
      this.handleGetUsers(params)
    },
    ...mapMutations([
      'updateTitle'
    ]),
    ...mapMutations('home', [
      'updateActiveMenu'
    ]),
    handleDeleteUser(id) {
      this.$confirm('Dữ liệu không thể phục hồi, Bạn có muốn biếp tục?', 'Cảnh báo', {
        confirmButtonText: 'Xóa',
        cancelButtonText: 'Đóng',
        confirmButtonClass: 'deleteConfirm',
        type: 'warning'
      }).then(() => {

        api.deleteUser(id).then(() => {
          this.$message({
            showClose: true,
            type: 'success',
            message: 'Xóa thành công'
          });
          this.closePopper()
          this.handleCurrentChange(this.current_page)
        })
      })
    },
    closePopper() {
      let control = document.getElementsByClassName('el-popper');
      control.forEach(element => {
        element.style.display = 'none'
        element.style.position = 'static'
      })
    },
  },
  mounted() {
    this.handleGetUsers();
    this.updateTitle('Quản lý tài khoản')
    this.updateActiveMenu('3')
  },

  data() {
    return {
      loading: false,
      current_page: 1,
      per_page: 10,
      total: 0,
      from: 0,
      to: 0,
      users: [],
    }
  }
}
</script>

<style lang="scss" scoped>
@import "src/assets/styles/variables";

</style>