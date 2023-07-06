<template>
  <ion-page class="scrollbar-active" mode="ios">
    <ion-grid :fixed="true" class="reg-page">
      <ion-text class="page-title">
        <ion-icon :icon="personAddOutline" size="large"></ion-icon>
        <h1 class="page-title--fixed-margin">Registration</h1>
      </ion-text>
      <template v-if="regStatus === 'pending'">
        <form class="reg-page__inputs" @submit.prevent="handleRegistration">
          <ion-item class="reg-page__input-item" lines="none">
            <ion-input
              v-model="userData.email"
              type="email"
              placeholder="email@example.com"
              @ionInput="handleInput('email')"
              @ionBlur="handleInput('email')"
              required
              class="reg-page__input"
            >
            </ion-input>
            <ion-icon
              :icon="mail"
              slot="start"
              :color="emailIconColor"
              class="reg-page__input-icon"
            >
            </ion-icon>
          </ion-item>

          <div v-if="emailInvalidMessage" class="reg-page__form-error">
            <ion-icon :icon="alertCircleOutline" slot="start" color="danger" />
            <div>
              {{ emailInvalidMessage }}
            </div>
          </div>

          <ion-item class="reg-page__input-item" lines="none">
            <ion-input
              v-model="userData.name"
              type="text"
              placeholder="Peter Parker"
              @ionInput="handleInput('name')"
              @ionBlur="handleInput('name')"
              required
              class="reg-page__input"
            >
            </ion-input>
            <ion-icon
              :icon="personCircle"
              slot="start"
              :color="nameIconColor"
              class="reg-page__input-icon"
            >
            </ion-icon>
          </ion-item>

          <div v-if="nameInvalidMessage" class="reg-page__form-error">
            <ion-icon :icon="alertCircleOutline" slot="start" color="danger" />
            <div>
              {{ nameInvalidMessage }}
            </div>
          </div>

          <ion-item class="reg-page__input-item" lines="none">
            <ion-input
              v-model="userData.password"
              :clearOnEdit="false"
              type="password"
              placeholder="Password"
              @ionInput="handleInput('password')"
              @ionBlur="handleInput('password')"
              required
              class="reg-page__input"
            >
            </ion-input>
            <ion-icon
              :icon="lockClosed"
              slot="start"
              :color="passwordIconColor"
              class="reg-page__input-icon"
            >
            </ion-icon>
          </ion-item>

          <ion-item class="reg-page__input-item" lines="none">
            <ion-input
              v-model="passwordRepeat"
              :clearOnEdit="false"
              type="password"
              placeholder="Repeat Password"
              @ionInput="handleInput('confirmPassword')"
              @ionBlur="handleInput('confirmPassword')"
              required
              class="reg-page__input"
            >
            </ion-input>
            <ion-icon
              :icon="lockClosed"
              slot="start"
              :color="passwordIconColor"
              class="reg-page__input-icon"
            >
            </ion-icon>
          </ion-item>

          <template v-for="message in passwordInvalidMessage" :key="message">
            <div class="reg-page__form-error">
              <ion-icon
                :icon="alertCircleOutline"
                slot="start"
                color="danger"
              />
              <div>
                {{ message }}
              </div>
            </div>
          </template>

          <div class="reg-page__terms-container">
            <div class="reg-page__terms-checkbox">
              <ion-checkbox
                class="terms-checkbox"
                v-model="termsChecked"
                @ionChange="handleInput('terms')"
                label-placement="end"
                justify="start"
                color="dark"
              ></ion-checkbox
              ><span
                >I agree to the
                <a class="terms-link" @click="setOpen(true)"
                  >Terms and Conditions</a
                ></span
              >
            </div>

            <div v-if="termsInvalidMessage" class="reg-page__form-error">
              <ion-icon
                :icon="alertCircleOutline"
                slot="start"
                color="danger"
              />
              <div>
                {{ termsInvalidMessage }}
              </div>
            </div>
          </div>

          <ion-button
            color="dark"
            expand="full"
            class="reg-page__reg-button"
            @click="handleRegistration"
          >
            Register
          </ion-button>
        </form>
      </template>

      <ion-modal :is-open="isOpen" mode="ios">
        <ion-header>
          <ion-toolbar>
            <ion-title>Terms and Conditions</ion-title>
            <ion-buttons slot="end">
              <ion-button @click="setOpen(false)">Close</ion-button>
            </ion-buttons>
          </ion-toolbar>
        </ion-header>
        <ion-content class="ion-padding terms-text">
          {{ termsAndConditions("E-Commerce") }}
        </ion-content>
      </ion-modal>

      <template v-if="regStatus === 'success'">
        <div class="reg-page__success-notif">
          <ion-icon
            :icon="checkmarkCircleOutline"
            class="reg-page__success-icon"
          ></ion-icon>
          <div class="reg-page__success-text">
            You have successfully registered!
          </div>
          <ion-button
            color="dark"
            expand="full"
            class="reg-page__login-button"
            @click="() => router.push('/profile')"
          >
            My Profile
          </ion-button>
        </div>
      </template>
    </ion-grid>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, Ref, ComputedRef, watch } from "vue";
