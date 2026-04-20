export interface Comment {
  id: number;
  author_name: string;
  text: string;
  created_at: string;
}

export interface Product {
  id: number;
  name: string;
  brand: string;
  is_authentic: boolean;
  serial_number: string;
  manufacture_location: string;
  history: string;
  image_url?: string;
  comments?: Comment[];
}