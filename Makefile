startup:
	# Take down services.
	docker-compose down
	
	# run database migrations and create the first user account
	# Before starting Airflow for the first time, You need to prepare your environment, 
	# i.e. create the necessary files, directories and initialize the database.
	docker-compose up airflow-init
	
	# start all service, after initialization is complete.
	docker-compose up



k8s_context:	
	# set k8s context as k8s
	kubectl config use-context docker-for-desktop


k8s_remove:
	# Remove all deployment, services, and pod
	kubectl delete --all svc --namespace=airflow
	kubectl delete --all deployments --namespace=airflow
	kubectl delete --all statefulsets --namespace=airflow
	kubectl delete --all pods --namespace=airflow