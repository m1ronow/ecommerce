<template>
  <ion-page class="scrollbar-active" mode="ios">
    <ion-grid :fixed="true">
      <ion-text class="page-title">
        <ion-icon
          :icon="personCircleOutline"
          size="large"
          aria-hidden="true"
        ></ion-icon>
        <h1 class="page-title--fixed-margin">Profile</h1>
      </ion-text>

      
    </ion-grid>
  </ion-page>
</template>

<script setup lang="ts">
import { IonPage, IonGrid, IonText, IonIcon } from "@ionic/vue";

import { personCircleOutline } from "ionicons/icons";
</script>
