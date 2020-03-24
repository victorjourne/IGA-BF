ifndef $(base_url)
	base_url="https://www.interieur.gouv.fr/Publications/Rapports-de-l-IGA/Bonnes-Feuilles"
endif

venv:
	python3 -m venv venv
	venv/bin/pip3 install -r requirements.txt

crawl:
	rm -f  iga.json
	venv/bin/scrapy runspider iga.py  -o iga.json -s FEED_EXPORT_ENCODING='utf-8'

json2df:
	venv/bin/python3 json2df.py iga.json

shell:
	venv/bin/scrapy shell $(base_url)

run:venv crawl json2df
