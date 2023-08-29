<template>
  <ion-grid :fixed="true">
    <ion-row class="product-filters">
      <ion-list>
        <ion-item class="products-filter" color="light">
          <ion-select
            class="filter"
            v-model="filterParams.orderBy"
            @ionChange="handleFilterChange('order_by', filterParams.orderBy)"
            aria-label="Sorting"
            label="Sort by:"
            interface="popover"
          >
            <ion-select-option value="">New</ion-select-option>
            <ion-select-option value="updated_at">Old</ion-select-option>
            <ion-select-option value="price">Price: Low to High</ion-select-option>
            <ion-select-option value="-price">Price: High to Low</ion-select-option>
            <ion-select-option value="name">Name</ion-select-option>
          </ion-select>
        </ion-item>
      </ion-list>

      <ion-button class="button-filter" id="price-filter-trigger" color="light">
        <ion-text class="filter-text">Price</ion-text>
        <ion-icon slot="end" :icon="chevronExpand" size="small"></ion-icon>
      </ion-button>
      <ion-popover class="popover-filter" trigger="price-filter-trigger">
        <ion-list class="popover-filter__list" lines="none">
          <ion-item class="popover-filter__item">
            <ion-input
              class="popover-filter__input"
              v-model="filterParams.minPrice"
              type="number"
              placeholder="Min Price"
              min="0"
              :clear-input="true"
              @ion-blur="handleFilterChange('min_price', filterParams.minPrice)"
            ></ion-input>
          </ion-item>
          <ion-item class="popover-filter__item">
            <ion-input
              class="popover-filter__input"
              v-model="filterParams.maxPrice"
              type="number"
              placeholder="Max Price"
              min="0"
              :clear-input="true"
              @ion-blur="handleFilterChange('max_price', filterParams.maxPrice)"
            ></ion-input>
          </ion-item>
        </ion-list>
      </ion-popover>
    </ion-row>
    
    <ion-row v-if="products?.length < 1" class="products-empty">
      Nothing found
    </ion-row>
    <ion-row v-if="products?.length > 0" class="products-layout">
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

        <div class="product-card__description">
          {{ product.description }}
        </div>

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

    <ion-row class="paginatiom">
      <ion-button class="pagination__button color-white" fill="solid" color="medium" :disabled="route.query.page && parseInt(route.query.page.toString()) > 1 ? false : true">&lt;</ion-button>
      <ion-button class="pagination__button" fill="outline" color="tertiary">1</ion-button>
      <ion-button class="pagination__button" fill="outline" color="medium">2</ion-button>
      <ion-button class="pagination__button" fill="outline" color="medium">3</ion-button>
      <div class="pagination__dots">...</div>
      <ion-button class="pagination__button" fill="outline" color="medium">9</ion-button>
      <ion-button class="pagination__button" fill="outline" color="medium">10</ion-button>
      <ion-button class="pagination__button" fill="outline" color="medium">11</ion-button>
      <ion-button class="pagination__button color-white" fill="solid" color="medium" :disabled="route.query.page && parseInt(route.query.page.toString()) === [].length ? true : false">&gt;</ion-button>
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
  IonRadio,
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
import { ref, reactive, toRef, watch, computed } from "vue";
import {
  addCartItem,
  deleteCartItems,
  addFavoriteItem,
  deleteFavoriteItems,
} from "@/api/api";
import { Product } from "@/types/types";
import { useAuthStore } from "@/stores/auth";
import { useRoute } from "vue-router";

const router = useIonRouter();
const route = useRoute();
const auth = useAuthStore();
const props = defineProps<{
  productsData: any;
}>();
const products = ref<Array<any>>([]);
const currency = ref<string>('');
watch(props, () => {
  products.value = props.productsData.results.data;
  currency.value = props.productsData.results.currency;
})
const filterParams = computed<any>(() => {
  return {
    orderBy: route.query.order_by ? route.query.order_by : "",
    minPrice: route.query.min_price ? route.query.min_price : "",
    maxPrice: route.query.max_price ? route.query.max_price : "",
  }
});

const handleFilterChange = (param: string, value: string) => {
  if (value) {
    router.push({ query: { ...route.query, [param]: value } });
  } else {
    let {[param]: _, ...updatedQuery} = route.query;  // updatedQuery is route.query object without param
    router.push({ query: updatedQuery });
  }
}

const addToCart = (product: string, productIndex: number) => {
  if (auth.isLoggedIn) {
    const cartItem = {
      product,
    };
    addCartItem(cartItem)
      .then((response: any) => {
        if (response.status) {
          products.value[productIndex].in_cart = true;
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
        products.value[productIndex].in_cart = false;
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
          products.value[productIndex].in_favorites = true;
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
        products.value[productIndex].in_favorites = false;
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
  height: 380px;
}

ion-item {
  --inner-border-width: 0;
  border-bottom: 1px solid lightgray;
}

ion-item.products-filter {
  --border-radius: 25px;
  --inner-border-width: 0;
  --min-height: 32px;
  border-bottom: 0;
}

ion-select.filter {
  min-height: 32px;
}

ion-popover.popover-filter {
  margin-top: -6.5px;
}

ion-list.popover-filter__list {
  padding: 0;
}

ion-item.popover-filter__item {
  --min-height: 45px !important;
}

ion-input.popover-filter__input {
  min-height: 35px !important;
}

ion-card-header {
  color: black;
  gap: 10px;
  padding: 13px 20px 10px 20px !important;
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

.product-card__description,
ion-card-content {
  height: 70px;
  padding: 0 20px 20px 20px;
  font-size: 16px;
  line-height: 1.4;
  
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  white-space: pre-wrap;
}

ion-row.products-empty,
ion-row.products-layout {
  display: flex;
  flex-wrap: wrap;
  column-gap: 2%;
  row-gap: 1rem;
}

ion-row.products-empty {
  padding-top: 100px;
  justify-content: center;
}

ion-buttons.product-buttons {
  margin: 5px 0 20px 12px;
}

ion-row.product-filters {
  padding: 5px 0 10px 0;
  column-gap: 10px;
  row-gap: 5px;
}

ion-row.paginatiom {
  margin: 15px 0 15px 0;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 5px;
  width: 100%;
}

ion-button.pagination__button {
  width: 30px;
  height: 30px;
  padding: 0;
  margin: 0;
}

ion-button.pagination__button::part(native) {
  border-radius: 10%;
  width: 30px;
  height: 30px;
  padding: 0;
  color: black;
}

.pagination__dots {
  padding: 5px;
}

ion-button.color-white::part(native) {
 color: white;
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
