ifndef $(base_url)
	base_url="https://www.interieur.gouv.fr/Publications/Rapports-de-l-IGA/Bonnes-Feuilles"
endif
ifndef $(base_path)
	base_path=data
endif

venv:
	python3 -m venv venv
	venv/bin/pip3 install -r requirements.txt

crawl:
	rm -f  iga.json
	rm -f $(base_path)/pdf -r
	mkdir -p $(base_path)/pdf
	venv/bin/scrapy runspider iga.py -o iga.json -s FEED_EXPORT_ENCODING='utf-8'
	cp -r tmp/* $(base_path)/pdf/

json2df:
	venv/bin/python3 json2df.py iga.json $(base_path)

json2meta:
		rm -f $(base_path)/meta -r
		mkdir -p $(base_path)/meta
		venv/bin/python3 json2meta.py iga.json $(base_path)

shell:
	venv/bin/scrapy shell $(base_url)

run:venv crawl json2df json2meta
