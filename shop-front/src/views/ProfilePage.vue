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

      <UnauthenticatedMessage v-if="!auth.isLoggedIn"></UnauthenticatedMessage>

      <div v-if="auth.isLoggedIn && userProfile" class="profile-info">
        <ion-card class="profile-info__card">
          <ion-text>
            <h1 class="card-title">Account information</h1>
          </ion-text>
          
          <div class="profile-info__inputs">
            <ion-item v-if="userProfile" class="input-item" lines="none">
              <ion-input
                v-model="userProfile.user.email"
                type="email"
                :disabled="true"
                placeholder="email@example.com"
                autocomplete="email"
                class="basic-input"
              >
              </ion-input>
              <ion-icon
                :icon="mail"
                slot="start"
                color="medium"
                class="input-icon"
              >
              </ion-icon>
              <div v-if="false" slot="start" class="required-field"></div>
            </ion-item>

            <ion-item v-if="userProfile" class="input-item" lines="none">
              <ion-input
                v-model="userProfile.name"
                type="text"
                :disabled="isNameEditing ? false : true"
                placeholder="Peter"
                @keydown.enter="handleProfileChange('name', userProfile.name)"
                autocomplete="given-name"
                class="basic-input"
              >
              </ion-input>
              <ion-icon
                :icon="personCircle"
                slot="start"
                color="medium"
                class="input-icon"
              >
              </ion-icon>
              <ion-button 
                slot="end"
                @click="handleProfileChange('name', userProfile.name)"
                :color="isNameEditing ? 'primary' : 'dark'"
                style="--border-radius: 0;"
              >{{ isNameEditing ? 'Save' : 'Edit' }}
              </ion-button>
            </ion-item>

            <ion-item v-if="userProfile" class="input-item" lines="none">
              <ion-input
                v-model="userProfile.phone"
                type="text"
                :disabled="isPhoneEditing ? false : true"
                placeholder="+1234567890"
                @keydown.enter="handleProfileChange('phone', userProfile.phone)"
                autocomplete="tel"
                class="basic-input"
              >
              </ion-input>
              <ion-icon
                :icon="phonePortraitOutline"
                slot="start"
                color="medium"
                class="input-icon"
              >
              </ion-icon>
              <ion-button 
                slot="end"                
                @click="handleProfileChange('phone', userProfile.phone)"
                :color="isPhoneEditing ? 'primary' : 'dark'"
                style="--border-radius: 0;"
              >{{ isPhoneEditing ? 'Save' : 'Edit' }}
              </ion-button>
            </ion-item>
          </div>
        </ion-card>

        <ion-card class="profile-info__card">
          <ion-text>
            <h1 class="card-title">Address</h1>
          </ion-text>
          
            <form  class="profile-info__inputs" @submit.prevent="handleAddressChange">
              <ion-item class="input-item" lines="none">
                <ion-input
                  id="firstName"
                  required
                  v-model="userAddress.first_name"
                  :disabled="isAddressEditing ? false : true"
                  type="text"
                  placeholder="Peter"
                  @keydown.enter="focusOnInput('lastName')"
                  autocomplete="given-name"
                  class="basic-input"
                >
                </ion-input>
                <ion-icon
                  :icon="personCircle"
                  slot="start"
                  color="medium"
                  class="input-icon"
                />
                <div v-if="isAddressEditing" slot="start" class="required-field"></div>
              </ion-item>
  
              <ion-item class="input-item" lines="none">
                <ion-input
                  id="lastName"
                  required
                  v-model="userAddress.last_name"
                  :disabled="isAddressEditing ? false : true"
                  :clearOnEdit="false"
                  type="text"
                  placeholder="Parker"
                  @keydown.enter="focusOnInput('company')"
                  autocomplete="family-name"
                  class="basic-input"
                >
                </ion-input>
                <ion-icon
                  :icon="personCircle"
                  slot="start"
                  color="medium"
                  class="input-icon"
                />
                <div v-if="isAddressEditing" slot="start" class="required-field"></div>
              </ion-item>
  
              <ion-item class="input-item" lines="none">
                <ion-input
                  id="company"
                  v-model="userAddress.company"
                  :disabled="isAddressEditing ? false : true"
                  :clearOnEdit="false"
                  type="text"
                  placeholder="Company Name"
                  @keydown.enter="focusOnInput('phone')"
                  autocomplete="organization"
                  class="basic-input"
                >
                </ion-input>
                <ion-icon
                  :icon="briefcaseOutline"
                  slot="start"
                  color="medium"
                  class="input-icon"
                />
              </ion-item>
  
              <ion-item class="input-item" lines="none">
                <ion-input
                  id="phone"
                  required
                  v-model="userAddress.phone"
                  :disabled="isAddressEditing ? false : true"
                  :clearOnEdit="false"
                  type="text"
                  placeholder="+1234567890"
                  @keydown.enter="focusOnInput('country')"
                  autocomplete="tel"
                  class="basic-input"
                >
                </ion-input>
                <ion-icon
                  :icon="phonePortraitOutline"
                  slot="start"
                  color="medium"
                  class="input-icon"
                />
                <div v-if="isAddressEditing" slot="start" class="required-field"></div>
              </ion-item>
  
              <ion-item class="input-item" lines="none">
                <ion-input
                  id="country"
                  required
                  v-model="userAddress.country"
                  :disabled="isAddressEditing ? false : true"
                  :clearOnEdit="false"
                  type="text"
                  placeholder="Poland"
                  @keydown.enter="focusOnInput('postCode')"
                  autocomplete="country-name"
                  class="basic-input"
                >
                </ion-input>
                <ion-icon
                  :icon="earthOutline"
                  slot="start"
                  color="medium"
                  class="input-icon"
                />
                <div v-if="isAddressEditing" slot="start" class="required-field"></div>
              </ion-item>
  
              <ion-item class="input-item" lines="none">
                <ion-input
                  id="postCode"
                  required
                  v-model="userAddress.post_code"
                  :disabled="isAddressEditing ? false : true"
                  :clearOnEdit="false"
                  type="text"
                  placeholder="12-345W"
                  @keydown.enter="focusOnInput('city')"
                  autocomplete="postal-code"
                  class="basic-input"
                >
                </ion-input>
                <ion-icon
                  :icon="mailOutline"
                  slot="start"
                  color="medium"
                  class="input-icon"
                />
                <div v-if="isAddressEditing" slot="start" class="required-field"></div>
              </ion-item>
  
              <ion-item class="input-item" lines="none">
                <ion-input
                  id="city"
                  required
                  v-model="userAddress.city"
                  :disabled="isAddressEditing ? false : true"
                  :clearOnEdit="false"
                  type="text"
                  placeholder="Warsaw"
                  @keydown.enter="focusOnInput('address')"
                  autocomplete="address-level2"
                  class="basic-input"
                >
                </ion-input>
                <ion-icon
                  :icon="businessOutline"
                  slot="start"
                  color="medium"
                  class="input-icon"
                />
                <div v-if="isAddressEditing" slot="start" class="required-field"></div>
              </ion-item>
  
              <ion-item class="input-item" lines="none">
                <ion-input
                  id="address"
                  required
                  v-model="userAddress.full_address"
                  :disabled="isAddressEditing ? false : true"
                  :clearOnEdit="false"
                  type="text"
                  placeholder="Bednarska 10/5"
                  @keydown.enter="handleAddressChange()"
                  autocomplete="street-address"
                  class="basic-input"
                >
                </ion-input>
                <ion-icon
                  :icon="homeOutline"
                  slot="start"
                  color="medium"
                  class="input-icon"
                />
                <div v-if="isAddressEditing" slot="start" class="required-field"></div>
              </ion-item>

              <ion-button
                  type="submit"
                  :color="isAddressEditing ? 'primary' : 'dark'"
                  expand="full"
                  class="standart-button"
                >
                  {{ isAddressEditing ? 'Save' : 'Edit' }}
                </ion-button>
            </form>
        </ion-card>

        <ion-card class="profile-info__card">
          <ion-text>
            <h1 class="card-title">Change password</h1>
          </ion-text>
          
          <form class="profile-info__inputs" @submit.prevent="handlePasswordChange">
            <ion-item class="input-item" lines="none">
              <ion-input
                id="currentPassword"
                v-model="newPassword.current_password"
                :clearOnEdit="false"
                type="password"
                placeholder="Current Password"
                @keydown.enter="focusOnInput('newPassword')"
                autocomplete="current-password"
                required
                class="basic-input"
              >
              </ion-input>
              <ion-icon
                :icon="lockClosed"
                slot="start"
                color="medium"
                class="input-icon"
              >
              </ion-icon>
            </ion-item>
            
            <ion-item class="input-item" lines="none">
              <ion-input
                id="newPassword"
                v-model="newPassword.new_password"
                :clearOnEdit="false"
                type="password"
                placeholder="New Password"
                @keydown.enter="focusOnInput('repeatPassword')"
                required
                class="basic-input"
              >
              </ion-input>
              <ion-icon
                :icon="lockClosed"
                slot="start"
                color="medium"
                class="input-icon"
              >
              </ion-icon>
            </ion-item>
  
            <ion-item class="input-item" lines="none">
              <ion-input
                id="repeatPassword"
                v-model="newPassword.repeat"
                :clearOnEdit="false"
                type="password"
                placeholder="Repeat New Password"
                @keydown.enter="handlePasswordChange()"
                required
                class="basic-input"
              >
              </ion-input>
              <ion-icon
                :icon="lockClosed"
                slot="start"
                color="medium"
                class="input-icon"
              >
              </ion-icon>
            </ion-item>

            <template v-for="message in passwordErrorMessage" :key="message">
              <div class="form-error">
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

            <ion-button
              type="submit"
              color="dark"
              expand="full"
              class="standart-button"
            >
              Change Password
            </ion-button>
          </form>
        </ion-card>
      </div>
    </ion-grid>
  </ion-page>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { IonPage, IonGrid, IonNote, IonText, IonIcon, IonCard, IonInput, IonButton, IonItem, onIonViewDidEnter } from "@ionic/vue";
