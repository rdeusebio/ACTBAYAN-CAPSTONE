# Implementation Plan: Public Key Click-to-View-Details on Duplicate Modal

## Steps:

- [x] 1. Create TODO.md
- [x] 2. **app.py** - Add `public_key` to the duplicate API response in `api_check_duplicate()`
- [x] 3. **file_concern.html** - Update duplicate list item template to use `public_key` for click handler
- [x] 4. **file_concern.html** - Create `openPostModalByPublicKey()` function that fetches report details via API and populates the details modal
- [x] 5. Verify changes
