create table products (
  id uuid primary key default gen_random_uuid(),
  url text unique,
  name text,
  product_id text,
  price int,
  last_price int,
  stock boolean default false,
  enabled boolean default true,
  created_at timestamp default now(),
  updated_at timestamp default now()
);