<template>
  <ion-page class="scrollbar-active" mode="ios">
    <ion-grid :fixed="true" class="login-page">
      <ion-text class="page-title">
        <ion-icon :icon="personOutline" size="large"></ion-icon>
        <h1 class="page-title--fixed-margin">Log In</h1>
      </ion-text>

      <div class="login-container">
        <LoginForm></LoginForm>
      </div>
    </ion-grid>
  </ion-page>
</template>

<script setup lang="ts">
import { watch } from "vue";
import { IonPage, IonGrid, IonText, IonIcon, useIonRouter } from "@ionic/vue";
import LoginForm from "@/components/LoginForm.vue";
import { personOutline } from "ionicons/icons";
import { useAuthStore } from "@/stores/auth";

const router = useIonRouter();
const auth = useAuthStore();

// if user logged in - redirect him to the main page
watch(auth, () => {
  if (auth.isLoggedIn) {
    router.push("/");
  }
});
</script>

<style>
.login-page {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login-container {
  width: 40%;
}
</style>
