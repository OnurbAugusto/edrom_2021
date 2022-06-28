#!/usr/bin/env python3
#coding=utf-8

import rospy
from controller import Supervisor

from modularized_bhv_msgs.srv import moveRequest, moveRequestResponse #Srv associado ao service utilizado para requisitar qualquer movimento dos motores

#Limites relacionados aos motores da cabeça em radianos
hor_increment = ((1.7+1.7)/10) #Valores de incremento obtidos através do step
ver_increment = ((1.47)/10) #dos motores do pescoço na neck_interpreter.py

#Setando a grafia correta das requisições para a cabeça
RIGHT = 'head_to_right'
LEFT = 'head_to_left'
UP = 'head_to_up'
DOWN = 'head_to_down'
CENTER = 'head_to_center'
POSSIBLE_REQUESTS = [RIGHT, LEFT, UP, DOWN, CENTER]

class HeadMover():

    def __init__(self, supervisor):
        """
        Construtor:
        - Faz a chamada de funções para definir as variáveis field e ros dos motores da simulação.
        """
        self.general_supervisor = supervisor

        self.init_head()
    
    #Função de chamada recorrente no bhv_sim
    def callClock(self):
        """
        -> Funcao:
        Chamar o metodo para atualizacao interna da posicao da cabeca.
        """
        self.motorUpdate()
    
    #Função chamada no loop para atualizar internamente a posição atual dos motores da cabeça
    def motorUpdate(self):
        """
        -> Funcao:
        Atualizar a posição dos motores da cabeça, atraves de:
            - Capturar a posição no momento através do campo da rotação dos motores.
        """
        self.hor_head_pos = self.sim_hor_head_motor.getSFRotation()[3]
        self.ver_head_pos = self.sim_ver_head_motor.getSFRotation()[3]
    
    #Função chamada pelo construtor para habilitação da movimentação da cabeça
    def init_head(self):
        """
        -> Funcao:
        Inicializar todas as variáveis necessárias para movimentação dos motores da cabeça, atraves de:
            - Capturar os nodes de Transform de cada motor;
            - Capturar seus campos de rotação;
            - Iniciar as variáveis que indica as posições dos motores da cabeça;
            - Inicializa as variáveis do ROS para recebimento de requisição de movimento da cabeça.
        """
        sim_horizontal_head_motor_node = self.general_supervisor.getFromDef('HorizontalMotor')
        sim_vertical_head_motor_node = self.general_supervisor.getFromDef('VerticalMotor')

        self.sim_hor_head_motor = sim_horizontal_head_motor_node.getField('rotation')
        self.sim_ver_head_motor = sim_vertical_head_motor_node.getField('rotation')

        self.hor_head_pos = self.sim_hor_head_motor.getSFRotation()[3]
        self.ver_head_pos = self.sim_ver_head_motor.getSFRotation()[3]

        rospy.Service('/bhv2mov_communicator/head_requisitions', moveRequest, self.moveSimHead)
        self.response = moveRequestResponse()
        
    #Função responsável pela movimentação da cabeça de acordo com as requisições
    def moveSimHead(self, request):
        """
        -> Funcao:
        Alterar o campo de rotação dos nodes da cabeça para simular o movimento do pescoço, atraves de:
            - Verificar a requisição de direção do movimento para determinar o sentido de rotação;
            - Verificar a requisição de direção do movimento para determinar o motor a ser utilizado;
            - Construir o novo vetor de rotação, atraves de campos já existentes e um incremento no último index;
            - Enviar a nova rotação ao simulador;
            - Retornar a informação de sucesso após movimentar.
        """
        if request.moveRequest in POSSIBLE_REQUESTS:
            calm_down = True
            initial_time = self.general_supervisor.getTime()
        else:
            calm_down = False

        direction = request.moveRequest

        if direction == RIGHT or direction == DOWN:
            increment = 1
        elif direction == LEFT or direction == UP:
            increment = -1

        if direction == RIGHT or direction == LEFT:
            increment *= hor_increment
            rotation = self.sim_hor_head_motor.getSFRotation()[:3]+[round(self.hor_head_pos+increment,2)]
            self.sim_hor_head_motor.setSFRotation(rotation)
        elif direction == UP or direction == DOWN:
            increment *= ver_increment
            rotation = self.sim_ver_head_motor.getSFRotation()[:3]+[round(self.ver_head_pos+increment,2)]
            self.sim_ver_head_motor.setSFRotation(rotation)
        elif direction == CENTER:
            hor_rotation = self.sim_hor_head_motor.getSFRotation()[:3]+[0]
            ver_rotation = self.sim_ver_head_motor.getSFRotation()[:3]+[0.45]
            self.sim_hor_head_motor.setSFRotation(hor_rotation)
            self.sim_ver_head_motor.setSFRotation(ver_rotation)

        if calm_down:
            while self.general_supervisor.getTime()-initial_time < 0.1:
                pass
        
        self.response.success = True
        return self.response

