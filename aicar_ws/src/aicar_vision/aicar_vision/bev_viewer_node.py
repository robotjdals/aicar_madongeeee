import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image


class BevViewerNode(Node):
    def __init__(self):
        super().__init__('bev_viewer_node')
        self.get_logger().info('BEV Viewer Node started.')

        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            Image, '/image_bev_binary', self.image_callback, 10
        )

    def image_callback(self, msg):
        try:
            bev_image = self.bridge.imgmsg_to_cv2(msg, 'mono8')
        except Exception as exc:
            self.get_logger().error(f'Failed to convert BEV image: {exc}')
            return

        cv2.imshow('BEV View', bev_image)
        cv2.waitKey(1)

    def destroy_node(self):
        cv2.destroyAllWindows()
        return super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = BevViewerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
