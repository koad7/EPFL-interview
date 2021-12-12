<template>
  <v-select v-model="item" :items="items" hide-details>
    <template v-slot:selection="data">
      {{ $t(prefix + data.item) }}
    </template>
    <template v-slot:item="data">
      {{ $t(prefix + data.item) }}
    </template>
  </v-select>
</template>

<script lang="ts">
import { Component, Prop, VModel, Vue } from "vue-property-decorator";
import { SelectItem } from "@/utils/vuetify";

@Component
export default class LocaleSelect extends Vue {
  @VModel({ type: String, default: "" })
  item!: string;
  @Prop({ type: Array as () => SelectItem[], default: [] })
  readonly items!: SelectItem[];
  @Prop({ type: String, default: "" })
  readonly prefix!: string;
}
</script>
