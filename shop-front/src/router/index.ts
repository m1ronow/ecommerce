import { createRouter, createWebHistory } from "@ionic/vue-router";
import { RouteRecordRaw } from "vue-router";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    component: () => import("@/views/MainPage.vue"),
  },
  {
    path: "/home",
    component: () => import("@/views/MainPage.vue"),
  },
  {
    path: "/favorites",
    component: () => import("@/views/FavoritesPage.vue"),
  },
  {
    path: "/cart",
    component: () => import("@/views/CartPage.vue"),
  },
  {
    path: "/checkout",
    component: () => import("@/views/CheckoutPage.vue"),
  },
  {
    path: "/orders",
    component: () => import("@/views/OrdersPage.vue"),
  },
  {
    path: "/categories/:id",
    component: () => import("@/views/CategoryPage.vue"),
  },
  {
    path: "/registration",
    component: () => import("@/views/RegistrationPage.vue"),
  },
  {
    path: "/login",
    component: () => import("@/views/LoginPage.vue"),
  },
  {
    path: "/profile",
    component: () => import("@/views/ProfilePage.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
