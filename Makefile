.PHONY: check
JSONC=$(wildcard *jsonc) # json with comments
ALLDERIV=$(patsubst %.json,out/%.deriv.json,$(wildcard *json)) $(patsubst %.jsonc,out/%.deriv.json,$(JSONC))

.INTERMEDIATE: $(ALLDERIV) # remove .deriv.json when done
out/combined_template.json: $(ALLDERIV) | out/
	jq -s '.[0] + {rules: .[1:]}' $(sort $(ALLDERIV)) > $@

out/%.deriv.json: %.json | out/
	cp $^ $@
	jq < $@ > /dev/null # confirm valid json

out/%.deriv.json: %.jsonc | out/
	cpp -P -E $^ -o $@
	jq < $@ > /dev/null # confirm valid json

out/:
	mkdir -p out

check: out/combined_template.json
	 fw-template-check -t out/combined_template.json -r AntiSaccade "AntiSaccade" "AntiSaccade_repeat" "Habit" "Habit_SBRef" "ABCD_T1w_vNav xyx"
