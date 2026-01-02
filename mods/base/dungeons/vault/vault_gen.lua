local M = {}

-- REQUIRED ENTRY POINT
function M.generate(dungeon, ctx)

    -- Fill dungeon with walls
    -- ctx.fill("#", false)
    
    ctx.create_square_room(20, 20)

    -- Carve main room
    -- ctx.carve_room(2, 2, 16, 16)

    -- Place exit
    ctx.place_exit(10, 10)

    -- Spawn mobs
    -- ctx.spawn_mob("base:spirit", 5, 5)
    -- ctx.spawn_mob("base:spirit", 14, 14)

end

return M