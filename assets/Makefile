JS_SOURCES=js/jquery.min.js js/bootstrap.min.js js/pdp.min.js
JS_OUTPUT=js/all.min.js

CSS_SOURCES=css/bootstrap.min.css css/bootstrap-responsive.min.css \
			css/bootstrap-pygments.min.css css/pygments.min.css    \
			css/progdupeupl.min.css
CSS_OUTPUT=css/all.min.css

# Javascript variables

JS_FILES=$(filter-out %.min.js,$(wildcard \
	js/*.js \
))
JS_MINIFIED=$(JS_FILES:.js=.min.js)

# CSS variables

CSS_FILES=$(filter-out %.min.css,$(wildcard \
	css/*.css \
))
CSS_MINIFIED=$(CSS_FILES:.css=.min.css)

# Common rules

.PHONY: clean

all: minify-js minify-css

clean: 
	rm $(CSS_OUTPUT)
	rm $(JS_OUTPUT)

# Javascript rules

minify-js: $(JS_MINIFIED)
	cat $(JS_SOURCES) > $(JS_OUTPUT)

%.min.js: %.js
	yuicompressor -o $@ $<

# CSS rules

minify-css: $(CSS_MINIFIED)
	cat $(CSS_SOURCES) > $(CSS_OUTPUT)

%.min.css: %.css
	yuicompressor -o $@ $<
