import arcade

class CollisionService:
    @staticmethod
    def check_player_hit(player, enemy_lasers):
        hits = arcade.check_for_collision_with_list(player, enemy_lasers)
        if hits:
            for h in hits:
                h.remove_from_sprite_lists()
            player.lives -= 1
            return True
        return False
