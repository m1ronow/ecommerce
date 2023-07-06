<template>
  <ion-page mode="ios">
    <products-list :products="products"></products-list>
  </ion-page>
</template>

<script setup lang="ts">
import { ref } from "vue";
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  onIonViewDidEnter,
} from "@ionic/vue";
import { useRoute } from "vue-router";
import ProductsList from "@/components/ProductsList.vue";
import { getCategoryProducts } from "@/api/api";

const products = ref<Array<Product>>([]);
const route = useRoute();
const categoryId: string | undefined = route.params.id
  ? route.params.id.toString()
  : undefined;

const loadProducts = () => {
  getCategoryProducts(categoryId)
    .then((response: any) => {
      products.value = response.data;
    })
    .catch((error: any) => {
      console.log(error);
    });
};

onIonViewDidEnter(() => {
  loadProducts();
});
</script>
