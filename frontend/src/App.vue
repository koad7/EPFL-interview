<template>
  <v-app>
    <v-app-bar app>
      <v-app-bar-title>
        <div>RESSLab Tools</div>
      </v-app-bar-title>
      <template v-slot:extension>
        <v-tabs>
          <v-tab to="/">Home</v-tab>
          <v-tab to="/connections">Connections</v-tab>
          <v-tab to="/columns">Columns</v-tab>
          <v-tab to="/bracings">Bracings</v-tab>
          <v-tab to="/about">About</v-tab>
        </v-tabs>
      </template>
    </v-app-bar>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>