import { alertCircleOutline, briefcaseOutline, businessOutline, call, earthOutline, homeOutline, lockClosed, mail, mailOutline, personCircle, personCircleOutline, phonePortrait, phonePortraitOutline } from "ionicons/icons";
import { useAuthStore } from "@/stores/auth";
import { getUserProfile, updateUserAddress, updateUserProfile, updateUserPassword } from "@/api/api";
import UnauthenticatedMessage from "@/components/UnauthenticatedMessage.vue";

const auth = useAuthStore();
const userProfile = ref<any>(null);
const userAddress = ref<any>(
  {
    "first_name": "",
    "last_name": "",
    "company": "",
    "phone": "",
    "country": "",
    "post_code": "",
    "city": "",
    "full_address": "",
  }
);
const newPassword = ref<any>(
  {
    current_password: '',
    new_password: '',
    repeat: '',
  }
);
const passwordErrorMessage = ref<Array<string>>([])
const isAddressEditing = ref<boolean>(false);
const isPhoneEditing = ref<boolean>(false);
const isNameEditing = ref<boolean>(false);

const focusOnInput = (inputId: string) => {
  const inputElement = document.getElementById(inputId)?.querySelector("input");
  if (inputElement) {
    inputElement.focus();
  }
};

const loadUserProfile = () => {
  getUserProfile()
    .then((response: any) => {
      userProfile.value = response.data;
      if (userProfile.value.current_address) {
        userAddress.value = userProfile.value.current_address;
      }
    })
    .catch((error: any) => {
      console.log(error);
    });
};

