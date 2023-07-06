<template>
  <ion-page class="scrollbar-active" mode="ios">
    <ion-grid :fixed="true">
      <ion-text class="page-title">
        <ion-icon :icon="receiptOutline" size="large"></ion-icon>
        <h1 class="page-title--fixed-margin">Checkout</h1>
      </ion-text>
      <div v-if="!cartItems.length" class="checkout__epmty">
        Nothing to checkout
      </div>
      <div v-if="cartItems.length" class="checkout">
        <div class="checkout__details">
          <ion-card class="details__address">
            <ion-text>
              <h1 class="details__title">Address</h1>
            </ion-text>
            <div class="address__data">
              <span>
                {{ userProfile.current_address?.first_name }}
                {{ userProfile.current_address?.last_name }}
                <span v-if="userProfile.current_address?.company"
                  >, {{ userProfile.current_address?.company }}</span
                >
              </span>

              <span>
                {{ userProfile.current_address?.full_address }}
              </span>

              <span>
                {{ userProfile.current_address?.post_code }}
                {{ userProfile.current_address?.city }},
                {{ userProfile.current_address?.country }}
              </span>

              <span>
                {{ userProfile.current_address?.phone }}
              </span>
            </div>

            <ion-button
              color="dark"
              fill="outline"
              class="standart-button details__button"
              @click="setModalOpen(true)"
              >Change address</ion-button
            >

            <ion-modal
              :is-open="isModalOpen"
              mode="ios"
              @willDismiss="setModalOpen(false)"
              class="address__modal"
            >
              <ion-header>
                <ion-toolbar>
                  <ion-title>Change address</ion-title>
                  <ion-buttons slot="end">
                    <ion-button @click="setModalOpen(false)">Close</ion-button>
                  </ion-buttons>
                </ion-toolbar>
              </ion-header>

              <form
                class="address__inputs"
                @submit.prevent="handleAddressChange"
              >
                <ion-item class="address__input-item" lines="none">
                  <ion-input
                    id="firstName"
                    required
                    v-model="addressData.first_name"
                    type="text"
                    placeholder="Peter"
                    @keydown.enter="focusOnInput('lastName')"
                    class="address__input"
                  >
                  </ion-input>
                  <ion-icon
                    :icon="personCircle"
                    slot="start"
                    class="address__input-icon"
                  />
                </ion-item>

                <ion-item class="address__input-item" lines="none">
                  <ion-input
                    id="lastName"
                    required
                    v-model="addressData.last_name"
                    :clearOnEdit="false"
                    type="text"
                    placeholder="Parker"
                    @keydown.enter="focusOnInput('company')"
                    class="address__input"
                  >
                  </ion-input>
                  <ion-icon
                    :icon="personCircle"
                    slot="start"
                    class="address__input-icon"
                  />
                </ion-item>

                <ion-item class="address__input-item" lines="none">
                  <ion-input
                    id="company"
                    v-model="addressData.company"
                    :clearOnEdit="false"
                    type="text"
                    placeholder="Company Name"
                    @keydown.enter="focusOnInput('phone')"
                    class="address__input"
                  >
                  </ion-input>
                  <ion-icon
                    :icon="briefcaseOutline"
                    slot="start"
                    class="address__input-icon"
                  />
                </ion-item>

                <ion-item class="address__input-item" lines="none">
                  <ion-input
                    id="phone"
                    required
                    v-model="addressData.phone"
                    :clearOnEdit="false"
                    type="text"
                    placeholder="+1234567890"
                    @keydown.enter="focusOnInput('country')"
                    class="address__input"
                  >
                  </ion-input>
                  <ion-icon
                    :icon="phonePortraitOutline"
                    slot="start"
                    class="address__input-icon"
                  />
                </ion-item>

                <ion-item class="address__input-item" lines="none">
                  <ion-input
                    id="country"
                    required
                    v-model="addressData.country"
                    :clearOnEdit="false"
                    type="text"
                    placeholder="Poland"
                    @keydown.enter="focusOnInput('postCode')"
                    class="address__input"
                  >
                  </ion-input>
                  <ion-icon
                    :icon="earthOutline"
                    slot="start"
                    class="address__input-icon"
                  />
                </ion-item>

                <ion-item class="address__input-item" lines="none">
                  <ion-input
                    id="postCode"
                    required
                    v-model="addressData.post_code"
                    :clearOnEdit="false"
                    type="text"
                    placeholder="12-345W"
                    @keydown.enter="focusOnInput('city')"
                    class="address__input"
                  >
                  </ion-input>
                  <ion-icon
                    :icon="mailOutline"
                    slot="start"
                    class="address__input-icon"
                  />
                </ion-item>

                <ion-item class="address__input-item" lines="none">
                  <ion-input
                    id="city"
                    required
                    v-model="addressData.city"
                    :clearOnEdit="false"
                    type="text"
                    placeholder="Warsaw"
                    @keydown.enter="focusOnInput('address')"
                    class="address__input"
                  >
                  </ion-input>
                  <ion-icon
                    :icon="businessOutline"
                    slot="start"
                    class="address__input-icon"
                  />
                </ion-item>

                <ion-item class="address__input-item" lines="none">
                  <ion-input
                    id="address"
                    required
                    v-model="addressData.full_address"
                    :clearOnEdit="false"
                    type="text"
                    placeholder="Bednarska 10/5"
                    @keydown.enter="handleAddressChange()"
                    class="address__input"
                  >
                  </ion-input>
                  <ion-icon
                    :icon="homeOutline"
                    slot="start"
                    class="address__input-icon"
                  />
                </ion-item>

                <ion-button
                  type="submit"
                  color="dark"
                  expand="full"
                  class="login__button"
                >
                  Save
                </ion-button>
              </form>
            </ion-modal>
          </ion-card>

          <ion-card class="details__shipping">
            <ion-text>
              <h1 class="details__title">Shipping</h1>
              <ion-radio-group v-model="shippingValue" class="shipping__list">
                <ion-radio
                  v-for="(method, index) in shippingMethods"
                  :value="index"
                  justify="start"
                  label-placement="end"
                  color="dark"
                  >{{ method.name }} - {{ method.price }} PLN</ion-radio
                >
              </ion-radio-group>
            </ion-text>
          </ion-card>

          <ion-card class="details__payment">
            <ion-text>
              <h1 class="details__title">Payment</h1>
              <ion-radio-group v-model="paymentValue" class="payments__list">
                <ion-radio
                  v-for="(method, index) in paymentMethods"
                  :value="index"
                  justify="start"
                  label-placement="end"
                  color="dark"
                >
                  {{ method.name }}
                  <img :src="method.logo" class="payment__logo" />
                </ion-radio>
              </ion-radio-group>
            </ion-text>
          </ion-card>
        </div>

        <div class="checkout__summary">
          <ion-card class="checkout-summary">
            <ion-text>
              <h1 class="checkout-summary__title">Summary</h1>
            </ion-text>

            <div class="checkout-summary__products">
              <span
                v-for="item in cartItems"
                class="checkout-summary__product-name"
              >
                {{ item.quantity }}x {{ item.product.name }}
              </span>
            </div>

            <ion-input
              label="Have a Promo Code?"
              placeholder="Enter Here!"
              label-placement="stacked"
              class="checkout-summary__promo"
            ></ion-input>

            <div class="checkout-summary__summary-labels">
              <div class="checkout-summary__info-label ion-hide-lg-down">
                <div>Subtotal</div>
                <div>{{ totalCost() }} {{ currency }}</div>
              </div>

              <div class="checkout-summary__info-label ion-hide-lg-down">
                <div>Shipping</div>
                <div>
                  {{ shippingMethods[shippingValue]?.price }} {{ currency }}
                </div>
              </div>

              <div class="checkout-summary__divider ion-hide-lg-down"></div>

              <div class="checkout-summary__info-label">
                <div>Total with shipping</div>
                <div>{{ toPayAmount() }} {{ currency }}</div>
              </div>
            </div>

            <ion-button
              color="dark"
              expand="full"
              class="standart-button"
              @click="newOrder()"
              >Make payment</ion-button
            >
          </ion-card>
        </div>
      </div>
    </ion-grid>
  </ion-page>
