def get_collision(rect, tile):
    hit_rect_list = []
    for i in tile:
        if rect.colliderect(i.rect):
            hit_rect_list.append(i.rect)
    return hit_rect_list


def fall(player, tile_map):
    if player.rect.y > tile_map.height:
        for tile_object in tile_map.tmxdata.objects:
            if tile_object.name == "player":
                player.rect.x = int(tile_object.x)
                player.rect.y = int(tile_object.y)
                player.death += 1


def move(player, tiles, tile_map):
    collision_type = {'Top': False, 'Right': False, 'Bottom': False, 'Left': False}
    fall(player, tile_map)
    if tile_map.width > player.rect.x >= 0:
        player.rect.x += player.movement[0]
        if player.rect.x < 0:
            player.rect.x = 0
        if player.rect.x > tile_map.width - 32:
            player.rect.x = tile_map.width - 32
    hits = get_collision(player.rect, tiles)
    for tile in hits:
        if player.movement[0] > 0:
            collision_type['Right'] = True
            player.rect.right = tile.left
        if player.movement[0] < 0:
            collision_type['Left'] = True
            player.rect.left = tile.right
    player.rect.y += round(player.movement[1])
    hits = get_collision(player.rect, tiles)
    for tile in hits:
        if player.movement[1] > 0:
            collision_type['Bottom'] = True
            player.rect.bottom = tile.top
        if player.movement[1] < 0:
            collision_type['Top'] = True
            player.rect.top = tile.bottom
            player.momentum = 0.2
    return player.rect, collision_type
