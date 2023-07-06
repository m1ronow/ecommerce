<template>
  <form class="login__inputs" @submit.prevent="handleLogin">
    <ion-item class="login__input-item" lines="none">
      <ion-input
        id="emailInput"
        v-model="userData.email"
        type="email"
        placeholder="email@example.com"
        required
        @keydown.enter="
          userData.password ? handleLogin() : focusOnInput('passwordInput')
        "
        class="login__input"
      >
      </ion-input>
      <ion-icon :icon="mail" slot="start" class="login__input-icon"> </ion-icon>
    </ion-item>

    <ion-item class="login__input-item" lines="none">
      <ion-input
        id="passwordInput"
        v-model="userData.password"
        :clearOnEdit="false"
        type="password"
        placeholder="Password"
        required
        @keydown.enter="
          userData.email ? handleLogin() : focusOnInput('emailInput')
        "
        class="login__input"
      >
      </ion-input>
      <ion-icon :icon="lockClosed" slot="start" class="login__input-icon">
      </ion-icon>
    </ion-item>

    <div v-if="loginErrorMessage" class="login__form-error">
      <ion-icon :icon="alertCircleOutline" slot="start" color="danger" />
      <div>
        {{ loginErrorMessage }}
      </div>
    </div>

    <ion-button type="submit" color="dark" expand="full" class="login__button">
      Log In
    </ion-button>
  </form>

  <div class="login__help-links">
    <!-- for implementing in future -->
    <!-- <a class="login__pass-recover-link">
        Forgot password?
      </a> -->
    <a
      @click="() => router.push('/registration')"
      class="login__pass-recover-link"
    >
      Create account
    </a>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeMount } from "vue";
import {
  IonButton,
  IonToolbar,
  IonIcon,
  IonHeader,
  IonSearchbar,
  IonItem,
  IonLabel,
  IonPopover,
  IonText,
  IonList,
  IonMenuButton,
  IonContent,
  IonInput,
  useIonRouter,
} from "@ionic/vue";
import {
  personCircle,
  heartOutline,
  desktopOutline,
  shirtOutline,
  homeOutline,
  mail,
  alertCircleOutline,
  lockClosed,
} from "ionicons/icons";
import { login, getUserData } from "@/api/api";
import { LogUserData } from "@/types/types";
import { useAuthStore } from "@/stores/auth";

const router = useIonRouter();
const user = ref<object>({});
const auth = useAuthStore();
const loginErrorMessage = ref<string>("");

const userData = ref<LogUserData>({
  email: "",
  password: "",
});

const focusOnInput = (inputId: string) => {
  const inputElement = document.getElementById(inputId)?.querySelector("input");
  if (inputElement) {
    inputElement.focus();
  }
};

const handleLogin = () => {
  loginErrorMessage.value = "";
  login(userData.value)
    .then((response: any) => {
      // updating auth store after login
      auth.getLoginStatus();
      if (!window.location.href.includes("/login")) {
        location.reload();
      }
    })
    .catch((error: any) => {
      if (error.response.status === 400) {
        loginErrorMessage.value = "Wrong username or password.";
      } else {
        console.log(error);
      }
    });
};
</script>

<style lang="scss">
.login__inputs {
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 10px;
}

.login__input-item {
  border-bottom: 1px solid lightgrey;
  margin: 0;
  --min-height: 40px;
}

.login__input-item::part(native) {
  padding-left: 10px;
}

.login__input-icon {
  margin: 0 10px 0 0;
  color: var(--ion-color-medium);
}

.login__input {
  margin: 0;
  border-radius: 3px;
  font-size: 14px;
  min-height: 40px !important;

  .native-wrapper {
    --border-width: 0;
  }
}

.login__form-error {
  display: flex;
  flex-direction: row;
  align-items: center;
  min-height: 13px;
  font-size: 13px;
  color: var(--ion-color-danger);
  gap: 2px;
}

.login__pass-recover-link {
  font-size: 14px;
  text-align: center;
  margin: 4px;
  cursor: pointer;
}

.login__help-links {
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
}

.login__button {
  margin: 10px 0 0 0;
  height: 40px;
}
</style>
