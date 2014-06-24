all: addons

design/elt.xmi: design/elt.zargo
	-echo "REBUILD elt.xmi from elt.zargo. I cant do it"

addons: elt

elt: design/elt.uml
	xmi2oerp -r -i $< -t addons -v 2

clean:
	rm -rf addons/elt/*
	sleep 1
	touch design/elt.uml
