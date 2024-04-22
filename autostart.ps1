#Run in Linux: 0 3 * * * path/autostart.sh

$STATUS = docker inspect --format="{{.State.Status}}" $CONTAINERNAME

if ($STATUS -ne "running") {
	docker starёt $CONTAINERNAME
}

