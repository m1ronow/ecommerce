import { defineStore } from "pinia";
import { ref, watch } from "vue";
import { useRoute } from "vue-router";

export const useListParamsStore = defineStore("list-params", () => {
  const route = useRoute();
  const params = ref<any>(route.query);

  watch(() => route.query, () => {
    params.value = route.query;
  })

  return { params };
});
