projects="/data/share/projects"

home="/home/pi/able-fr24"
project="$projects/able-fr24"

sudo rm -rf $project.old >/dev/null 2>/dev/null
sudo mv $project $project.old
sudo cp -rp $home $project
