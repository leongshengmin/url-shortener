# URL Shortener

### Description
1. Given a URL, returns a shortened URL.

E.g.
- Input: https://shopee.sg/m/99-super-shopping-day-825-sneak-peek?smtt=204.35043
- Output: https://sho.rt/92jdZaQ1

2. Given a shortened URL, return the original URL.
E.g. 
- Input: https://sho.rt/92jdZaQ1
- Output: https://shopee.sg/m/99-super-shopping-day-825-sneak-peek?smtt=204.35043

### Changes:
- Add caching for retrieving urls in `src/managers/default.py`
- Vertically scale mysql instance (bumped CPU) in `docker-compose`
- Remove unnecessary `order_by` clause in `find_match_by_url` in `src/accessors/urls_tab.py`  