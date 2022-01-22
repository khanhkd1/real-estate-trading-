<template>
  <div class="shops">
    <el-card class="box-card header">
      <el-row class="style-header" :gutter="20">
        <el-col>
          <el-input placeholder="Nhập thông tin cần tìm kiếm" v-model="search" @keydown.enter.native="handleGetPosts" @clear="handleGetPosts"
                    clearable
                    style="width: 400px; margin-right: 10px"
          ></el-input>
          <el-select clearable style="width: 150px; margin-right: 10px" v-model="district" placeholder="Quận huyện">
            <el-option
                v-for="item in districtList"
                :key="item.value"
                :label="item.label"
                :value="item.value">
            </el-option>
          </el-select>
          <el-input placeholder="Số phòng ngủ" v-model="bedroom" @keydown.enter.native="handleGetPosts"
                    type="number"
                    style="width: 150px; margin-right: 10px"
          ></el-input>
          <el-input placeholder="Số phòng tắm" v-model="toilet" @keydown.enter.native="handleGetPosts"
                    type="number"
                    style="width: 150px; margin-right: 10px"
          ></el-input>
          <el-button type="primary" @click="handleGetPosts"><i class="el-icon-search"></i> <span>Tìm kiếm</span></el-button>
        </el-col>
      </el-row>
    </el-card>

    <el-card class="main" style="margin-top: 20px">
      <el-table
          v-loading="loading"
          :data="posts">
        <el-table-column
            align="center"
            label="Ảnh"
            width="150px">
          <template v-slot:default="shop">
            <img style="width: 100px; height: 100px" v-if="shop.row.images" :src="shop.row.images[0]" alt="">
          </template>
        </el-table-column>
        <el-table-column
            prop="title"
            label="Tiêu đề">
          <template v-slot:default="shop">
            <router-link :to="'/post/' + shop.row.post_id">
              <el-link :underline="false" type="primary">{{ shop.row.title}}</el-link>
            </router-link>
          </template>
        </el-table-column>
        <el-table-column
            prop="acreage"
            align="center"
            label="Diện tích(m2)">
        </el-table-column>
        <el-table-column
            prop="bedroom"
            align="center"
            label="Phòng ngủ">
        </el-table-column>
        <el-table-column
            prop="toilet"
            align="center"
            label="Toilet">
        </el-table-column>
        <el-table-column
            prop="sold"
            align="center"
            label="Trạng thái">
          <template scope="item">
            {{ item.row.sold ? "Đã bán" : "Chưa bán" }}
          </template>
        </el-table-column>
        <el-table-column
            align="center"
            label="Hành động">
          <template scope="item">
            <el-button type="danger" icon="el-icon-delete" circle @click="handleDeletePost(item.row.post_id)"></el-button>
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
  name: "Post",
  methods: {
    handleGetPosts(params = {}) {
      this.loading = true
      if (this.search) {
        params.search = this.search
      }
      params.filter = "address:"
          + (this.district ? "" + this.district : "")
          + (this.toilet ? ",toilet:" + this.toilet : "")
          + (this.bedroom ? ",bedroom:" + this.bedroom : "")
      api.getPosts(params).then(response => {
        this.posts = _.get(response, "data.posts", [])
        this.total = _.get(response, "data.paging.total_count", 0)
        this.current_page = _.get(response, "data.paging.current_page", 1)
        this.loading = false
      }).catch(() => {
        this.loading = false
      })
    },
    handleCurrentChange(val) {
      let params = {
        page: val
      }
      this.handleGetPosts(params)
    },
    ...mapMutations([
      'updateTitle'
    ]),
    ...mapMutations('home', [
      'updateActiveMenu'
    ]),
    handleDeletePost(id) {
      this.$confirm('Dữ liệu không thể phục hồi, Bạn có muốn biếp tục?', 'Cảnh báo', {
        confirmButtonText: 'Xóa',
        cancelButtonText: 'Đóng',
        confirmButtonClass: 'deleteConfirm',
        type: 'warning'
      }).then(() => {

        api.deletePost(id).then(() => {
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
    this.handleGetPosts();
    this.updateTitle('Quản lý bài đăng')
    this.updateActiveMenu('2')
  },

  data() {
    return {
      loading: false,
      current_page: 1,
      per_page: 10,
      total: 0,
      from: 0,
      to: 0,
      posts: [],
      search: "",
      toilet: "",
      bedroom: "",
      district: "",
      districtList: [
        {
          label: "Ba Đình",
          value: "ba đình"
        },
        {
          label : "Bắc Từ Liêm",
          value: "bắc từ liêm"
        },
        {
          label : "Cầu Giấy",
          value: 'cầu giấy'
        },
        {
          label : "Đống Đa",
          value: "đống đa"
        },
        {
          label : "Hà Đông",
          value: 'hà đông'
        },
        {
          label : "Hai Bà Trưng",
          value: "hai bà trưng"
        },
        {
          label : "Hoàn Kiếm",
          value: 'hoàn kiếm'
        },
        {
          label : "Hoàng Mai",
          value: 'hoàng mai'
        },
        {
          label : "Long Biên",
          value: 'long biên'
        },
        {
          label : "Nam Từ Liêm",
          value: 'nam từ liêm'
        },
        {
          label : "Tây Hồ",
          value: 'tây hồ'
        },
        {
          label : "Thanh Xuân",
          value: 'thanh xuân'
        },
        {
          label : "Sơn Tây",
          value: 'sơn tây'
        },
        {
          label : "Ba Vì",
          value: 'ba vì'
        },
        {
          label : "Chương Mỹ",
          value : 'chương mỹ'
        },
        {
          label : "Đan Phượng",
          value: 'đan phượng'
        },
        {
          label : "Đông Anh",
          value: 'đông anh'
        },
        {
          label : "Gia Lâm",
          value: 'gia lâm'
        },
        {
          label : "Hoài Đức",
          value: 'hoài đức'
        },
        {
          label : "Mê Linh",
          value: 'mê linh'
        },
        {
          label : "Mỹ Đức",
          value: 'mỹ đức'
        },
        {
          label : "Phú Xuyên",
          value: 'phú xuân'
        },
        {
          label : "Phúc Thọ",
          value: 'phúc thọ'
        },
        {
          label : "Quốc Oai",
          value: 'quốc oai'
        },
        {
          label : "Sóc Sơn",
          value: 'sóc sơn'
        },
        {
          label : "Thạch Thất",
          value: 'thạch thất'
        },
        {
          label : "Thanh Oai",
          value: 'thanh oai'
        },
        {
          label : "Thanh Trì",
          value: 'thanh trì'
        },
        {
          label : "Thường Tín",
          value: 'thường tín'
        },
        {
          label : "Ứng Hoà",
          value: 'ứng hòa'
        }
      ]
    }
  }
}
</script>

<style lang="scss" scoped>
@import "src/assets/styles/variables";

</style>