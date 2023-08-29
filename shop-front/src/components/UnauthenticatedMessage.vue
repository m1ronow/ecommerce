<template>
    <div class="unauthenticated-content">
        Please,
        <a @click="() => router.push('/login')" class="router-link">log in</a>
        or
        <a @click="() => router.push('/registration')" class="router-link"
          >register</a
        >
    </div>
</template>

<script setup lang="ts">
import { useIonRouter } from "@ionic/vue";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const router = useIonRouter();
</script>

<style>
.unauthenticated-content {
    width: 100%;
    text-align: center;
    padding: 35px;
}

.router-link {
    cursor: pointer;
}
</style>