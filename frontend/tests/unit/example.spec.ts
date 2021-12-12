import ConnectionBrowser from "@/components/ConnectionBrowser.vue";
import { expect } from "chai";
import { shallowMount } from "@vue/test-utils";

describe("ConnectionBrowser.vue", () => {
  it("renders title", () => {
    const title = "Beams";
    const wrapper = shallowMount(ConnectionBrowser);
    expect(wrapper.text()).to.include(title);
  });
});
