import pandas as pd

# ====================
# Config & Params
# ====================
const_wrist_idx = [15, 16]
const_hand_idx = [
    [17, 19, 21],
    [18, 20, 22]
]
const_hand_names = ['left', 'right']
const_vis_threshold = 0.05


# ====================
# Utility Functions
# ====================
def format_pose_to_lst(processed):
    local_landmarks = processed.pose_landmarks.landmark
    global_landmarks = processed.pose_world_landmarks.landmark

    local_res = []
    for land_mark in local_landmarks:
        local_res.append({
            "x": land_mark.x,
            "y": land_mark.y,
            "z": land_mark.z,
            "vis": land_mark.visibility
        })

    global_res = []
    for land_mark in global_landmarks:
        global_res.append({
            "x": land_mark.x,
            "y": land_mark.y,
            "z": land_mark.z,
            "vis": land_mark.visibility
        })
    return local_res, global_res


def format_pose_to_df(processed):
    local_lst, global_lst = format_pose_to_lst(processed)

    # create df
    local_df = pd.DataFrame(local_lst)
    local_df['idx'] = local_df.index
    global_df = pd.DataFrame(global_lst)
    global_df['idx'] = global_df.index
    return local_df, global_df


def get_hand_movement_from_df(df):
    df_present = df[df['vis'] > const_vis_threshold].reset_index()

    res = []
    for i in range(2):
        hand = const_hand_names[i]
        # if const_wrist_idx[i] not in df_present['idx'].tolist():
        #     continue

        df_curr_hand = df_present[df_present['idx'].isin(const_hand_idx[i])]
        if df_curr_hand.shape[0] == 0:
            continue

        # wrist and at least one hand keypoint present
        # y_diff = df_curr_hand['y'].mean() - df_present[df_present['idx'] == const_wrist_idx[i]]['y'].mean()
        # z_mean = df_present[(df_present['idx'].isin(const_hand_idx[i])) |
        #                     (df_present['idx'] == const_wrist_idx[i])]['z'].mean()
        # res.append((hand, y_diff, z_mean))

        df_hand = df_present[(df_present['idx'].isin(const_hand_idx[i])) |
                            (df_present['idx'] == const_wrist_idx[i])]
        if df_hand.shape[0] >= 2:
            y_mean = df_hand['y'].mean()
            z_mean = df_hand['z'].mean()
            res.append((hand, y_mean, z_mean))

    return res


# i.e. from the mp result
def get_hand_movement_from_raw(processed, is_local=False):
    df = format_pose_to_df(processed)[0] if is_local else format_pose_to_df(processed)[1]
    return get_hand_movement_from_df(df)
