export const booleanOptions = [true, false];

// https://vuetifyjs.com/en/api/v-select/#props-items
interface SelectItemObject {
  text: string | number;
  value: string | number;
  disabled: boolean;
  divider: boolean;
  header: string;
}

export type SelectItem = string | SelectItemObject;
