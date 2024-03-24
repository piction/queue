#!/bin/python3
import matplotlib.pyplot as plt
import numpy as np
import utils


class Occupation:
    def __init__(self, enter_time, leave_time, robot_id, is_stranded):
        self.enter_time = enter_time
        self.leave_time = leave_time
        self.robot_id = robot_id
        self.is_stranded = is_stranded

    @classmethod
    def enter_robot(cls, robot_id, enter_time):
        return cls(enter_time, {}, robot_id, True)

    @classmethod
    def enter_leave_robot(cls, robot_id, enter_time, leave_time):
        return cls(enter_time, leave_time, robot_id, False)

    def has_overlap(self, enter_time, leave_time):
        if self.is_stranded and enter_time >= self.enter_time:
            return True
        if self.enter_time >= enter_time and enter_time <= self.leave_time:
            return True
        if self.enter_time <= leave_time and leave_time <= self.leave_time:
            return True
        return False


class Occupations:
    def __init__(self):
        self.occupations = []

    def enter_robot(self, robot_id, enter_time):
        self.occupations.append(Occupation.enter_robot(robot_id, enter_time))

    def leave_robot(self, leave_time):
        self.occupations[-1].leave_time = leave_time
        self.occupations[-1].is_stranded = False

    def pass_with_robot(self, robot_id, enter_time, leave_time):
        self.occupations.append(
            Occupation.enter_leave_robot(robot_id, enter_time, leave_time)
        )

    def can_enter_robot(self):
        if len(self.occupations) == 0:
            return True
        if self.occupations[-1].is_stranded:
            return False
        else:
            return True

    def get_earliest_enter_time(self):
        if not self.can_enter_robot():
            raise Exception("No robot can enter")
        if len(self.occupations) == 0:
            return 0
        return self.occupations[-1].leave_time

    def can_pass(self, enter_time, leave_time):
        if len(self.occupations) == 0:
            return True
        if self.occupations[-1].is_stranded:
            return False
        return not any(
            [
                occupation.has_overlap(enter_time, leave_time)
                for occupation in self.occupations
            ]
        )


class Spot:
    def __init__(self, xy_position, phi):
        self.pos = xy_position
        self.phi = phi
        self.occupations = Occupations()


class Route:
    def __init__(self, spots) -> None:
        self.spots = spots


def get_trajectory_time(spots_list):
    spot_points = [spot.pos for spot in spots_list]
    utils.removeIntermediatePathPoints(spot_points)
    max_vel = 10
    max_acc = 3
    total_time = 0
    for i in range(len(spot_points) - 1):
        distance = np.linalg.norm(spot_points[i] - spot_points[i + 1])
        time, velocity = utils.velocity_profile(distance, max_vel, max_acc)
        total_time += time[-1]
    return total_time


def try_move(spots_list, start_time, robot_id):
    total_time = get_trajectory_time(spots_list)
    end_time = start_time + total_time
    # copy spots_list
    spots_list = spots_list.copy()
    # check time interval with occupations
    spots_list[0].occupations.leave_robot(start_time)
    if not spots_list[-1].occupations.can_enter_robot():
        return (False, {})
    earliest_enter_time = spots_list[-1].occupations.get_earliest_enter_time()
    if end_time < earliest_enter_time:
        return (False, {})
    spots_list[-1].occupations.enter_robot(robot_id, end_time)

    if len(spots_list) > 2:
        for i in range(1, len(spots_list) - 1):
            if not spots_list[i].occupations.can_pass(start_time, end_time):
                return (False, {})
            spots_list[i].occupations.pass_with_robot(robot_id, start_time, end_time)
    return (True, spots_list)


class Queue:
    def __init__(self, spots_map) -> None:
        self.spots = spots_map.spots
        self.enter_routes = {}  # map with lists of routes for every enter spot


spot1 = Spot(np.array([0, 0]), 0)
spot2 = Spot(np.array([0, 2]), 0)
spot3 = Spot(np.array([0, 4]), 0)
spots = [spot1, spot2, spot3]
spots[0].occupations.enter_robot("robot_1", 0)
(can_move, new_spot_list) = try_move(spots, 0, "robot_1")
if ( can_move):
  spots = new_spot_list


print(can_move)
