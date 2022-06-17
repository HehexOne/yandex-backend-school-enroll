docker stop mytarantool
docker container rm mytarantool
docker run --name mytarantool -p 3301:3301 -d tarantool/tarantool tarantool box_init.lua
docker cp box_init.lua mytarantool:/opt/tarantool/box_init.lua
docker start mytarantool