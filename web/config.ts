export default {
  api_host: "http://localhost:8000",
  logout_url:
    "http://localhost:8000/auth/logout/?next=http://localhost:3000/home",
  oauth: {
    client_id: "Rgkqb0nHHdZkE5LdiIGWspJaZ1OBurcudFISCpUO",
    client_secret:
      "A6x43GBwX1JWdQoKrkYX9SKoPX2Ws601WvFlf6hmnhslc3uZZMBEsK2wxR8I1eF6qQI6lsaGN8WztV0nPbFf28oZAkkPXebTvxQYCKP8AcvEVPOTb5a1ZirKGy5ryD9y",
  },
  session_cookie: {
    password: "complex_password_at_least_32_characters_long",
    cookieName: "myapp_cookiename",
    // if your localhost is served on http:// then disable the secure flag
    cookieOptions: {
      secure: process.env.NODE_ENV === "production",
    },
  },
};
