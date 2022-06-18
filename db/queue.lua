queue = {}

function queue:new()
  local object = {}

  object.list = {}
  object.offset = 1

  self.__index = self
  return setmetatable(object, self)
end

function queue:length()
  return #self.list - self.offset
end

function queue:isEmpty()
  return #self.list == 0
end

function queue:enqueue(item)
  table.insert(self.list, item)

  return self
end

function queue:peek()
  if not self:isEmpty() then
    return self.list[self.offset]
  end

  return nil
end

function queue:dequeue()
  if self:isEmpty() then return nil end

  local item = self.list[self.offset]
  self.offset = self.offset + 1

  if (self.offset * 2) >= #self.list then
    self:optimize()
  end

  return item
end

function queue:optimize()
  local pos, new = 1, {}

  for i = self.offset, #self.list do
    new[pos] = self.list[i]
    pos = pos + 1
  end

  self.offset = 1
  self.list = new
end