</template>

<script setup lang="ts">
import {
  IonPage,
  IonCard,
  IonRadio,
  IonRadioGroup,
  IonButton,
  IonGrid,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonInput,
  IonItem,
  IonText,
  onIonViewDidEnter,
  IonModal,
  IonButtons,
  IonIcon,
} from "@ionic/vue";

import {
  receiptOutline,
  businessOutline,
  personCircle,
  phonePortraitOutline,
  earthOutline,
  mailOutline,
  briefcaseOutline,
  homeOutline,
} from "ionicons/icons";
import { ref } from "vue";
import {
  getCartItems,
  getUserProfile,
  getShippingMethods,
  getPaymentMethods,
  createOrder,
  updateUserAddress,
} from "../api/api";
import { CartItems } from "../types/types";
const cartItems = ref<Array<CartItems>>([]);
const shippingMethods = ref<Array<any>>([]);
const shippingValue = ref<number>(0);
const paymentMethods = ref<Array<any>>([]);
const paymentValue = ref<number>(0);
const userProfile = ref<any>({});
const isModalOpen = ref<boolean>(false);
const addressData = ref<any>({});
let currency = "";

const totalCost = (): string => {
  let cost: number = 0;
  for (const element of cartItems.value) {
    const priceConverted: number = +element.product.price;
    cost += priceConverted * element.quantity;
  }
  return cost.toFixed(2);
};
const toPayAmount = (): string => {
  const cost: number = +totalCost();
  const shipping: number = +shippingMethods.value[shippingValue.value]?.price;

  return (cost + shipping).toFixed(2);
};

