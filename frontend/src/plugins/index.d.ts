import { ConnectionsApi } from "@/backend";

declare module "vue/types/vue" {
  interface Vue {
    $connectionsApi: ConnectionsApi;
  }
}
