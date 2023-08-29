<template>
  <ion-page class="scrollbar-active" mode="ios">
    <products-list 
      :productsData="productsData"
    >
    </products-list>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { IonPage, onIonViewDidEnter } from "@ionic/vue";
import ProductsList from "@/components/ProductsList.vue";
import { getProducts } from "@/api/api";
import { useListParamsStore } from "@/stores/list-params";

let paramsStore = useListParamsStore();
const productsData = ref<any>({});

const loadProducts = (params: any = paramsStore.params) => {
  getProducts(params)
    .then((response: any) => {
      productsData.value = response.data;
    })
    .catch((error: any) => {
      console.log(error);
    });
};

onIonViewDidEnter(() => {
  paramsStore = useListParamsStore();
  loadProducts();
});

watch(() => paramsStore.params, () => {
  loadProducts(paramsStore.params)
})
</script>
