all: addons

design/oerp_migrator.xmi: design/oerp_migrator.zargo
	-echo "REBUILD oerp_migrator.xmi from oerp_migrator.zargo. I cant do it"

addons: oerp_migrator

oerp_migrator: design/oerp_migrator.uml
	xmi2oerp -r -i $< -t addons -v 2

clean:
	rm -rf addons/oerp_migrator/*
	sleep 1
	touch design/oerp_migrator.uml
