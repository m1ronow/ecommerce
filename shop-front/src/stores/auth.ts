import { defineStore } from "pinia";
import { ref, onMounted } from "vue";
import { authVerify } from "@/api/api";

export const useAuthStore = defineStore("auth", () => {
  const isLoggedIn = ref<boolean>(false);

  const getLoginStatus = () => {
    authVerify()
      .then((response: any) => {
        isLoggedIn.value = response.data.isAuthenticated;
        return response.data.isAuthenticated;
      })
      .catch((error: any) => {
        console.log(error);
        return error;
      });
  };

  onMounted(() => {
    getLoginStatus();
  });

  return { isLoggedIn, getLoginStatus };
});
