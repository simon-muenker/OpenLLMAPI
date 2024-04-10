# --- --- ---

install:
	@python3 -m pip install -r requirements.txt

# --- --- ---

dev:
	@python3 -m uvicorn api:app --reload

serve:
	@python3 -m uvicorn api:app
