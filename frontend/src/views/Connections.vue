<template>
  <v-container fluid>
    <v-tabs>
      <v-tab to="/connections/database">Database</v-tab>
      <v-tab to="/connections/fragility-curve">Fragility Curve</v-tab>
      <v-tab to="/connections/component-model">Component Model</v-tab>
      <v-tab to="/connections/homework">Homework</v-tab>

    </v-tabs>
    <router-view></router-view>
  </v-container>
</template>
