import { createClient } from "https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm";

export const db = createClient(
  "https://mzmkdexhkbkpgdvfzazs.supabase.co",
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im16bWtkZXhoa2JrcGdkdmZ6YXpzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI0Njg4MTgsImV4cCI6MjA5ODA0NDgxOH0.eKznfYuZy5h-5NXma6CAYRdZJucPrf-dlYolByH-Lfs"
);