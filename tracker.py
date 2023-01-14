from typing import List

# Config & Params
CONST_Y_THRESHOLD_DOWN = 0.25
CONST_Y_THRESHOLD_UP = 0.75 * CONST_Y_THRESHOLD_DOWN

CONST_EWM_ALPHA = 0.75

class Pair:
    def __init__(self, item_l, item_r):
        self.data = {
            "left": item_l,
            "right": item_r
        }

    def get(self, hand):
        return self.data[hand]

    def set(self, hand, val):
        self.data[hand] = val

    def is_valid(self, hand):
        return self.data[hand] is not None

    def set_none(self, hand):
        self.set(hand, None)


class MoveTracker:
    def __init__(self, y_threshold_down=CONST_Y_THRESHOLD_DOWN, y_threshold_up=CONST_Y_THRESHOLD_UP):
        self.max_y = Pair(None, None)
        self.min_y = Pair(None, None)
        self.curr_y = Pair(None, None)
        self.is_alr_down = Pair(False, False)
        self.y_threshold_down = y_threshold_down
        self.y_threshold_up = y_threshold_up

    def update_movement(self, move_data) -> (bool, List):
        is_boo = False
        boo_lst = []
        updated = {
            "left": False, "right": False
        }

        # item is (hand, y_diff, z_mean)
        for item in move_data:
            hand = item[0]

            # TODO: determine ema or just copy over
            if self.curr_y.is_valid(hand):
                self.curr_y.set(hand, self.curr_y.get(hand) * (1-CONST_EWM_ALPHA) + item[1] * CONST_EWM_ALPHA)
            else:
                self.curr_y.set(hand, item[1])
            updated[hand] = True

            # update min
            if not self.min_y.is_valid(hand) or self.min_y.get(hand) > self.curr_y.get(hand):
                self.min_y.set(hand, self.curr_y.get(hand))

            # calculate threshold
            if self.is_alr_down.get(hand) == False and self.max_y.is_valid(hand) \
                    and self.max_y.get(hand) - self.curr_y.get(hand) >= self.y_threshold_down:
                is_boo = True
                boo_lst.append(hand)
                self.is_alr_down.set(hand, True)

            # check if need to update max_y
            # case 1: when init
            # case 2: move up some dist
            if not self.max_y.is_valid(hand) \
                    or self.is_alr_down.get(hand) and self.min_y.is_valid(hand) \
                    and self.curr_y.get(hand) - self.min_y.get(hand) >= self.y_threshold_up:
                print("Hey")
                self.max_y.set(hand, self.curr_y.get(hand))
                self.is_alr_down.set(hand, False)

            self.max_y.set(hand, max(self.max_y.get(hand), self.curr_y.get(hand)))

        # set missing to None
        # for hand in updated.keys():
        #     if not updated[hand]:
        #         # self.curr_y[hand] = None  # TODO: max_y???
        # tmp_i = 1
        return is_boo, boo_lst
