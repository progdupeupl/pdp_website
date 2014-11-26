# Progdupeupl's Makefile
#
# May provides useful targets in order to avoid a lot of typing when we want to
# run all the tests and other commands that require specific options.

MANAGE = manage.py
PMANAGE = python $(MANAGE)

TEST_APPS = pdp.article \
	pdp.tutorial \
	pdp.forum \
	pdp.member \
	pdp.utils \
	pdp.pages \
	pdp.messages \
	pdp.gallery

FIXTURES = fixtures/auth.yaml \
	fixtures/forum.yaml \
	fixtures/member.yaml \
	fixtures/messages.yaml \
	fixtures/tutorial.yaml

ASSETS_DIR = ./assets/

# If you add a new target, do not forget to put it here so that make will not
# think your target is a real file.
.PHONY: tests \
	test \
	syncdb \
	migrate \
	initsearch \
	updatesearch \
	assets \
	collectstatic \
	loadfixtures \
	coverage \
	celery \
	bootstrap \
	checkdeps

# Test all the project's own applications.
tests:
	$(PMANAGE) test $(TEST_APPS)

test: tests

# Synchronize the Django database with the models.
syncdb:
	$(PMANAGE) syncdb

# Run the South database migrations.
migrate:
	$(PMANAGE) migrate

# Initialize the search engine and its cache.
initsearch:
	$(PMANAGE) rebuild_index --noinput

# Update the search engine cache.
updatesearch:
	$(PMANAGE) update_index

# Execute the Makefile in the assets directory.
assets:
	cd $(ASSETS_DIR) && $(MAKE)

# Collect and process all the static content.
collectstatic:
	$(PMANAGE) collectstatic --noinput

# Load fake data and put them in the database.
loadfixtures:
	$(PMANAGE) loaddata $(FIXTURES)

# Launch coverage report.
coverage:
	coverage run --source="." $(MANAGE) test $(TEST_APPS)
	coverage html

# Start the celery tasks server
celery:
	celery worker --app=pdp.celeryapp:app

# Initialize the whole project for the first time
bootstrap: checkdeps syncdb migrate initsearch assets collectstatic
	mkdir -p media/tutorials

# Count lines of code, avoiding irrelevant files
cloc:
	cloc . --exclude-dir='assets,__pycache__,venv,media,static,migrations,fixtures'

# Check dependencies
checkdeps:
	./check_dependencies.sh
