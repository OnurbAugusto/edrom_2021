#!/usr/bin/env python3
#coding=utf-8

import rospy
from modularized_bhv_msgs.msg import currentStateMsg
from modularized_bhv_msgs.srv import moveRequest

#Setando a grafia correta das requisições para movimento de caminhada
FORWARD = 'walk_forward'

class WalkingRoutine():

    def __init__(self):
        
        self.move_request = rospy.ServiceProxy('/bhv2mov_communicator/3D_move_requisitions', moveRequest)
        rospy.Subscriber('/transitions_and_states/state_machine', currentStateMsg, self.flagUpdate)

        self.flag = False

        while not rospy.is_shutdown():
            self.createRequest()
    
    def flagUpdate(self, msg):
        if msg.currentState == 'walking':
            self.flag = True
        else:
            self.flag = False
        
    def createRequest(self):

        if self.flag:
            self.move_request(FORWARD)


if __name__ == '__main__':
    rospy.init_node('Walking_node', anonymous=False)

    routine = WalkingRoutine()
    rospy.spin()