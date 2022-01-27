class PossibleMovementsList():

    def __init__(self):
        # Mixed or other movements - prioridade 1
        # Os outros 3 - prioridade 2
        # Comentário pra upar o código

        self.walking_movements_listed = ["walk_forward", "rotate_clockwise", "rotate_counter_clockwise"]
        self.page_movements_listed = ["left_kick", "right_kick", "stand_up_front", "stand_up_back", "squat", "left_defense", "right_defense"]
        self.moving_head_movements_listed = ["head_to_left","head_to_right","head_to_up","head_to_down", "head_to_center", "head_search"]
        self.mixed_or_other_movements_listed = ["nothing_request", "body_alignment_to_left", "body_alignment_to_right", "emergency_shutdown"]
        

        self.all_movements_listed = self.walking_movements_listed + self.page_movements_listed + self.moving_head_movements_listed + self.mixed_or_other_movements_listed
        self.dict_movements_listed_and_their_status = dict.fromkeys(self.all_movements_listed,False)
        self.dict_priority_movements = dict.fromkeys(self.mixed_or_other_movements_listed,False)