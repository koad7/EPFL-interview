import "./plugins/axios";
import "./registerServiceWorker";

import App from "./App.vue";
import VSwitch from "v-switch-case";
import Vue from "vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import i18n from "./i18n";

Vue.config.productionTip = false;

Vue.use(VSwitch);

new Vue({
  router,
  store,
  vuetify,
  i18n,
  render: (h) => h(App),
}).$mount("#app");
