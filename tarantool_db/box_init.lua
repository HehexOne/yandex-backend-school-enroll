local uuid = require("uuid")
local json = require("json")
local queue = require("queue")
local os = require("os")
local math = require("math")

box.cfg { listen = 3301,
          memtx_memory = 1024 * (1024 * 1024), -- 1 Gb memory
          memtx_max_tuple_size = 2 * (1024 * 1024),
          slab_alloc_factor = 2
}

box.schema.user.grant('guest', 'read,write,execute,create,drop', 'universe')

local units = box.schema.create_space('units', {
    format = {
        { name = 'id', type = 'uuid', is_nullable = false },
        { name = 'name', type = 'string', is_nullable = false },
        { name = 'date', type = 'unsigned', is_nullable = false },
        { name = 'parentId', type = 'uuid', is_nullable = true },
        { name = 'type', type = 'string', is_nullable = false },
        { name = 'price', type = 'number', is_nullable = true }
    },
    if_not_exists = true
})

units:create_index('i_index', { parts = { 'id' }, if_not_exists = true, unique = true, type = 'TREE' })
units:create_index('d_index', { parts = { 'date' }, if_not_exists = true, type = 'TREE', unique = false })
units:create_index('p_index', { parts = { 'parentId' }, if_not_exists = true, type = 'TREE', unique = false })

-- Тернарный оператор
function _if(bool, v1, v2)
    if bool then
        return v1
    else
        return v2
    end
end

responses = {
    ok = '{"code": 200, "message": "OK!"}',
    not_found = '{"code": 404, "message": "Item not found"}',
    validation_error = '{"code": 400, "message": "Validation Failed"}'
}

-- insets
function insert_units(payload)
    payload = json.decode(payload)
    box.begin()

    local items = payload.items
    local update_date = payload.updateDate

    for k, item in pairs(items) do

        item.id = uuid.fromstr(item.id)
        if item.parentId ~= nil then
            item.parentId = uuid.fromstr(item.parentId)
        else
            item.parentId = box.NULL
        end

        if item.price == nil then
            item.price = box.NULL
        end

        local unit = units.index.i_index:get(item.id, { iterator = "EQ" })

        local parent = box.NULL
        if item.parentId ~= box.NULL then
            parent = units.index.i_index:get(item.parentId, { iterator = "EQ" })
        end

        local children = units.index.p_index:count(item.id, { iterator = "EQ" })

        if children ~= 0 and item.type ~= ("CATEGORY") then
            error(responses.validation_error)
        end

        if parent ~= box.NULL and parent.type == "OFFER" then
            error(responses.validation_error)
        end

        if unit and unit.type ~= item.type then
            error(responses.validation_error)
        end

        if item.type == "OFFER" and item.price < 0 then
            error(responses.validation_error)
        end

        if item.type == "CATEGORY" and item.price ~= box.NULL then
            error(responses.validation_error)
        end

        if unit then
            units.index.i_index:update(unit.id, {
                { '=', 'name', item.name },
                { '=', 'date', update_date },
                { '=', 'parentId', item.parentId },
                { '=', 'price', item.price }
            })
        else
            units:insert({ item.id, item.name, update_date, item.parentId, item.type, item.price })
        end

        if parent ~= box.NULL then
            local p_unit = parent
            while p_unit ~= box.NULL do
                units.index.i_index:update(p_unit.id, { { '=', 'date', update_date } })
                if p_unit.parentId ~= box.NULL then
                    p_unit = units.index.i_index:get(p_unit.parentId)
                else
                    break
                end
            end
        end
    end

    box.commit()
    return responses.ok
end

-- delete
function delete_unit(id)
    box.begin()
    id = uuid.fromstr(id)

    local unit = units.index.i_index:get(id, { iterator = "EQ" })

    if not unit then
        error(responses.not_found)
    end

    local q = queue:new()
    q:enqueue(unit.id)

    while not q:isEmpty() do
        local q_unit = q:dequeue()
        for k, v in units.index.p_index:pairs(q_unit, { iterator = "EQ" }) do
            q:enqueue(v.id)
        end
        units.index.i_index:delete(q_unit)
    end

    box.commit()
    return responses.ok
end

-- nodes
function get_nodes(id)
    box.begin()
    id = uuid.fromstr(id)

    local unit = units.index.i_index:get(id, { iterator = "EQ" })

    if unit == box.NULL then
        error(responses.not_found)
    end

    local res = {
        id = unit.id,
        name = unit.name,
        date = os.date("!%Y-%m-%dT%H:%M:%S.000Z", unit.date),
        parentId = _if(unit.parentId == nil, json.NULL, unit.parentId),
        type = unit.type,
        price = _if(unit.price == nil, json.NULL, unit.price),
        children = _if(unit.type == "CATEGORY", {}, json.NULL)
    }

    if res.children ~= json.NULL then
        local children_obj = get_children(res.id)
        res.children = children_obj.children
        if children_obj.children ~= json.NULL and #children_obj.children > 0 then
            res.price = math.floor(children_obj.offer_price_sum / children_obj.offer_count)
        end
    end

    box.commit()
    return json.encode(res)
end

function get_children(id)
    local unit = units.index.i_index:get(id, { iterator = "EQ" })
    if unit.type == "OFFER" then
        return { children = json.NULL, offer_price_sum = unit.price, offer_count = 1 }
    end
    local res = {}
    local offer_price_sum = 0
    local offer_count = 0
    for k, v in units.index.p_index:pairs(unit.id, { iterator = "EQ" }) do
        local child = {
            id = v.id,
            name = v.name,
            date = os.date("!%Y-%m-%dT%H:%M:%S.000Z", v.date),
            parentId = _if(v.parentId == nil, json.NULL, v.parentId),
            type = v.type,
            price = _if(v.price == nil, json.NULL, v.price),
            children = _if(v.type == "CATEGORY", {}, json.NULL)
        }
        local children_obj = get_children(child.id)
        child.children = children_obj.children
        offer_price_sum = offer_price_sum + children_obj.offer_price_sum
        offer_count = offer_count + children_obj.offer_count
        if child.children ~= json.NULL and #child.children > 0 then
            child.price = math.floor(children_obj.offer_price_sum / children_obj.offer_count)
        end
        table.insert(res, child)
    end
    return { children = res, offer_price_sum = offer_price_sum, offer_count = offer_count }
end

function get_sales(timestamp, before_timestamp)
    box.begin()

    local items = {}
    for k, v in units.index.d_index:pairs({ before_timestamp }, { iterator = "GE" }) do
        if v.type == "OFFER" and v.date <= timestamp then
            local res_val = {
                id = v.id,
                name = v.name,
                date = os.date("!%Y-%m-%dT%H:%M:%S.000Z", v.date),
                parentId = _if(v.parentId == nil, json.NULL, v.parentId),
                price = _if(v.price == nil, json.NULL, v.price),
                type = v.type,
            }
            table.insert(items, res_val)
        end
    end

    local res = { items = items }

    box.commit()
    return json.encode(res)
end