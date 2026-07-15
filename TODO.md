# TODO - Refactor Flask user management

- [x] Update `/users` SELECT query in `app.py` to return **one row per account/person**.
- [x] Update `/users` POST actions to use `account_id` and affect **all credentials** belonging to that account/contact.
- [x] Implement single JOIN UPDATE for Ban/Unban/Restrict.
- [x] Update Remove behavior (safe approach): lock all credentials for that account.
- [x] Update `templates/users.html` to submit `account_id` (hide `user_id`) and display `#account_id` instead of `#user_id`.
- [ ] Quick manual test: ensure no duplicate rows and actions affect all credentials (left for you).

 