.PHONY: filter test clean render all

all: filter render

filter:
	python filter.py --src timetable0.csv --out timetable.csv

test:
	python render.py --src timetable.csv --template template_jp.md --lang jp --out output_jp.md
	python render.py --src timetable.csv --template template_en.md --lang en --out output_en.md

clean:
	rm -rf output_jp.md
	rm -rf output_en.md
	
render:
	python render.py --src timetable.csv --template template_jp.md --lang jp --out ../content/program/timetable.md
	python render.py --src timetable.csv --template template_en.md --lang en --out ../content/program/timetable.en.md