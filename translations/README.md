# translations/

Babel message catalogs live here. English is the source locale (no catalog
needed). When Arabic launches:

    pybabel extract -F babel.cfg -k _l -o translations/messages.pot .
    pybabel init  -i translations/messages.pot -d translations -l ar
    # translate translations/ar/LC_MESSAGES/messages.po
    pybabel compile -d translations

Then add `ar` to SUPPORTED_LOCALES. RTL and the Arabic font hook are already
implemented in the CSS — no template or route changes required.
