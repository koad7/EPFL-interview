import VueRouter, { RouteConfig } from "vue-router";

import Vue from "vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "Home",
    component: () => import("../views/Home.vue"),
  },
  {
    path: "/connections",
    component: () => import("../views/Connections.vue"),
    children: [
      {
        path: "",
        redirect: "database",
      },
      {
        path: "database",
        component: () => import("../views/connections/Database.vue"),
      },
      {
        path: "fragility-curve",
        component: () => import("../views/connections/FragilityCurve.vue"),
      },
      {
        path: "component-model",
        component: () => import("../views/connections/ComponentModel.vue"),
      },
      {
        path: "homework",
        component: () => import("../views/connections/Homework.vue"),
      },
    ],
  },
  {
    path: "/columns",
    name: "Columns",
    component: () => import("../views/Columns.vue"),
  },
  {
    path: "/bracings",
    name: "Bracings",
    component: () => import("../views/Bracings.vue"),
  },
  {
    path: "/about",
    name: "About",
    component: () => import("../views/About.vue"),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
