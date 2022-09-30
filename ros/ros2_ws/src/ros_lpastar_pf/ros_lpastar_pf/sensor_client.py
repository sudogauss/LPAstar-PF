import rclpy
from rclpy.Node import Node
from lpastar_pf.ASensor import ASensor
from pf_interfaces.srv import Scan
from typing import Tuple, Iterable


class SensorClient(Node, ASensor):

    def __init__(self) -> None:
        Node.__init__(self, "pf_sensor_client")
        self.scan_cli = self.create_client(Scan, "pf_scan")

        while not self.scan_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Scan service is not available. Retry...")
        self.scan_req = Scan.Request()

    def scan(self, origin: Tuple[float, float, float]) -> Iterable[Tuple[float, float, float]]:
        self.scan_req.origin = [origin[0], origin[1], origin[2]]
        res = self.scan_req.call(self.scan_req)
        return [(res.obstacles_xs[i], res.obstacles_ys[i], res.obstacles_ws[i]) for i in range(len(res.obstacles_xs))]
