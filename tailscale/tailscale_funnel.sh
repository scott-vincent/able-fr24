usage="Usage: $0 [fr24_data|fr24_live_data] [enable|disable]"

if [ "$1" = fr24_data ]
then
    local="/mem/fr24_data"
    path="/fr24_data"
elif [ "$1" = fr24_live_data ]
then
    local="/mem/fr24_live_data"
    path="/fr24_live_data"
else
    echo "$usage"
    exit
fi

# Create RAM drive
if [ ! -d /mem ]
then
  sudo mkdir /mem
  echo tmpfs /mem tmpfs nodev,nosuid,size=32K 0 0 | sudo tee -a /etc/fstab >/dev/null
  sudo mount -a
fi

if [ "$2" = enable ]
then
    if [ ! -f $local ]
    then
        >$local
    fi
    sudo tailscale funnel --set-path $path -bg "$local"
elif [ "$2" = disable ]
then
    sudo tailscale funnel --set-path $path -bg "$local" off
    tailscale serve status
else
    echo "$usage"
    exit
fi
