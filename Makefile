
### Docker-Compose Deployment
start:
	# Take down services.
	docker-compose down
	
	# run database migrations and create the first user account
	# Before starting Airflow for the first time, You need to prepare your environment, 
	# i.e. create the necessary files, directories and initialize the database.
	docker-compose up airflow-init
	
	# start all service, after initialization is complete.
	docker-compose up -d

containers:
	watch -n 2 docker container ls -a

exec:
	docker exec -it airflow-dags-airflow-webserver-1 bash

### Helm Deployment 
k8s_context:	
	# set k8s context as k8s
	kubectl config use-context docker-desktop


k8s_remove: k8s_context
	# Remove all deployment, services, and pod
	kubectl delete --all svc --namespace=airflow
	kubectl delete --all deployments --namespace=airflow
	kubectl delete --all statefulsets --namespace=airflow
	kubectl delete --all pods --namespace=airflow
	kubectl delete namespace airflow


k8s_deploy_astro:
	# Testing the helm distributino from astro.
	kubectl create namespace airflow
	helm repo add astronomer https://helm.astronomer.io
	helm install airflow --namespace astro astronomer/airflow

k8s_remove_astro:
	helm delete airflow


k8_deploy_bairflow:
	# Testing the bitnami installation of airflow. The deployment should be accessible at http://127.0.0.1:8080
	# Username: User, Password: the output of "export AIRFLOW_PASSWORD"
	kubectl create namespace airflow
	helm repo add bitnami https://charts.bitnami.com/bitnami
	helm install my-release bitnami/airflow

	# You will need to port forward the to access the webserver without a load balancer
	kubectl port-forward --namespace airflow svc/my-release-airflow 8080:8080

	# View the password your should use to access the database.
	export AIRFLOW_PASSWORD=$(kubectl get secret --namespace "airflow" my-release-airflow -o jsonpath="{.data.airflow-password}" | base64 --decode)

k8s_remove_bairflow:
	helm delete airflow