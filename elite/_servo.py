'''
Author: Elite_zhangjunjie
CreateDate: 
LastEditors: Elite_zhangjunjie
LastEditTime: 2022-05-10 10:16:52
Description: 伺服相关类
'''

import time
from enum import Enum

from elite._baseec import BaseEC


class ECServo(BaseEC):
    """伺服服务
    """
    




    
    
#  伺服服务 
    @property
    def mode(self) -> BaseEC.RobotMode:
        """获取机器人的模式

        Returns
        -------
            RobotMode: 0示教,1运行,2远程
        
        Examples
        --------
        >>> from elite import EC
        >>> ec = EC(ip="192.168.1.200", auto_connect=True)
        >>> print(ec.mode)  # => RobotMode.TECH
        """
        return self.RobotMode(self.send_CMD("getRobotMode"))
      
    
    @property
    def state(self) -> BaseEC.RobotState:
        """获取机器人运行状态
            #!本指令获取的急停状态只会短暂存在,很快会被报警覆盖,如果需要获取急停状态,请使用robot_get_estop_status()
            
        Returns
        -------
            RobotState: 0停止,1暂停,2急停,3运行,4错误,5碰撞
            
        Examples
        --------
        >>> from elite import EC
        >>> ec = EC(ip="192.168.1.200", auto_connect=True)
        >>> print(ec.state)  # => RobotState.STOP
        """
        return self.RobotState(self.send_CMD("getRobotState"))
    
    
    @property
    def estop_status(self) -> int:
        """获取机器人的紧急停止状态(硬件的状态)

        Returns
        -------
            int: 0:非急停,1: 急停
        """
        return self.send_CMD("get_estop_status")
    
    
    @property
    def servo_status(self) -> bool:
        """获取伺服状态

        Returns
        -------
            bool: True启用,False未启用
        """
        return self.send_CMD("getServoStatus")
    
    
    def servo_status_set(self, _status:int = 1) -> bool:
        """设置机器人伺服状态

        Args
        ----
            status (int, optional): 1上伺服,0下伺服. Defaults to 1.

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("set_servo_status",{"status":_status})
        
        
    def sync(self) -> bool:
        """编码器同步

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("syncMotorStatus")
    
    
    @property
    def sync_status(self) -> bool:
        """获取同步状态

        Returns
        -------
            bool: True同步,False未同步
        """
        return self.send_CMD("getMotorStatus")
    
    
    def clear_alarm(self) -> bool:
        """清除报警

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("clearAlarm")


    def wait_stop(self) -> None:
        """等待机器人运动停止
        """
        while True:
            time.sleep(0.005)
            result = self.state
            if result != self.RobotState.PLAY:
                if result != self.RobotState.STOP:
                    str_ = ["","state of robot in the pause","state of robot in the emergency stop","","state of robot in the error","state of robot in the collision"]
                    self.logger.debug(str_[result.value])
                    break
                break
        self.logger.info("The robot has stopped")


    def calibrate_encoder_zero(self) -> bool:
        """编码器零位校准,如果可以校准则返回True并不在乎校准结果,如果不可以校准,返回error,

        Returns
        -------
            bool: 成功 True,失败 False
        """
        return self.send_CMD("calibrate_encoder_zero_position")
       
    