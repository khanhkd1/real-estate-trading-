<template>
  <div class="detail">
    <el-card v-loading="loading">
      <div class="header">
        <h1 style="margin-top: 0">{{post.sold ? "(Đã bán) " : ""}}{{post.title}}</h1>
      </div>
      <div class="slice-img">
        <el-row :gutter="5" style="text-align: center">
          <el-col :span="6" v-for="(item, index) in post.images" :key="index">
            <img style="width: 100%; height: 200px" :src="item">
          </el-col>
        </el-row>
      </div>
      <div class="info">
        <div class="el-row">
          <el-col :span="14">
            <h4>Thông tin chi tiết</h4>
            <p><b>Gía bán:</b> {{ post.price ? post.price : "Đang cập nhật"}}</p>
            <p><b>Địa chỉ:</b> {{ post.address ? post.address : "Đang cập nhật"}}</p>
            <p><b>Diện tích:</b> {{ post.acreage ? post.acreage : "Đang cập nhật"}} (m2)</p>
            <p><b>Phòng ngủ:</b> {{ post.bedroom ? post.bedroom : "Đang cập nhật"}}</p>
            <p><b>Phòng tắm:</b> {{ post.toilet ? post.toilet : "Đang cập nhật"}}</p>
            <p><b>Ngày đăng:</b> {{ post.time_upload ? post.time_upload : ""}}</p>
            <p><b>Mô tả:</b></p>
            <p>{{ post.description ? post.description : "Đang cập nhật"}}</p>
          </el-col>
          <el-col :span="10">
            <h4>Thông tin liên hệ</h4>
            <el-row>
              <el-col :span="5">
                <img :src="post.user ? post.user.avatar : ''" style="width: 100px; height: 100px; border-radius: 50%">
              </el-col>
              <el-col :span="19">
                <p><b>Người đăng: </b>{{ post.user ? post.user.fullname : ""}}</p>
                <p><b>Email: </b>{{ post.user ? post.user.email : ""}}</p>
                <p><b>Số điện thoại: </b>{{ post.user ? post.user.phone : ""}}</p>
                <p><b>Địa chỉ: </b>{{ post.user ? post.user.address : ""}}</p>
              </el-col>
            </el-row>
          </el-col>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import api from '../api';
import _ from "lodash";
import {mapMutations} from "vuex";

export default {
  name: "DetailPost",
  data() {
    return {
      loading: false,
      post: []
    }
  },
  mounted() {
    this.updateTitle('Chi tiết bài viết')
    this.updateActiveMenu('2')
    this.handleGetPost();
  },
  methods: {
    ...mapMutations([
      'updateTitle'
    ]),
    ...mapMutations('home', [
      'updateActiveMenu'
    ]),
    handleGetPost() {
      this.loading = true;
      api.getDetailPost(this.$route.params.id).then(response => {
        this.post = _.get(response, "data")
        this.loading = false;
      }).catch(() => {
        this.loading = false;
        this.$router.push({ path: '/posts'})
        this.$message({
          type: "error",
          message: "Bài viết không tồn tại"
        })
      })
    }
  }
}
</script>

<style lang="scss" scoped>

</style>