projects="/data/share/projects"

home="/home/pi/able_fr24"
project="$projects/able_fr24"

sudo rm -rf $project.old >/dev/null 2>/dev/null
sudo mv $project $project.old
sudo cp -rp $home $project
