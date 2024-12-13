usage="Usage: $0 [fr24_data|fr24_live_data] [enable|disable]"

if [ "$1" = fr24_data ]
then
    local="/dev/shm/fr24_data"
    path="/fr24_data"
elif [ "$1" = fr24_live_data ]
then
    local="/dev/shm/fr24_live_data"
    path="/fr24_live_data"
else
    echo "$usage"
    exit
fi

if [ "$2" = enable ]
then
    sudo tailscale funnel --set-path $path -bg "$local"
elif [ "$2" = disable ]
then
    sudo tailscale funnel --set-path $path -bg "$local" off
    tailscale serve status
else
    echo "$usage"
    exit
fi
