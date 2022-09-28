import rclpy
from rclpy.node import Node
from lpastar_pf.GAgent import GAgent
from pf_interfaces.srv import Move, Position, Stop
from typing import Tuple


class AgentClient(Node, GAgent):

    def __init__(self) -> None:
        Node.__init__(self, "pf_agent_client")
        GAgent.__init__(self)
        self.move_cli = self.create_client(Move, "pf_move")
        self.position_cli = self.create_client(Position, "pf_position")
        self.stop_cli = self.create_client(Stop, "pf_stop")

        while not self.move_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Move service is not available. Retry...")
        self.move_req = Move.Request()

        while not self.position_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Move service is not available. Retry...")
        self.position_req = Move.Request()

        while not self.stop_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Move service is not available. Retry...")
        self.stop_req = Move.Request()

    def get_position(self) -> Tuple[float, float, float]:
        self.position_future = self.position_cli.call_async(self.position_req)
        rclpy.spin_until_future_complete(self, self.position_future)
        res = self.position_future.result()
        return (res[0], res[1], res[2])

    def move(self, x: float, y: float) -> None:
        self.move_req.x = x
        self.move_req.y = y
        self.move_future = self.move_cli.call_async(self.move_req)
        rclpy.spin_until_future_complete(self, self.move_future)
        res = self.move_future.result()
        if not res:
            self.get_logger().info("Can't move to \
            (%f, %f). Internal service issue.", (x, y))

    def stop(self) -> None:
        self.stop_future = self.stop_cli.call_async(self.stop_req)
        rclpy.spin_until_future_complete(self, self.stop_future)
        res = self.stop_future.result()
        if not res:
            self.get_logger().info("Robot can't stop. Internal service issue.")