import {
  IonItem,
  IonPage,
  IonGrid,
  IonButton,
  IonIcon,
  IonInput,
  IonCheckbox,
  IonModal,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonButtons,
  IonContent,
  useIonRouter,
} from "@ionic/vue";
import {
  personAddOutline,
  mail,
  lockClosed,
  personCircle,
  alertCircleOutline,
  checkmarkCircleOutline,
} from "ionicons/icons";
import { regUser } from "@/api/api";
import { RegUserData } from "@/types/types";
import { termsAndConditions } from "@/data/terms";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const router = useIonRouter();

const siteKey = "6LdO6yUmAAAAAMw1AnuEkKNDzZeT1KBQFTnnayA1";

const userData = ref<RegUserData>({
  email: "",
  name: "",
  password: "",
  captcha: "",
});
const passwordRepeat = ref("");
const termsChecked = ref(false);
const regStatus = ref("pending"); // pending, success, fail

const isOpen = ref(false);
function setOpen(newStatus: boolean) {
  isOpen.value = newStatus;
}

const isTouchedFields = ref({
  password: false,
  confirmPassword: false,
  email: false,
  name: false,
  terms: false,
});

const passwordsMatch = computed(
  () => userData.value.password === passwordRepeat.value
);
const emailMatch = computed(() => checkEmailSyntax(userData.value.email));
const isPasswordsTouched = computed(
  () => isTouchedFields.value.password && isTouchedFields.value.confirmPassword
);

const isPasswordValid = computed(() => {
  const password = userData.value.password;
  const isStrongEnough =
    password.length > 7 && /[a-z]/.test(password) && /[A-Z]/.test(password);
  return isPasswordsTouched.value && passwordsMatch.value && isStrongEnough;
});
const isPasswordInvalid = computed(() => {
  const password = userData.value.password;
  const isStrongEnough =
    password.length > 7 && /[a-z]/.test(password) && /[A-Z]/.test(password);
  return isPasswordsTouched.value && (!isStrongEnough || !passwordsMatch.value);
});
const isEmailValid = computed(
  () => isTouchedFields.value.email && emailMatch.value
);
const isEmailInvalid = computed(
  () => isTouchedFields.value.email && !emailMatch.value
);
const isNameValid = computed(
  () => isTouchedFields.value.name && userData.value.name.length > 2
);
const isNameInvalid = computed(
  () => isTouchedFields.value.name && userData.value.name.length < 3
);
const isTermsValid = computed(
  () => isTouchedFields.value.terms && termsChecked.value
);
const isTermsInvalid = computed(
  () => isTouchedFields.value.terms && !termsChecked.value
);

const emailInvalidMessage = computed(() =>
  isEmailInvalid.value ? "Email is not valid." : null
);
const nameInvalidMessage = computed(() =>
  isNameInvalid.value ? "Name is too short." : null
);
const passwordInvalidMessage = computed(() => {
  const errors: string[] = [];

  if (isPasswordInvalid.value) {
    if (!/[a-z]/.test(userData.value.password)) {
      errors.push("Password should contain at least one lowercase letter.");
    }
    if (!/[A-Z]/.test(userData.value.password)) {
      errors.push("Password should contain at least one uppercase letter.");
    }
    if (userData.value.password.length < 8) {
      errors.push("Password should be at least 8 characters long.");
    }
    if (!passwordsMatch.value) {
      errors.push("Passwords do not match.");
    }
  }

  return errors;
});
const termsInvalidMessage = computed(() =>
  isTermsInvalid.value
    ? "To finish registration you must agree to the Terms and Conditions."
    : null
);

const getIconColor = (isValid: any, isInvalid: any): string => {
  if (isValid.value) {
    return "success";
  }
  if (isInvalid.value) {
    return "danger";
  }
  return "medium";
};

