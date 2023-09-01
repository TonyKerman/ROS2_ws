# URDF

一种构建可视化机器人模型的文件

使用xml语言编写

## 快速查看模型

一个不用ros查看urdf的软件

[urdf-viewer](https://github.com/openrr/urdf-viz)

## URDF的组成介绍

一般情况下，URDF由声明信息和两种关键组件共同组成

### 声明信息

声明信息包含两部分，第一部分是xml的声明信息，放在第一行 第二部分是机器人的声明，通过robot标签就可以声明一个机器人模型

```xml
<?xml version="1.0"?>
<robot name="fishbot">
    <link></link>
    <joint></joint>
......
</robot>
```

## 两种关键组件(Joint&Link)

### Link：部件

我们把左轮，右轮、支撑轮子，IMU和雷达部件称为机器人的Link

声明一个 Link
```xml
<link name="base_link">

</link>
```

通过两行代码就可以定义好base_link，但现在的base_link是空的，我们还要声明我们的base_link长什么样，通过visual子标签就可以声明出来机器人的visual形状

```xml
<!-- base link -->
<link name="base_link">
    <visual>
    <origin xyz="0 0 0.0" rpy="0 0 0"/>
    <geometry>
        <cylinder length="0.12" radius="0.10"/>
    </geometry>
    </visual>
</link>
```

#### link的子标签列表

    <visual> 显示形状
    <geometry> (几何形状)
        <box> 长方体
        标签属性: size-长宽高
        举例：<box size="1 1 1" />

        <cylinder> 圆柱体
        标签属性:radius -半径 length-高度
        举例：<cylinder radius="1" length="0.5"/>

        <sphere> 球体
        属性：radius -半径
        举例：<sphere radius="0.015"/>

        <mesh> 第三方导出的模型文件
        属性：filename
        举例: <mesh filename="package://robot_description/meshes/base_link.DAE"/>
    
    <origin> (可选：默认在物体几何中心)
    属性 xyz默认为零矢量 rpy 弧度 表示的翻滚、俯仰、偏航
    举例：<origin xyz="0 0 0" rpy="0 0 0" />

    <material> 材质
    属性 name 名字

    <color>
    属性 rgba a代表透明度
    举例：<material name="white"><color rgba="1.0 1.0 1.0 0.5" /> </material>

    <collision> 碰撞属性，仿真章节中讲解
    <inertial> 惯性参数 质量等，仿真章节中讲解

### Joint：关节

而Link和Link之间的连接部分称之为Joint关节
joint为机器人关节，机器人关节用于连接两个机器人部件，主要写明父子关系

* 父子之间的连接类型，包括是否固定的，可以旋转的等
* 父部件名字
* 子部件名字
* 父子之间相对位置
* 父子之间的旋转轴，绕哪个轴转


## eg.创建图形

创建一个圆柱形

```xml
<?xml version="1.0"?>
<robot name="myfirst">
<link name="base_link">
    <visual>
    <geometry>
        <cylinder length="0.6" radius="0.2"/>
    </geometry>
    </visual>
</link>
</robot>
```

创建一个多link模型

```xml
<?xml version="1.0"?>
<robot name="bot">
    
  <!-- base link -->
  <link name="base_link">
      <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <!--<cylinder length="0.12" radius="0.10"/> -->
        <box size="0.7 0.7 0.2"/>
      </geometry>
    </visual>
  </link>
    
  <!-- laser link -->
  <link name="laser_link">
      <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <cylinder length="0.05" radius="0.05"/>
      </geometry>
      <material name="black">
          <color rgba="0.0 0.0 0.0 0.5" /> 
      </material>
    </visual>
  </link>
    
  <!-- laser joint -->
    <joint name="laser_joint" type="fixed">
        <parent link="base_link" />
        <child link="laser_link" />
        <origin xyz="0.3 0 0.125" />
    </joint>

</robot>

```

## solidworks导出urdf

## 参考
[链接](https://fishros.com/d2lros2/#/humble/chapt8/get_started/1.URDF%E7%BB%9F%E4%B8%80%E6%9C%BA%E5%99%A8%E4%BA%BA%E5%BB%BA%E6%A8%A1%E8%AF%AD%E8%A8%80)