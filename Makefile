LunaHabit/:
	fw download fw://mrrc/playground/files/test-5.json
	mv test-5.json EH-202502.json
	./bundler.py --explode --jsondir LunaHabit/ --combined EH-202502.json --template LunaHabit/template.json
	# for f in LunaHabit/*json; do jq 'del(.custom_name)' $f | sponge $f; done

LunaHabit_curate.json: $(wildcard LunaHabit/*)
	./bundler.py  --jsondir LunaHabit/ --combined LunaHabit_curate.json --template LunaHabit/template.jsonc
