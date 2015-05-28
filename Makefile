
depends:
	@scripts/install_spotify_depends.sh

clean:
	@find . -name \*.pyc -delete

clean_all: clean
	@rm -rf .venv
