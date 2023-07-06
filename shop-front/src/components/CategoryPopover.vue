<template>
  <ion-button class="button-category" :id="clickTrigger">
    <!-- <ion-icon slot="start" :icon="listOutline" size="middle"></ion-icon> -->
    Category
    <ion-icon slot="end" :icon="icon['chevronDown']" size="small"></ion-icon>
  </ion-button>
  <ion-popover
    class="popover-categories"
    :trigger="clickTrigger"
    trigger-action="click"
  >
    <ion-list class="categories-list" lines="full">
      <ion-item
        @click="() => router.push('/categories/' + category.id)"
        v-for="category in props.categoriesList"
        button
        :detail="false"
      >
        <ion-label> {{ category.name }} </ion-label>
        <ion-icon :icon="icons[category.icon_name]" slot="start"></ion-icon>
      </ion-item>
    </ion-list>
  </ion-popover>
</template>

<script setup lang="ts">
import {
  IonButton,
  IonIcon,
  IonItem,
  IonLabel,
  IonPopover,
  IonList,
  useIonRouter,
} from "@ionic/vue";
import * as icon from "ionicons/icons";

// type assertion to explicitly specify the type of the icon object
// we create an IconObject interface that specifies an index signature for the icon object
// we then assert the type of the icon object as IconObject using icon as IconObject
interface IconObject {
  [key: string]: string;
}
const icons: IconObject = icon as IconObject;

const router = useIonRouter();

// need clickTrigger because the trigger must have different name for each component instance
const props = defineProps<{
  clickTrigger: string;
  categoriesList: {
    id: number;
    url: string;
    name: string;
    icon_name: string;
    sort_index: number;
    description: string;
  }[];
}>();
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
