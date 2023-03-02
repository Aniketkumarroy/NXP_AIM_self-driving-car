// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from nxp_cup_interfaces:msg/PixyVector.idl
// generated code does not contain a copyright notice

#ifndef NXP_CUP_INTERFACES__MSG__DETAIL__PIXY_VECTOR__BUILDER_HPP_
#define NXP_CUP_INTERFACES__MSG__DETAIL__PIXY_VECTOR__BUILDER_HPP_

#include "nxp_cup_interfaces/msg/detail/pixy_vector__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace nxp_cup_interfaces
{

namespace msg
{

namespace builder
{

class Init_PixyVector_m1_y1
{
public:
  explicit Init_PixyVector_m1_y1(::nxp_cup_interfaces::msg::PixyVector & msg)
  : msg_(msg)
  {}
  ::nxp_cup_interfaces::msg::PixyVector m1_y1(::nxp_cup_interfaces::msg::PixyVector::_m1_y1_type arg)
  {
    msg_.m1_y1 = std::move(arg);
    return std::move(msg_);
  }

private:
  ::nxp_cup_interfaces::msg::PixyVector msg_;
};

class Init_PixyVector_m1_x1
{
public:
  explicit Init_PixyVector_m1_x1(::nxp_cup_interfaces::msg::PixyVector & msg)
  : msg_(msg)
  {}
  Init_PixyVector_m1_y1 m1_x1(::nxp_cup_interfaces::msg::PixyVector::_m1_x1_type arg)
  {
    msg_.m1_x1 = std::move(arg);
    return Init_PixyVector_m1_y1(msg_);
  }

private:
  ::nxp_cup_interfaces::msg::PixyVector msg_;
};

class Init_PixyVector_m1_y0
{
public:
  explicit Init_PixyVector_m1_y0(::nxp_cup_interfaces::msg::PixyVector & msg)
  : msg_(msg)
  {}
  Init_PixyVector_m1_x1 m1_y0(::nxp_cup_interfaces::msg::PixyVector::_m1_y0_type arg)
  {
    msg_.m1_y0 = std::move(arg);
    return Init_PixyVector_m1_x1(msg_);
  }

private:
  ::nxp_cup_interfaces::msg::PixyVector msg_;
};

class Init_PixyVector_m1_x0
{
public:
  explicit Init_PixyVector_m1_x0(::nxp_cup_interfaces::msg::PixyVector & msg)
  : msg_(msg)
  {}
  Init_PixyVector_m1_y0 m1_x0(::nxp_cup_interfaces::msg::PixyVector::_m1_x0_type arg)
  {
    msg_.m1_x0 = std::move(arg);
    return Init_PixyVector_m1_y0(msg_);
  }

private:
  ::nxp_cup_interfaces::msg::PixyVector msg_;
};

class Init_PixyVector_m0_y1
{
public:
  explicit Init_PixyVector_m0_y1(::nxp_cup_interfaces::msg::PixyVector & msg)
  : msg_(msg)
  {}
  Init_PixyVector_m1_x0 m0_y1(::nxp_cup_interfaces::msg::PixyVector::_m0_y1_type arg)
  {
    msg_.m0_y1 = std::move(arg);
    return Init_PixyVector_m1_x0(msg_);
  }

private:
  ::nxp_cup_interfaces::msg::PixyVector msg_;
};

class Init_PixyVector_m0_x1
{
public:
  explicit Init_PixyVector_m0_x1(::nxp_cup_interfaces::msg::PixyVector & msg)
  : msg_(msg)
  {}
  Init_PixyVector_m0_y1 m0_x1(::nxp_cup_interfaces::msg::PixyVector::_m0_x1_type arg)
  {
    msg_.m0_x1 = std::move(arg);
    return Init_PixyVector_m0_y1(msg_);
  }

private:
  ::nxp_cup_interfaces::msg::PixyVector msg_;
};

class Init_PixyVector_m0_y0
{
public:
  explicit Init_PixyVector_m0_y0(::nxp_cup_interfaces::msg::PixyVector & msg)
  : msg_(msg)
  {}
  Init_PixyVector_m0_x1 m0_y0(::nxp_cup_interfaces::msg::PixyVector::_m0_y0_type arg)
  {
    msg_.m0_y0 = std::move(arg);
    return Init_PixyVector_m0_x1(msg_);
  }

private:
  ::nxp_cup_interfaces::msg::PixyVector msg_;
};

class Init_PixyVector_m0_x0
{
public:
  explicit Init_PixyVector_m0_x0(::nxp_cup_interfaces::msg::PixyVector & msg)
  : msg_(msg)
  {}
  Init_PixyVector_m0_y0 m0_x0(::nxp_cup_interfaces::msg::PixyVector::_m0_x0_type arg)
  {
    msg_.m0_x0 = std::move(arg);
    return Init_PixyVector_m0_y0(msg_);
  }

private:
  ::nxp_cup_interfaces::msg::PixyVector msg_;
};

class Init_PixyVector_timestamp
{
public:
  Init_PixyVector_timestamp()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PixyVector_m0_x0 timestamp(::nxp_cup_interfaces::msg::PixyVector::_timestamp_type arg)
  {
    msg_.timestamp = std::move(arg);
    return Init_PixyVector_m0_x0(msg_);
  }

private:
  ::nxp_cup_interfaces::msg::PixyVector msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::nxp_cup_interfaces::msg::PixyVector>()
{
  return nxp_cup_interfaces::msg::builder::Init_PixyVector_timestamp();
}

}  // namespace nxp_cup_interfaces

#endif  // NXP_CUP_INTERFACES__MSG__DETAIL__PIXY_VECTOR__BUILDER_HPP_
