#include "rclcpp/rclcpp.hpp"

class Node01 : public rclcpp::Node
{
    public:
        Node01(std::string name):Node(name)
        {
            RCLCPP_INFO(this->get_logger(), "Hello,im %s.",name.c_str());
        }
    private:
};

int main(int argc, char **argv)
{
    rclcpp::init(argc,argv);
    auto node = std::make_shared<Node01>("node_01");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}