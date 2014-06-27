all: addons

design/etl.xmi: design/etl.zargo
	-echo "REBUILD etl.xmi from etl.zargo. I cant do it"

addons: etl

etl: design/etl.uml
	xmi2oerp -r -i $< -t addons -v 2

clean:
	rm -rf addons/etl/*
	sleep 1
	touch design/etl.uml
