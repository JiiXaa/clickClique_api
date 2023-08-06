# clickClique_api

## Common usage patterns using Django's generic views to avoid repetition for the views.

## dj-rest-auth API endpoints:

| url                        | http | data sent                    | data received                     |
| -------------------------- | ---- | ---------------------------- | --------------------------------- |
| dj-rest-auth/registration  | POST | username password1 password2 | -                                 |
| dj-rest-auth/login         | POST | username password            | access token refresh token        |
| dj-rest-auth/logout        | POST | -                            | -                                 |
| dj-rest-auth/user/         | GET  | access token refresh token   | username profile_id profile_image |
| dj-rest-auth/token/refresh | POST | access token refresh token   | (new) access token                |
