box.cfg {
    log_level = 5,
    wal_mode = "write"
}

units = box.schema.create_space("units", {format = {
    {name = "id", type = "string"},
    {name = "name", type = "string"},
    {name = "date", type = "string"},
    {name = "parentId", type = "string", is_nullable = true},
    {name = "type", type = "string"},
    {name = "price", type = "number", is_nullable = true},
    {name = "children", type = "array"}
}, if_not_exists = true})


units:create_index('pk', {type = 'tree', parts = {'id'},  unique = true, if_not_exists=true})
units:create_index('dateTime', {type = 'tree', parts = {'date'}, unique = false, if_not_exists = true})


function get_mean_sum(id)
    local root = units:select(id)[1];
    local price = root[6];
    return price
end