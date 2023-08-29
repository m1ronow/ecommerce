<template>
  <ion-button
    class="header-button"
    :id="clickTrigger"
    fill="clear"
    color="medium"
  >
    <ion-icon slot="icon-only" :icon="personCircle"></ion-icon>
  </ion-button>
  <ion-popover
    mode="ios"
    class="popover-user-profile"
    :trigger="clickTrigger"
    trigger-action="click"
  >
    <login-form v-if="!auth.isLoggedIn"></login-form>

    <div v-if="auth.isLoggedIn">
      Name: {{ user.name }}

      <ion-button
        color="dark"
        expand="full"
        class="login__button"
        @click="handleLogout()"
      >
        Log Out
      </ion-button>
    </div>
  </ion-popover>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import {
  IonButton,
  IonIcon,
  IonPopover,
} from "@ionic/vue";
import {
  personCircle,
} from "ionicons/icons";
import LoginForm from "@/components/LoginForm.vue";
import { getUserData, logout } from "@/api/api";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const user = ref<any>({});

// need it because the trigger must have different name for each component instance
const props = defineProps({
  clickTrigger: String,
});

const handleLogout = () => {
  logout()
    .then((response: any) => {
      // updating auth store after logout
      auth.getLoginStatus();
      location.reload();
    })
    .catch((error: any) => {
      console.log(error);
    });
};

watch(auth, () => {
  if (auth.isLoggedIn) {
    getUserData()
      .then((response: any) => {
        user.value = response.data;
      })
      .catch((error: any) => {
        console.log(error);
      });
  }
});
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

ion-searchbar.custom {
  padding: 0;
}

ion-popover.popover-user-profile {
  margin-top: -11.5px;
  --width: 270px;
}

ion-col.header-nav-buttons {
  display: flex;
  justify-content: flex-end;
}

ion-button.button-category {
  margin: 0;
  max-height: 32px;
  --border-radius: 25px;
}

ion-list.user-popover-list {
  padding: 0;
}

div.toolbar-divider {
  height: 0.55px;
  background-color: var(
    --ion-toolbar-border-color,
    var(--ion-border-color, var(--ion-color-step-150, rgba(0, 0, 0, 0.2)))
  );
}

div.logo {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 0.4rem;
}

@media (min-width: 1px) and (max-width: 576px) {
  ion-button.header-button {
    --padding-start: 6px;
    --padding-end: 6px;
    margin-top: 0;
    margin-bottom: 0;
  }
}

@media (min-width: 577px) and (max-width: 991px) {
  ion-toolbar.main-toolbar {
    --border-style: solid;
    --border-color: var(
      --ion-toolbar-border-color,
      var(--ion-border-color, var(--ion-color-step-150, rgba(0, 0, 0, 0.2)))
    );
    --border-width: 0 0 0.55px 0;
  }
}

@media (min-width: 992px) {
  ion-toolbar.main-toolbar {
    --border-style: solid;
    --border-color: var(
      --ion-toolbar-border-color,
      var(--ion-border-color, var(--ion-color-step-150, rgba(0, 0, 0, 0.2)))
    );
    --border-width: 0 0 0.55px 0;
  }
}
</style>
