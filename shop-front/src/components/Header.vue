<template>
  <ion-header>
    <ion-toolbar class="main-toolbar">
      <ion-grid :fixed="true" style="padding: 0 5px 0 5px">
        <ion-row class="ion-justify-content-between">
          <ion-col class="ion-align-self-center">
            <ion-buttons class="ion-hide-sm-up">
              <category-popover
                click-trigger="header-trigger"
                :categories-list="categories"
              />
            </ion-buttons>

            <div class="logo-col ion-hide-sm-down">
              <div class="logo" @click="() => router.push('/')">
                <ion-icon
                  :icon="bagCheckOutline"
                  size="large"
                  aria-hidden="true"
                ></ion-icon>
                <ion-text>
                  <h2>E-Commerce</h2>
                </ion-text>
              </div>
            </div>
          </ion-col>

          <ion-col class="ion-align-self-center">
            <ion-searchbar
              class="custom"
              animated
              placeholder="Search"
            ></ion-searchbar>
          </ion-col>

          <ion-col class="ion-align-self-center header-nav-buttons">
            <ion-button
              @click="() => router.push('/cart')"
              class="header-button ion-hide-sm-down"
              fill="clear"
              color="medium"
            >
              <ion-icon slot="icon-only" :icon="cartOutline"></ion-icon>
            </ion-button>

            <ion-button
              @click="() => router.push('/favorites')"
              router-link="/favorites"
              class="header-button ion-hide-sm-down"
              fill="clear"
              color="medium"
            >
              <ion-icon slot="icon-only" :icon="heartOutline"></ion-icon>
            </ion-button>

            <user-profile click-trigger="user-profile" />
          </ion-col>
        </ion-row>
      </ion-grid>
    </ion-toolbar>

    <!-- the div below fixes visibility issue:
        when sliding menu, header's bottom border is invisible and we can see menu elements through that line -->
    <div class="toolbar-divider"></div>

    <ion-toolbar class="ion-hide-sm-down">
      <ion-grid :fixed="true">
        <ion-row class="ion-justify-content-between">
          <ion-buttons>
            <category-popover
              click-trigger="navbar-trigger"
              :categories-list="categories"
            />
            <ion-button @click="() => console.log(route.query)"> Button 1 </ion-button>
            <ion-button> Button 2 </ion-button>
            <ion-button> Button 3 </ion-button>
            <ion-button> Button 4 </ion-button>
          </ion-buttons>
        </ion-row>
      </ion-grid>
    </ion-toolbar>
  </ion-header>
</template>

<script setup lang="ts">
import {
  IonButton,
  IonButtons,
  IonToolbar,
  IonIcon,
  IonHeader,
  IonSearchbar,
  IonCol,
  IonGrid,
  IonRow,
  IonText,
  useIonRouter,
} from "@ionic/vue";
import { bagCheckOutline, cartOutline, heartOutline } from "ionicons/icons";
import CategoryPopover from "./CategoryPopover.vue";
import UserProfile from "./UserProfile.vue";
import { ref } from "vue";
import { getCategories } from "../api/api";
import { useRoute } from "vue-router";

const route = useRoute();
const router = useIonRouter();
const categories = ref([]);

getCategories()
  .then((response: any) => {
    categories.value = response.data.results;
  })
  .catch((error: any) => {
    console.log(error);
  });
</script>

<style lang="scss">
ion-searchbar.custom {
  padding: 0;
}

ion-popover.popover-categories {
  margin-top: -6.5px;
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

ion-list.categories-list {
  padding: 0;
}

div.toolbar-divider {
  height: 0.55px;
  background-color: var(
    --ion-toolbar-border-color,
    var(--ion-border-color, var(--ion-color-step-150, rgba(0, 0, 0, 0.2)))
  );
}

div.logo-col {
  display: flex;
  justify-content: flex-start;
}

div.logo {
  align-items: center;
  gap: 0.4rem;
  cursor: pointer;
  padding-left: 4px;
}

ion-button.header-button {
  --padding-start: 4px;
  --padding-end: 4px;
  margin-top: 0;
  margin-bottom: 0;
}

@media (min-width: 1px) and (max-width: 576px) {
  ion-button.header-button {
    --padding-start: 3px;
    --padding-end: 3px;
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