const setModalOpen = (value: boolean) => {
  isModalOpen.value = value;
  // assigning non reactive copy of userProfile property of empty object
  if (value) {
    addressData.value = JSON.parse(
      JSON.stringify(userProfile.value.current_address)
    );
  }
};

const focusOnInput = (inputId: string) => {
  const inputElement = document.getElementById(inputId)?.querySelector("input");
  if (inputElement) {
    inputElement.focus();
  }
};

const loadCartData = () => {
  getCartItems()
    .then((response: any) => {
      cartItems.value = response.data.cart;
      currency = response.data.currency;
    })
    .catch((error: any) => {
      console.log(error);
    });
};

const loadUserProfile = () => {
  getUserProfile()
    .then((response: any) => {
      userProfile.value = response.data;
    })
    .catch((error: any) => {
      console.log(error);
    });
};

const loadShipping = () => {
  getShippingMethods()
    .then((response: any) => {
      shippingMethods.value = response.data.results;
    })
    .catch((error: any) => {
      console.log(error);
    });
};

const loadPayments = () => {
  getPaymentMethods()
    .then((response: any) => {
      paymentMethods.value = response.data.results;
    })
    .catch((error: any) => {
      console.log(error);
    });
};

const newOrder = () => {
  const data = {
    shipping_method: shippingMethods.value[shippingValue.value].url,
    payment_method_id: paymentMethods.value[paymentValue.value].id,
  };

  createOrder(data)
    .then((response: any) => {
      window.location.replace(response.data.payment_url);
    })
    .catch((error: any) => {
      console.log(error);
    });
};

const handleAddressChange = () => {
  updateUserAddress(addressData.value)
    .then((response: any) => {
      userProfile.value.current_address = response.data;
      setModalOpen(false);
    })
    .catch((error: any) => {
      console.log(error);
    });
};

onIonViewDidEnter(() => {
  loadCartData();
  loadUserProfile();
  loadShipping();
  loadPayments();
});
</script>

<style lang="scss">
.checkout__details {
  display: flex;
  flex-direction: column;
  width: 70%;
  flex-grow: 1;
  padding: 10px 8px 0px 8px;
  gap: 15px;
}

.checkout {
  display: flex;
  width: auto;
}

ion-card.details__address,
ion-card.details__shipping,
ion-card.details__payment {
  margin: 0;
  padding: 20px;
}

.details__button {
  height: 30px;
  --border-radius: 0;
}

.address__data {
  display: flex;
  flex-direction: column;
  color: black;
}

.address__list,
.payments__list,
.shipping__list {
  display: flex;
  flex-direction: column;
  color: black;
  gap: 10px;
}

ion-radio {
  width: 2000px;
  height: 20px;
}

ion-radio::part(container) {
  width: 23px;
  height: 23px;
  border: 2px solid var(--ion-color-dark);
  border-radius: 50%;
}

.checkout__summary {
  width: 30%;
  padding: 10px 8px 10px 8px;
}

ion-card.checkout-summary {
  margin: 0;
  padding: 20px;
}

.checkout-summary__title,
.details__title {
  margin: 0 0 15px 0;
  color: black;
}

.checkout-summary__promo {
  border-bottom: 1px solid lightgrey;
  min-height: 46px;
  margin: 15px 0 20px 0;
}

.checkout-summary__products {
  display: flex;
  flex-direction: column;
}

.checkout-summary__product-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.checkout-summary__summary-labels {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.checkout-summary__info-label {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  color: black;
}

.checkout-summary__divider {
  height: 1px;
  background-color: lightgrey;
}

.checkout__epmty {
  width: 100%;
  text-align: center;
  padding: 35px;
}

.payment__logo {
  height: 10px;
  margin-left: 3px;
}

.address__modal {
  --height: auto;
  --width: 30%;
}

.address__inputs {
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 10px 30px 20px 30px;
}

.address__input-item {
  border-bottom: 1px solid lightgrey;
  margin: 0;
  --min-height: 40px;
}

.address__input-item::part(native) {
  padding-left: 10px;
}

.address__input-icon {
  margin: 0 10px 0 0;
  color: var(--ion-color-medium);
}

.address__input {
  display: flex;
  margin: 0;
  border-radius: 3px;
  font-size: 14px;
  min-height: 40px !important;
  align-items: center;

  .native-wrapper {
    --border-width: 0;
  }
}

@media (min-width: 1px) and (max-width: 991px) {
  .checkout {
    flex-direction: column;
  }

  .checkout__details {
    width: 100%;
  }

  .checkout__summary {
    width: 100%;
    margin-top: 15px;
    padding: 0px 8px 10px 8px;
  }

  .standart-button {
    height: 35px;
  }

  .address__modal {
    --height: 100%;
    --width: 100%;
  }
}

@media (min-width: 992px) {
}
</style>
