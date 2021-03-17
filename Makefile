startup:
	# Take down services.
	docker-compose down
	
	# run database migrations and create the first user account
	docker-compose up airflow-init
	
	# start all service
	docker-compose up