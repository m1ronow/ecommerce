<template>
  <ion-page class="scrollbar-active" mode="ios">
    <ion-grid :fixed="true">
      <ion-text class="page-title">
        <ion-icon
          :icon="bagHandleOutline"
          size="large"
          aria-hidden="true"
        ></ion-icon>
        <h1 class="page-title--fixed-margin">My Cart</h1>
      </ion-text>

      <UnauthenticatedMessage v-if="!auth.isLoggedIn"></UnauthenticatedMessage>

      <div
        v-if="!cartItems.length && auth.isLoggedIn"
        class="cart-content__epmty"
      >
        Cart is empty
      </div>
      <div v-if="cartItems.length && auth.isLoggedIn" class="cart-content">
        <div class="cart-content__products">
          <ion-card v-for="(item, index) in cartItems" class="cart-product">
            <div class="cart-product__container">
              <div class="cart-product__basic-info">
                <div class="cart-product__image-container">
                  <img class="cart-product__image" :src="item.product.image" />
                </div>

                <ion-card-header>
                  <ion-text class="cart-product__name">{{
                    item.product.name
                  }}</ion-text>
                </ion-card-header>
              </div>

              <div class="cart-product__price-info">
                <div class="cart-product__quantity-input">
                  <vue-number-input
                    v-model="item.quantity"
                    :min="1"
                    :max="1000"
                    size="small"
                    center
                    controls
                  ></vue-number-input>
                </div>
                <div class="cart-product__price-fields">
                  <ion-text class="cart-product__total-price">
                    {{
                      productPriceSummary(item.product?.price, item.quantity)
                    }}
                    {{ currency }}
                  </ion-text>
                  <ion-text
                    v-if="item.quantity > 1"
                    class="cart-product__single-price"
                  >
                    {{ item.product?.price }} {{ currency }}
                  </ion-text>
                </div>
              </div>

              <div class="cart-product__remove-button-container">
                <ion-button
                  @click="handleItemDelete(item.product.id, index)"
                  fill="clear"
                  color="medium"
                  class="cart-product__remove-product-button"
                >
                  <ion-icon
                    slot="icon-only"
                    :icon="trashOutline"
                    style="height: 20px"
                  ></ion-icon>
                </ion-button>
              </div>
            </div>
          </ion-card>
        </div>

        <div class="cart-content__summary">
          <ion-card class="cart-summary">
            <ion-text class="ion-hide-lg-down">
              <h1 class="cart-summary__title">Summary</h1>
            </ion-text>

            <div class="cart-summary__summary-labels">
              <div class="cart-summary__info-label ion-hide-lg-down">
                <div>Subtotal</div>
                <div>{{ totalCost() }} {{ currency }}</div>
              </div>

              <div class="cart-summary__info-label ion-hide-lg-down">
                <div>Shipping</div>
                <div>{{ shippingCost }} {{ currency }}</div>
              </div>

              <div class="cart-summary__divider ion-hide-lg-down"></div>

              <div class="cart-summary__info-label">
                <div>Total with shipping</div>
                <div>{{ toPayAmount() }} {{ currency }}</div>
              </div>
            </div>

            <ion-button
              color="dark"
              expand="full"
              class="standart-button"
              @click="handleCheckoutRedirect()"
              >Checkout</ion-button
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
  IonCardHeader,
  IonButton,
  IonGrid,
  IonText,
  IonIcon,
  onIonViewDidEnter,
  useIonRouter,
} from "@ionic/vue";
import { bagHandleOutline, trashOutline } from "ionicons/icons";
import VueNumberInput from "@chenfengyuan/vue-number-input";
import { ref, computed } from "vue";
import {
  getCartItems,
  getShippingMethods,
  deleteCartItems,
  updateCartQuantity,
} from "../api/api";
import UnauthenticatedMessage from "@/components/UnauthenticatedMessage.vue";
import { CartItems } from "../types/types";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const router = useIonRouter();
const cartItems = ref<Array<CartItems>>([]);
const shippingMethods = ref<Array<any>>([]);
let currency = "";
const shippingCost = computed(() => shippingMethods.value[0]?.price);
const productPriceSummary = (price: string, quantity: number): string => {
  const priceConverted: number = +price; // converting string to number
  // calculates total price, rounds by 2 decimals, toFixed keeps 2 decimals even if they are zeros
  return (
    Math.round((priceConverted * quantity + Number.EPSILON) * 100) / 100
  ).toFixed(2);
};
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
  const shipping: number = +shippingCost.value;

  return (cost + shipping).toFixed(2);
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

