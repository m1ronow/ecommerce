export interface Product {
  id: number;
  url: string;
  name: string;
  description: string;
  price: string;
  image: string;
  created_at: string;
  updated_at: string;
  category: string;
  in_cart: boolean;
  in_favorites: boolean;
}

export interface CartItems {
  url: string;
  quantity: number;
  cart: string;
  product: Product;
}

export interface RegUserData {
  email: string;
  name: string;
  password: string;
  captcha: string;
}

export interface LogUserData {
  email: string;
  password: string;
}
