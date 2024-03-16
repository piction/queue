#!/bin/python3
import matplotlib.pyplot as plt
import numpy as np
import utils

class Occupation:
  def __init__(self,enter_time,leave_time,robot_id,is_stranded):
    self.enter_time =enter_time
    self.leave_time =leave_time
    self.robot_id =robot_id
    self.is_stranded = is_stranded
  @classmethod
  def enter_robot(cls, robot_id, enter_time):
    return cls(enter_time, {}, robot_id, True)
  @classmethod
  def enter_leave_robot(cls, robot_id, enter_time, leave_time):
    return cls(enter_time, leave_time, robot_id, False)
  def has_overlap (self, enter_time, leave_time):
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
  def leave_robot(self,leave_time):
    self.occupations[-1].leave_time = leave_time
    self.occupations[-1].is_stranded = False
  def pass_with_robot(self, robot_id, enter_time, leave_time):
    self.occupations.append(Occupation.enter_leave_robot(robot_id, enter_time, leave_time))
  
  def can_enter_robot(self):
    if self.occupations.len == 0:
      return True
    if self.occupations[-1].is_stranded:
      return False
    else:
      return True
  
  def get_earliest_enter_time(self):
    if not self.can_enter_robot():
      raise Exception("No robot can enter")
    if self.occupations.len == 0:
      return 0
    return self.occupations[-1].leave_time
    
  def can_pass(self,  enter_time, leave_time):
    if self.occupations.len == 0:
      return True
    if self.occupations[-1].is_stranded:
      return False
    return not any([occupation.has_overlap(enter_time, leave_time) for occupation in self.occupations])
    

class Spot:
  def __init__(self,xy_position, phi):
    self.pos = np.array([0,0])
    self.phi = phi
    self.occupations = Occupations()

class Route:
  def __init__(self, spots) -> None:
    self.spots = spots


def get_trajectory_time(self, spots_list):
  spot_points= [spot.pos for spot in spots_list]
  utils.removeIntermediatePathPoints (spot_points)
  max_vel = 10
  max_acc =3
  total_time =0
  for i in range(len(spot_points)-1):
      distance = spot_points[i]-spot_points[i+1].norm()
      time, velocity = utils.velocity_profile(distance, max_vel, max_acc)
      total_time += time
  return total_time

def try_move(spots_list, start_time, robot_id):
  total_time = get_trajectory_time(spots_list)
  end_time = start_time + total_time
  # check time interval with occupations
  pass_occupation=Occupation.enter_leave_robot(robot_id, start_time, end_time)
  enter_occupation =Occupation.enter_robot(robot_id, start_time)




class Queue:
  def __init__(self, spots_map) -> None:
    self.spots = spots_map.spots
    self.enter_routes = {} # map with lists of routes for every enter spot




#plot time velocity with matplotlib
plt.plot(time, velocity)
plt.show()

