import { ConnectionsApi } from "@/backend";
import Vue from "vue";
import axios from "axios";

const axiosInstance = axios.create();
const baseUrl = process.env.VUE_APP_BACKEND_URL;
Vue.prototype.$connectionsApi = new ConnectionsApi(
  undefined,
  baseUrl,
  axiosInstance
);
