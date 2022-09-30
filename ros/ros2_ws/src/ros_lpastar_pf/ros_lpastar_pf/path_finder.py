from ros_lpastar_pf.agent_client import AgentClient
from ros_lpastar_pf.sensor_client import SensorClient
import rclpy
from rclpy.node import Node
from lpastar_pf.LPAStarPathFinder import LPAStarPathFinder
from lpastar_pf.exception.MapInitializationException \
    import MapInitializationException
from lpastar_pf.exception.TimeoutException import TimeoutException
from typing import Dict
from pf_interfaces import Goal
#import sys


class PathFinder(Node):

    def __init__(self, params: Dict[str, int]) -> None:
        super().__init__('path_finder')
        self.agent_client = AgentClient()
        self.sensor_client = SensorClient()
        self.path_service = self.create_service(Goal, \
            "pf_path_finder", self.path_finder_callback)
        try:
            self.path_finder = LPAStarPathFinder(
                agent=self.agent_client,
                sensor=self.sensor_client,
                params=params
            )
        except MapInitializationException:
            self.get_logger().info("Failed to initialize path-finder. There must be missing parameters. \
            check example config.")
            exit(1)
        self.goal = None

    def path_finder_callback(self, request, response) -> None:
        status = 0
        goal = (request.x, request.y)
        try:
            self.path_finder.find_path(goal)
        except TimeoutException:
            self.get_logger().info("Path-finder timeout exceeded for goal (%f, %f)", goal[0], goal[1])
            status += 1
        pos = self.agent_client.get_position()
        x, y = (pos[0], pos[1])
        if (x, y) != goal:
            self.get_logger().info("Goal is not reached. Goal is: (%f, %f), actual position is (%f, %f)", \
            goal[0], goal[1], x, y)
            status += 2
        response.status = status
        return response


def main(args=None):
    rclpy.init(args=args)

    # yaml reading
    pf = PathFinder()

    rclpy.spin(pf)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
