<template>
  <ion-app>
    <ion-page mode="ios" id="main-content">
      <ion-tabs>
        <Header></Header>

        <ion-router-outlet :animated="false"></ion-router-outlet>

        <ion-tab-bar class="ion-hide-sm-up" slot="bottom">
          <ion-tab-button tab="home" href="/home">
            <ion-icon :icon="homeOutline" />
            <ion-label>Home</ion-label>
          </ion-tab-button>

          <ion-tab-button tab="favorites" href="/favorites">
            <ion-icon :icon="heartOutline" />
            <ion-label>Favorites</ion-label>
          </ion-tab-button>

          <ion-tab-button tab="cart" href="/cart">
            <ion-icon :icon="cartOutline" />
            <ion-label>Cart</ion-label>
          </ion-tab-button>

          <ion-tab-button tab="orders" href="/orders">
            <ion-icon :icon="receiptOutline" />
            <ion-label>Orders</ion-label>
          </ion-tab-button>
        </ion-tab-bar>
      </ion-tabs>
    </ion-page>
  </ion-app>
</template>

<script setup lang="ts">
import {
  IonApp,
  IonPage,
  IonHeader,
  IonContent,
  IonSearchbar,
  IonCol,
  IonGrid,
  IonRow,
  IonCard,
  IonCardContent,
  IonCardHeader,
  IonCardSubtitle,
  IonCardTitle,
} from "@ionic/vue";
import {
  IonButton,
  IonButtons,
  IonToolbar,
  IonIcon,
  IonInput,
  IonMenuToggle,
} from "@ionic/vue";
import {
  personCircle,
  bagCheckOutline,
  cartOutline,
  bagAddOutline,
  heartOutline,
  desktopOutline,
  chevronExpand,
  listOutline,
  receiptOutline,
} from "ionicons/icons";

import {
  IonFab,
  IonFabButton,
  IonItem,
  IonLabel,
  IonMenu,
  IonRadio,
  IonRadioGroup,
  IonTitle,
  IonAccordion,
  IonAccordionGroup,
  IonTabs,
  IonRouterOutlet,
  IonTabBar,
  IonTabButton,
} from "@ionic/vue";
import {
  add,
  shirtOutline,
  chevronDown,
  homeOutline,
  chevronUp,
  playCircle,
  radio,
  library,
  search,
} from "ionicons/icons";
import { createHead } from "unhead";
import Header from "./components/Header.vue";

createHead();
</script>
