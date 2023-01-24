#include "example_interfaces/srv/add_two_ints.hpp"
#include "rclcpp/rclcpp.hpp"

class ServiceServer01 :public rclcpp::Node
{
public:
    ServiceServer01(std::string name) : Node(name)
    {
        RCLCPP_INFO(this->get_logger(),"节点已启动：%s.", name.c_str());
        //创建服务
        add_ints_server_ =this->create_service<example_interfaces::srv::AddTwoInts>(
            "add_two_ints_srv",
            std::bind(&ServiceServer01::handle_add_two_ints,this,
            std::placeholders::_1,std::placeholders::_2)
        );

    }
private:
    //声明服务
    rclcpp::Service<example_interfaces::srv::AddTwoInts>::SharedPtr add_ints_server_;
    //收到请求后的处理函数
    //参数是service的固定格式
    void handle_add_two_ints(const std::shared_ptr<example_interfaces::srv::AddTwoInts::Request> request,
    std::shared_ptr<example_interfaces::srv::AddTwoInts::Response> response)
    {
         RCLCPP_INFO(this->get_logger(), "收到a: %ld b: %ld", request->a,
                request->b);
    response->sum = request->a + request->b;
    };
};
