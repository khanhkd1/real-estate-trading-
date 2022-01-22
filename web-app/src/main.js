import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import locale from 'element-ui/lib/locale/lang/vi'
import router from './router'
import store from './store'
import UUID from "vue-uuid";

Vue.use(ElementUI, { locale });
Vue.use(UUID);
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App),
  linkActiveClass: "active"
}).$mount('#app')
