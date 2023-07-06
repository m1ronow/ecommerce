<template>
  <ion-page class="scrollbar-active" mode="ios">
    <ion-grid :fixed="true">
      <ion-text class="page-title">
        <ion-icon
          :icon="heartOutline"
          size="large"
          aria-hidden="true"
        ></ion-icon>
        <h1 class="page-title--fixed-margin">Favorites</h1>
      </ion-text>
      <div v-if="!auth.isLoggedIn" class="favorites-content__epmty">
        Please,
        <a @click="() => router.push('/login')" class="router-link">log in</a>
        or
        <a @click="() => router.push('/registration')" class="router-link"
          >register</a
        >
      </div>

      <div
        v-if="!favoriteItems.length && auth.isLoggedIn"
        class="favorites-content__epmty"
      >
        No favorites
      </div>

      <div
        v-if="favoriteItems.length && auth.isLoggedIn"
        class="favorites-content"
      >
        <div class="favorites-content__products">
          <ion-card
            v-for="(item, index) in favoriteItems"
            class="favorites-product"
          >
            <div class="favorites-product__container">
              <div class="favorites-product__basic-info">
                <div class="favorites-product__image-container">
                  <img
                    class="favorites-product__image"
                    :src="item.product.image"
                  />
                </div>

                <ion-card-header>
                  <ion-text class="favorites-product__name">{{
                    item.product.name
                  }}</ion-text>
                </ion-card-header>
              </div>

              <div class="favorites-product__price-info">
                <div class="favorites-product__price-fields">
                  <ion-text class="favorites-product__total-price">
                    {{ item.product?.price }} {{ currency }}
                  </ion-text>
                </div>
              </div>

              <div class="favorites-product__button-container">
                <ion-button
                  @click="
                    item.product.in_cart
                      ? handleDeleteFromCart(item.product.id, index)
                      : handleAddToCart(item.product.url, index)
                  "
                  fill="clear"
                  color="primary"
                  class="favorites-product__to-cart-button"
                >
                  <ion-icon
                    slot="icon-only"
                    :icon="item.product.in_cart ? bagCheck : bagAddOutline"
                    style="height: 20px"
                  ></ion-icon>
                </ion-button>

                <ion-button
                  @click="handleItemDelete(item.product.id, index)"
                  fill="clear"
                  color="medium"
                  class="favorites-product__remove-button"
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
import {
  bagAddOutline,
  bagCheck,
  heartOutline,
  trashOutline,
} from "ionicons/icons";
import { ref } from "vue";
import {
  getFavoriteItems,
  deleteFavoriteItems,
  addCartItem,
  deleteCartItems,
} from "../api/api";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const router = useIonRouter();
const favoriteItems = ref<Array<any>>([]);
let currency = "";

const loadFavoritesData = () => {
  getFavoriteItems()
    .then((response: any) => {
      favoriteItems.value = response.data.favorites;
      currency = response.data.currency;
    })
    .catch((error: any) => {
      console.log(error);
    });
};

const handleItemDelete = (itemId: number, itemIndex: number) => {
  deleteFavoriteItems([itemId])
    .then((response: any) => {
      if (response.data.deleted_count) {
        favoriteItems.value.splice(itemIndex, 1);
      }
    })
    .catch((error: any) => {
      console.log(error);
    });
};

const handleAddToCart = (product: string, productIndex: number) => {
  const cartItem = {
    product,
  };
  addCartItem(cartItem)
    .then((response: any) => {
      if (response.status) {
        favoriteItems.value[productIndex].product.in_cart = true;
      }
    })
    .catch((error: any) => {
      console.log(error);
    });
};

const handleDeleteFromCart = (itemId: number, productIndex: number) => {
  deleteCartItems([itemId])
    .then((response: any) => {
      if (response.data.deleted_count) {
        favoriteItems.value[productIndex].product.in_cart = false;
      }
    })
    .catch((error: any) => {
      console.log(error);
    });
};

onIonViewDidEnter(() => {
  loadFavoritesData();
});
</script>

<style lang="scss">
.favorites-content__products {
  width: 70%;
  flex-grow: 1;
}

.product__price-details {
  display: flex;
  flex-grow: 1;
  flex-direction: row;
  align-items: center;
  gap: 10px;
  justify-content: flex-end;
}

.favorites-product__remove-button,
.favorites-product__to-cart-button {
  --padding-start: 0px;
  --padding-end: 0px;
  margin-top: 0;
  margin-bottom: 0;
}

.favorites-content {
  display: flex;
  width: auto;
}

ion-card.favorites-product {
  margin: 10px 8px 10px 8px;
}

.favorites-product__container {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 0 10px 0 10px;
  height: 100px;
}

.favorites-product__basic-info {
  flex-basis: 70%;
  min-width: 70%;
  width: 70%;
  display: flex;
  align-items: center;
}

.favorites-product__image-container {
  display: flex;
  width: 92px;
  min-width: 92px;
  height: 92px;
  justify-content: center;
  align-items: center;
}

.favorites-product__image {
  object-fit: scale-down;
  height: inherit;
  width: inherit;
}

ion-text.favorites-product__name {
  word-wrap: break-word;
  word-break: break-all;
  font-size: 12pt;
  color: black;
}

ion-card-header {
  padding: 15px;
}

.favorites-product__price-info {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  flex-basis: 20%;
  min-width: 20%;
  width: 20%;
}

.favorites-product__price-fields {
  position: relative;
}

.favorites-product__total-price {
  position: relative;
  top: 0;
  left: 0;
  color: black;
}

.favorites-product__button-container {
  display: flex;
  flex-grow: 1;
  justify-content: flex-end;
  gap: 10px;
}

.favorites-content__summary {
  width: 30%;
}

.favorites-content__epmty {
  width: 100%;
  text-align: center;
  padding: 35px;
}

.router-link {
  cursor: pointer;
}

@media (min-width: 1px) and (max-width: 991px) {
  .favorites-content {
    display: inline;
  }

  .favorites-content__products {
    display: inline;
  }

  .favorites-product__container {
    height: auto;
  }

  .favorites-product__basic-info {
    flex-basis: 100%;
    min-width: 100%;
    width: 100%;
    padding: 10px 20px 0 0;
  }

  .favorites-product__image-container {
    width: 75px;
    min-width: 75px;
    height: 75px;
  }

  .favorites-product__price-info {
    flex-basis: 100%;
    min-width: 100%;
    width: 100%;
    justify-content: flex-start;
    margin-top: 10px;
    margin-bottom: 10px;
    padding-left: 15px;
  }

  .favorites-product__price-fields {
    margin-left: 75px;
  }

  .favorites-product__button-container {
    flex-direction: column;
    position: absolute;
    right: 0.5rem;
    height: 100%;
    justify-content: space-evenly;
  }

  .favorites-product__remove-button,
  .favorites-product__to-cart-button {
    height: 22px;
  }

  .favorites-content__summary {
    display: inline;
    position: sticky;
    bottom: 1rem;
  }

  .standart-button {
    height: 35px;
  }

  .favorites-product__container {
    flex-direction: column;
  }
}

@media (min-width: 992px) {
}
</style>
