<template>
  <ion-page class="scrollbar-active" mode="ios">
    <products-list :products="products" :currency="currency"></products-list>
  </ion-page>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { IonPage, onIonViewDidEnter } from "@ionic/vue";
import ProductsList from "@/components/ProductsList.vue";
import { getProducts } from "@/api/api";

const products = ref<Array<Product>>([]);
let currency = "";

const loadProducts = () => {
  getProducts()
    .then((response: any) => {
      products.value = response.data.results.data;
      currency = response.data.results.currency;
    })
    .catch((error: any) => {
      console.log(error);
    });
};

onIonViewDidEnter(() => {
  loadProducts();
});
</script>