const passwordIconColor = computed(() =>
  getIconColor(isPasswordValid, isPasswordInvalid)
);
const emailIconColor = computed(() =>
  getIconColor(isEmailValid, isEmailInvalid)
);
const nameIconColor = computed(() => getIconColor(isNameValid, isNameInvalid));

const checkEmailSyntax = (email: string) => {
  const emailRegex =
    /^(?=.{1,254}$)(?=.{1,64}@)[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
  return email.match(emailRegex);
};

const handleInput = (fieldName: string) => {
  switch (fieldName) {
    case "password":
      isTouchedFields.value.password = true;
      break;
    case "confirmPassword":
      isTouchedFields.value.confirmPassword = true;
      break;
    case "email":
      isTouchedFields.value.email = true;
      break;
    case "name":
      isTouchedFields.value.name = true;
      break;
    case "terms":
      isTouchedFields.value.terms = true;
      break;
    default:
      break;
  }
};

onMounted(() => {
  loadRecaptchaScript();
});

const loadRecaptchaScript = () => {
  const script = document.createElement("script");
  script.src = `https://www.google.com/recaptcha/api.js?render=${siteKey}`;
  document.head.appendChild(script);
};

function setAllFieldsToTrue(obj: Record<string, boolean>) {
  for (const key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      obj[key] = true;
    }
  }
}

const handleRegistration = () => {
  // mark all form fields as touched to trigger error messages if errors exist
  setAllFieldsToTrue(isTouchedFields.value);

  if (
    isPasswordValid.value &&
    isNameValid.value &&
    isEmailValid.value &&
    isTermsValid.value
  ) {
    executeRecaptcha();
  }
};

const executeRecaptcha = () => {
  grecaptcha.ready(() => {
    grecaptcha.execute(siteKey, { action: "submit" }).then((token) => {
      userData.value.captcha = token;
      handleRecaptchaResponse();
    });
  });
};

const handleRecaptchaResponse = () => {
  regUser(userData.value)
    .then((response: any) => {
      if (response.data.hasOwnProperty("id")) {
        regStatus.value = "success";
      }
    })
    .catch((error: any) => {
      console.log(error);
    });
};

// if user logged in - redirect him to the main page
watch(auth, () => {
  if (auth.isLoggedIn) {
    router.push("/");
  }
});
</script>

<style lang="scss">
.reg-page {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.reg-page__inputs {
  display: flex;
  flex-direction: column;
  padding: 0 20px 0 20px;
  width: 40%;
  gap: 6px;
  margin-top: 5px;
}

.reg-page__input-item {
  border: 1px solid lightgrey;
  margin: 0;
  border-radius: 3px;
}

.reg-page__input-item::part(native) {
  padding-left: 10px;
}

.reg-page__input-icon {
  margin-right: 10px;
}

.reg-page__input {
  margin: 0;
  border-radius: 3px;
  font-size: 15px;

  .native-wrapper {
    --border-width: 0;
  }
}

.reg-page__reg-button {
  margin: 0;
}

.reg-page__login-button {
  margin-top: 25px;
  width: 100%;
}

.reg-page__form-error {
  display: flex;
  flex-direction: row;
  align-items: center;
  min-height: 13px;
  font-size: 13px;
  color: var(--ion-color-danger);
  gap: 2px;
}

.reg-page__terms-container {
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin: 10px 0 10px 0;
}

.reg-page__terms-checkbox {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 10px;
  font-size: 15px;
}

ion-checkbox.terms-checkbox {
  --size: 24px;
}

ion-content.terms-text {
  white-space: pre-wrap;
  height: calc(100% - 44px);
}

a.terms-link {
  cursor: pointer;
}

ion-checkbox::part(container) {
  border-radius: 3px;
}

.g-recaptcha {
  display: flex;
  justify-content: center;
}

.reg-page__success-notif {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 10px;
  align-items: center;
  margin: 40px 0 40px 0;
  border-radius: 5px;
}

.reg-page__success-icon {
  height: 60px;
  width: 60px;
}

.reg-page__success-text {
  font-size: 19px;
  text-align: center;
}

@media (min-width: 1px) and (max-width: 576px) {
  .reg-page__inputs {
    width: 100%;
  }
}

@media (min-width: 577px) and (max-width: 991px) {
  .reg-page__inputs {
    width: 60%;
  }
}

@media (min-width: 992px) {
}
</style>