const handleAddressChange = () => {
  if (isAddressEditing.value) {
    updateUserAddress(userAddress.value)
    .then((response: any) => {
      isAddressEditing.value = false;
    })
    .catch((error: any) => {
      console.log(error);
    });
  } else {
    isAddressEditing.value = true;
  }
};

const handleProfileChange = (property: string, value: string) => {
  if (property === 'phone' && isPhoneEditing.value) {
    updateUserProfile({[property]: value})
    .then((response: any) => {
      isPhoneEditing.value = false;
    })
    .catch((error: any) => {
      console.log(error);
    });
  } else if (property === 'phone' && !isPhoneEditing.value) {
    isPhoneEditing.value = true;
  }

  if (property === 'name' && isNameEditing.value) {
    updateUserProfile({[property]: value})
    .then((response: any) => {
      isNameEditing.value = false;
    })
    .catch((error: any) => {
      console.log(error);
    });
  } else if (property === 'name' && !isNameEditing.value) {
    isNameEditing.value = true;
  }
};

const validatePassword = (): boolean => {
  if (!/[a-z]/.test(newPassword.value.new_password)) {
    passwordErrorMessage.value.push("Password should contain at least one lowercase letter.");
  }
  if (!/[A-Z]/.test(newPassword.value.new_password)) {
    passwordErrorMessage.value.push("Password should contain at least one uppercase letter.");
  }
  if (newPassword.value.new_password.length < 8) {
    passwordErrorMessage.value.push("Password should be at least 8 characters long.");
  }
  if (newPassword.value.new_password != newPassword.value.repeat) {
    passwordErrorMessage.value.push("Passwords do not match.");
  }

  return passwordErrorMessage.value.length > 0 ? false : true;
}

const handlePasswordChange = () => {
  passwordErrorMessage.value = [];
  if (validatePassword()) {
    updateUserPassword(newPassword.value)
    .then((response: any) => {
      location.reload();
    })
    .catch((error: any) => {
      console.log(error);
      if (error.response.status === 400) {
        passwordErrorMessage.value.push(error.response.data.message)
      }
    });
  }
};

onIonViewDidEnter(() => {
  loadUserProfile();
});
</script>

<style lang="scss">
.profile-info {
  display: flex;
  flex-direction: column;
  width: auto;
  gap: 15px;
  padding: 10px 8px 0px 8px;
}

.profile-info__card {
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 20px;
  margin: 0;
}

.profile-info__inputs {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.card-title {
  margin: 0 0 15px 0;
  color: black;
}
</style>