const loadShipping = () => {
  getShippingMethods()
    .then((response: any) => {
      shippingMethods.value = response.data.results;
    })
    .catch((error: any) => {
      console.log(error);
    });
};

const handleItemDelete = (itemId: number, itemIndex: number) => {
  deleteCartItems([itemId])
    .then((response: any) => {
      if (response.data.deleted_count) {
        cartItems.value.splice(itemIndex, 1);
      }
    })
    .catch((error: any) => {
      console.log(error);
    });
};

const handleCheckoutRedirect = () => {
  updateCartQuantity(cartItems.value)
    .then((response: any) => {
      if (response.data.updated_count) {
        router.push("/checkout");
      }
    })
    .catch((error: any) => {
      console.log(error);
    });
};

onIonViewDidEnter(() => {
  loadCartData();
  loadShipping();
});
</script>

<style lang="scss">
.cart-content__products {
  width: 70%;
  flex-grow: 1;
}

.cart-content__epmty {
  width: 100%;
  text-align: center;
  padding: 35px;
}

.product__price-details {
  display: flex;
  flex-grow: 1;
  flex-direction: row;
  align-items: center;
  gap: 10px;
  justify-content: flex-end;
}

.cart-product__remove-product-button {
  --padding-start: 4px;
  --padding-end: 4px;
  margin-top: 0;
  margin-bottom: 0;
}

.cart-content {
  display: flex;
  width: auto;
}

ion-card.cart-product {
  margin: 10px 8px 10px 8px;
}

.cart-product__container {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 0 10px 0 10px;
  height: 100px;
}

.cart-product__basic-info {
  flex-basis: 50%;
  min-width: 50%;
  width: 50%;
  display: flex;
  align-items: center;
}

.cart-product__image-container {
  display: flex;
  width: 92px;
  min-width: 92px;
  height: 92px;
  justify-content: center;
  align-items: center;
}

.cart-product__image {
  object-fit: scale-down;
  height: inherit;
  width: inherit;
}

ion-text.cart-product__name {
  word-wrap: break-word;
  word-break: break-all;
  font-size: 12pt;
  color: black;
}

ion-card-header {
  padding: 15px;
}

.cart-product__price-info {
  display: flex;
  align-items: center;
  flex-basis: 40%;
  min-width: 40%;
  width: 40%;
}

.cart-product__quantity-input {
  flex-basis: 110px;
  min-width: 110px;
  width: 110px;
  margin: 0 15px 0 15px;
}

vue-number-input {
  width: 110px;
}

.cart-product__price-fields {
  position: relative;
}

.cart-product__total-price {
  position: relative;
  top: 0;
  left: 0;
  color: black;
}

.cart-product__single-price {
  position: absolute;
  top: 100%;
  left: 0;
  font-size: 11px;
}

.cart-product__remove-button-container {
  display: flex;
  flex-grow: 1;
  justify-content: flex-end;
}

.cart-content__summary {
  width: 30%;
}

ion-card.cart-summary {
  margin: 10px 8px 10px 8px;
  padding: 20px;
}

.cart-summary__title {
  margin: 0 0 15px 0;
  color: black;
}

.cart-summary__promo {
  border-bottom: 1px solid lightgrey;
  min-height: 46px;
  margin: 15px 0 20px 0;
}

.cart-summary__summary-labels {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.cart-summary__info-label {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  color: black;
}

.cart-summary__divider {
  height: 1px;
  background-color: lightgrey;
}

.router-link {
  cursor: pointer;
}

@media (min-width: 1px) and (max-width: 991px) {
  .cart-content {
    display: inline;
  }

  .cart-content__products {
    display: inline;
  }

  .cart-product__container {
    height: auto;
  }

  .cart-product__basic-info {
    flex-basis: 100%;
    min-width: 100%;
    width: 100%;
    padding: 10px 20px 0 0;
  }

  .cart-product__image-container {
    width: 75px;
    min-width: 75px;
    height: 75px;
  }

  .cart-product__price-info {
    flex-basis: 100%;
    min-width: 100%;
    width: 100%;
    justify-content: space-between;
    margin-top: 10px;
    margin-bottom: 10px;
  }

  .cart-product__quantity-input {
    margin: 0;
  }

  .cart-product__remove-button-container {
    position: absolute;
    right: 0.5rem;
    top: 20px;
  }

  .cart-content__summary {
    display: inline;
    position: sticky;
    bottom: 1rem;
  }

  .standart-button {
    height: 35px;
  }

  .cart-product__container {
    flex-direction: column;
  }
}

@media (min-width: 992px) {
}
</style>
