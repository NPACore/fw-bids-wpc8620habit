LunaHabit/:
	./bundler.py --explode --jsondir LunaHabit/ --combined EH-202502.json --template LunaHabit/template.json

LunaHabit.json: $(wildcard LunaHabit/*)
	./bundler.py  --jsondir LunaHabit/ --combined LunaHabit.json --template LunaHabit/template.json
