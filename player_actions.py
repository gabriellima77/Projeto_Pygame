def get_collision(rect, tile):
    hit_rect_list = []
    for i in tile:
        if rect.colliderect(i.rect):
            hit_rect_list.append(i.rect)
    return hit_rect_list


def fall(player,tile_map):
    if player.rect.y > tile_map.height:
        for tile_object in tile_map.tmxdata.objects:
            if tile_object.name == "player":
                player.rect.x = int(tile_object.x)
                player.rect.y = int(tile_object.y)
                player.death += 1


def move(rect, movement, tiles, player, tile_map):
    collision_type = {'Top': False, 'Right': False, 'Bottom': False, 'Left': False}
    fall(player,tile_map)
    if tile_map.width > rect.x >= 0:
        rect.x += movement[0]
        if rect.x < 0:
            rect.x = 0
        if rect.x > tile_map.width - 32:
            rect.x = tile_map.width - 32
    hits = get_collision(rect, tiles)
    for tile in hits:
        if movement[0] > 0:
            collision_type['Right'] = True
            rect.right = tile.left
        if movement[0] < 0:
            collision_type['Left'] = True
            rect.left = tile.right
    rect.y += round(movement[1])
    hits = get_collision(rect, tiles)
    for tile in hits:
        if movement[1] > 0:
            collision_type['Bottom'] = True
            rect.bottom = tile.top
        if movement[1] < 0:
            collision_type['Top'] = True
            rect.top = tile.bottom
            player.momentum = 0.2
    return rect, collision_type

