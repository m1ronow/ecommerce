import axios from "axios";
import Cookies from "js-cookie";

const apiHost: string = "http://localhost:8000";
const authHeaders = (data: object = {}) => {
  return {
    data,
    withCredentials: true,
    headers: {
      "X-CSRFToken": Cookies.get("csrftoken"),
    },
  };
};

export const getCategories = async () => {
  return await axios.get(`${apiHost}/categories/`);
};

export const getCategoryProducts = async (categoryId: string) => {
  return await axios.get(`${apiHost}/products/filtered_by_category/${categoryId}`, authHeaders());
};

export const getProducts = async () => {
  return await axios.get(`${apiHost}/products/`, authHeaders());
};

export const getCartItems = async () => {
  return await axios.get(`${apiHost}/cart_items/`, authHeaders());
};

export const addCartItem = async (cartItem: object) => {
  return await axios.post(`${apiHost}/cart_items/`, cartItem, authHeaders());
};

export const updateCartQuantity = async (cartData: Array<any>) => {
  return await axios.patch(`${apiHost}/cart_items/update_quantity/`, cartData, authHeaders());
};

export const deleteCartItems = async (itemIds: Array<number>) => {
  return await axios.delete(`${apiHost}/cart_items/delete/`, authHeaders({ product_ids: itemIds }));
};

export const getFavoriteItems = async () => {
  return await axios.get(`${apiHost}/favorites/`, authHeaders());
};

export const addFavoriteItem = async (fovoriteItem: object) => {
  return await axios.post(`${apiHost}/favorites/`, fovoriteItem, authHeaders());
};

export const deleteFavoriteItems = async (itemIds: Array<number>) => {
  return await axios.delete(`${apiHost}/favorites/delete/`, authHeaders({ product_ids: itemIds }));
};

export const regUser = async (userData: object) => {
  return await axios.post(`${apiHost}/users/`, userData, authHeaders());
};

export const getUserData = async () => {
  return await axios.get(`${apiHost}/users/me/`, authHeaders());
};

export const getUserProfile = async () => {
  return await axios.get(`${apiHost}/user_profile/me/`, authHeaders());
};

export const updateUserProfile = async (profileData: object) => {
  return await axios.patch(`${apiHost}/user_profile/update_me/`, profileData, authHeaders());
};

export const updateUserAddress = async (data: object) => {
  return await axios.patch(`${apiHost}/user_address/update_me/`, data, authHeaders());
};

export const getShippingMethods = async () => {
  return await axios.get(`${apiHost}/shipping_methods/`);
};

export const getPaymentMethods = async () => {
  return await axios.get(`${apiHost}/payment_methods/`);
};

export const createOrder = async (orderData: object) => {
  return await axios.post(`${apiHost}/orders/`, orderData, authHeaders());
};

export const login = async (userData: object) => {
  return await axios.post(`${apiHost}/login/`, userData, authHeaders());
};

export const logout = async () => {
  return await axios.post(`${apiHost}/logout/`, {}, authHeaders());
};

export const authVerify = async () => {
  return await axios.post(`${apiHost}/auth_verify/`, {}, authHeaders());
};

export const createPaymentInvoice = async (data: object) => {
  return await axios.post(`${apiHost}/payments/new/`, data);
};

export const createDonateInvoice = async () => {
  return await axios.post(`${apiHost}/payments/donate/`);
};
