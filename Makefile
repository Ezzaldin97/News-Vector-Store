# run Qdrant DB docker image..
qdrant:
	@echo "Running Qdrant DB Locally"
	docker pull qdrant/qdrant && \
	docker run -p 6333:6333 \
	    -v D:/llm_data_generator/data/db:/qdrant/storage:z \
        qdrant/qdrant

# run the pipeline pass date as parameter to get news of (date-1)
run:
	poetry run python main.py --date $(date)