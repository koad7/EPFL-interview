<template>
  <v-row>
    <v-col>
      <v-row>
        <v-col>
          <connection-browser
            :search.sync="search"
            :searches.sync="searches"
            :query="query"
          ></connection-browser>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import ConnectionBrowser from "@/components/ConnectionBrowser.vue";
import LocaleSelect from "@/components/commons/LocaleSelect.vue";
import { Searches } from "@/utils/common";
import { ConnectionField } from "@/backend";

@Component({
  components: {
    ConnectionBrowser,
    LocaleSelect,
  },
})
export default class Home extends Vue {
  readonly fields: string[] = Object.values(ConnectionField);

  search = "";
  searches: Searches = {};

  singleField = ConnectionField.Date;
  doubleFields: [ConnectionField, ConnectionField] = [
    ConnectionField.TCf,
    ConnectionField.TDpTot,
  ];

  get query(): string {
    const queries = Object.entries(this.searches)
      .filter(
        ([, value]) =>
          value != undefined && (typeof value == "boolean" || value.length > 0)
      )
      .map(([key, value]) => `${key}:${value}`);
    if (this.search && this.search.length > 0) {
      queries.push(`%${this.search}%`);
    }
    return queries.join(";");
  }
}
</script>
