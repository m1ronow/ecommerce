<template>
  <ion-grid :fixed="true">
    <ion-row class="product-filters">
      <ion-list>
        <ion-item class="products-filter" color="light">
          <ion-select
            class="filter"
            value="apples"
            aria-label="Sorting"
            interface="popover"
            placeholder="Sorting"
          >
            <ion-select-option value="apples">Sorted by Time</ion-select-option>
            <ion-select-option value="oranges">Oranges</ion-select-option>
            <ion-select-option value="bananas">Bananas</ion-select-option>
          </ion-select>
        </ion-item>
      </ion-list>

      <ion-button class="button-filter" id="price-filter-trigger" color="light">
        <ion-text class="filter-text">Price</ion-text>
        <ion-icon slot="end" :icon="chevronExpand" size="small"></ion-icon>
      </ion-button>
      <ion-popover class="popover-filter" trigger="price-filter-trigger">
        <ion-list lines="full">
          <ion-item>
            <ion-input
              type="number"
              placeholder="Min Price"
              :clear-input="true"
            ></ion-input>
          </ion-item>
          <ion-item lines="full">
            <ion-input
              type="number"
              placeholder="Max Price"
              :clear-input="true"
            ></ion-input>
          </ion-item>
        </ion-list>
      </ion-popover>
    </ion-row>

    <ion-row class="products-layout">
      <ion-card v-for="(product, index) in products" class="product-card">
        <div class="product-image-container">
          <img class="product-image" :src="product.image" />
        </div>

        <ion-card-header>
          <ion-text class="product-card__price"
            >{{ product.price }} {{ currency }}</ion-text
          >
          <ion-text class="product-card__name">{{ product.name }}</ion-text>
        </ion-card-header>

        <ion-card-content>
          {{ product.description }}
        </ion-card-content>

        <ion-buttons class="product-buttons">
          <ion-button
            @click="
              product.in_cart
                ? deleteFromCart(product.id, index)
                : addToCart(product.url, index)
            "
            fill="clear"
            color="primary"
          >
            <ion-icon
              slot="icon-only"
              :icon="product.in_cart ? bagRemove : bagAddOutline"
            ></ion-icon>
          </ion-button>

          <ion-button
            @click="
              product.in_favorites
                ? deleteFromFavorites(product.id, index)
                : addToFavorites(product.url, index)
            "
            fill="clear"
            color="danger"
          >
            <ion-icon
              slot="icon-only"
              :icon="product.in_favorites ? heartDislike : heartOutline"
            ></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-card>
    </ion-row>
  </ion-grid>
</template>

<script setup lang="ts">
import {
  IonGrid,
  IonRow,
  IonCard,
  IonCardContent,
  IonCardHeader,
  IonButton,
  IonButtons,
  IonIcon,
  IonInput,
  IonItem,
  IonSelectOption,
  IonSelect,
  IonList,
  IonText,
  IonPopover,
  useIonRouter,
  onIonViewDidEnter,
  onIonViewWillEnter,
} from "@ionic/vue";
import {
  bagAddOutline,
  heartOutline,
  chevronExpand,
  bagRemove,
  heartDislike,
} from "ionicons/icons";
import { watch } from "vue";
import {
  addCartItem,
  deleteCartItems,
  addFavoriteItem,
  deleteFavoriteItems,
} from "@/api/api";
import { Product } from "@/types/types";
import { useAuthStore } from "@/stores/auth";

const router = useIonRouter();
const auth = useAuthStore();
const props = defineProps<{
  products: Array<Product>;
  currency?: string;
}>();

const addToCart = (product: string, productIndex: number) => {
  if (auth.isLoggedIn) {
    const cartItem = {
      product,
    };
    addCartItem(cartItem)
      .then((response: any) => {
        if (response.status) {
          props.products[productIndex].in_cart = true;
        }
      })
      .catch((error: any) => {
        console.log(error);
      });
  } else {
    router.push("/login");
  }
};

const deleteFromCart = (itemId: number, productIndex: number) => {
  deleteCartItems([itemId])
    .then((response: any) => {
      if (response.data.deleted_count) {
        props.products[productIndex].in_cart = false;
      }
    })
    .catch((error: any) => {
      console.log(error);
    });
};

const addToFavorites = (product: string, productIndex: number) => {
  if (auth.isLoggedIn) {
    const cartItem = {
      product,
    };
    addFavoriteItem(cartItem)
      .then((response: any) => {
        if (response.status) {
          props.products[productIndex].in_favorites = true;
        }
      })
      .catch((error: any) => {
        console.log(error);
      });
  } else {
    router.push("/login");
  }
};

const deleteFromFavorites = (itemId: number, productIndex: number) => {
  deleteFavoriteItems([itemId])
    .then((response: any) => {
      if (response.data.deleted_count) {
        props.products[productIndex].in_favorites = false;
      }
    })
    .catch((error: any) => {
      console.log(error);
    });
};
</script>

<style lang="scss">
ion-searchbar.custom {
  padding: 0;
}

ion-card.product-card {
  margin: 0;
}

ion-item.products-filter {
  --border-radius: 25px;
  --inner-border-width: 0;
  --min-height: 32px;
}

ion-select.filter {
  min-height: 32px;
}

ion-popover.popover-filter {
  margin-top: -6.5px;
}

ion-card-header {
  color: black;
  gap: 10px;
}

ion-text.product-card__price {
  font-size: 22px;
}

ion-text.product-card__name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 17px;
}

div.product-image-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 180px;

  border-bottom: 0.1rem solid lightgrey;
}

img.product-image {
  height: auto;
  max-height: 96%;
}

ion-row.products-layout {
  display: flex;
  flex-wrap: wrap;
  column-gap: 2%;
  row-gap: 1rem;
}

ion-buttons.product-buttons {
  margin: 0 0 20px 12px;
}

ion-row.product-filters {
  padding: 5px 0 10px 0;
  column-gap: 10px;
  row-gap: 5px;
}

ion-button.button-filter {
  margin: 0;
  max-height: 32px;
  --border-radius: 25px;
}

ion-text.filter-text {
  font-weight: 400;
}

@media (min-width: 1px) and (max-width: 576px) {
  ion-row.products-layout > * {
    flex: 0 0 95%;
  }

  ion-row.products-layout {
    justify-content: center;
  }

  ion-row.product-filters {
    padding: 5px 2% 10px 2%;
  }
}

@media (min-width: 577px) and (max-width: 991px) {
  ion-row.products-layout > * {
    flex: 0 0 49%;
  }
}

@media (min-width: 992px) {
  ion-row.products-layout > * {
    flex: 0 0 32%;
  }
}
</style>
