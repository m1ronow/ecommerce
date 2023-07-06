<template>
  <!-- <ion-menu mode="ios" type="reveal" content-id="main-content" class="ion-hide-sm-up">
    <ion-content class="ion-padding">
      <ion-grid>
        <ion-row>
          <ion-accordion-group>
            <ion-accordion value="first">
              <ion-button class="menu-button" fill="clear" slot="header">
                <ion-label>Categories</ion-label>
                <ion-icon :icon="chevronDown" slot="end" class="ion-accordion-toggle-icon md" aria-hidden="true" role="img"></ion-icon>
              </ion-button>
              <div style="padding-left: 20px" slot="content">
                <ion-list lines="full">
                  <ion-item button :detail="false">
                    <ion-label>
                      Default Icon
                    </ion-label>
                    <ion-icon :icon="desktopOutline" slot="start"></ion-icon>
                  </ion-item>
                  <ion-item button :detail="false">
                    <ion-label>
                      Default Icon
                    </ion-label>
                    <ion-icon :icon="homeOutline" slot="start"></ion-icon>
                  </ion-item>
                  <ion-item button :detail="false">
                    <ion-label>
                      Default Icon
                    </ion-label>
                    <ion-icon :icon="shirtOutline" slot="start"></ion-icon>
                  </ion-item>
                  <ion-item button :detail="false">
                    <ion-label>
                      Default Icon
                    </ion-label>
                    <ion-icon :icon="heartOutline" slot="start"></ion-icon>
                  </ion-item>
                </ion-list>
              </div>
            </ion-accordion>
          </ion-accordion-group>
        </ion-row>
        <ion-row>
          <ion-button class="menu-button" fill="clear">
            Button 1
          </ion-button>
        </ion-row>
        <ion-row>
          <ion-button class="menu-button" fill="clear">
            Button 2
          </ion-button>
        </ion-row>
        <ion-row>
          <ion-button class="menu-button" fill="clear">
            Button 3
          </ion-button>
        </ion-row>
        <ion-row>
          <ion-button class="menu-button" fill="clear">
            Button 4
          </ion-button>
        </ion-row>
      </ion-grid>
    </ion-content>
  </ion-menu> -->
</template>

<script setup lang="ts">
import {
  IonPage,
  IonHeader,
  IonContent,
  IonSearchbar,
  IonCol,
  IonGrid,
  IonRow,
  IonCard,
  IonCardContent,
  IonCardHeader,
  IonCardSubtitle,
  IonCardTitle,
} from "@ionic/vue";
import {
  IonButton,
  IonButtons,
  IonToolbar,
  IonIcon,
  IonInput,
  IonMenuToggle,
} from "@ionic/vue";
import {
  personCircle,
  bagCheckOutline,
  cartOutline,
  bagAddOutline,
  heartOutline,
  desktopOutline,
  chevronExpand,
  listOutline,
  receiptOutline,
} from "ionicons/icons";

import {
  IonFab,
  IonFabButton,
  IonItem,
  IonLabel,
  IonMenu,
  IonRadio,
  IonRadioGroup,
  IonTitle,
  IonAccordion,
  IonAccordionGroup,
  IonTabs,
  IonRouterOutlet,
  IonTabBar,
  IonTabButton,
} from "@ionic/vue";
import {
  add,
  shirtOutline,
  chevronDown,
  homeOutline,
  chevronUp,
  playCircle,
  radio,
  library,
  search,
} from "ionicons/icons";
import Header from "../components/Header.vue";
</script>
