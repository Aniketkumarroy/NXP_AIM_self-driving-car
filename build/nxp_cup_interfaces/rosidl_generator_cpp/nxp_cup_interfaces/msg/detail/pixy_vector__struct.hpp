// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from nxp_cup_interfaces:msg/PixyVector.idl
// generated code does not contain a copyright notice

#ifndef NXP_CUP_INTERFACES__MSG__DETAIL__PIXY_VECTOR__STRUCT_HPP_
#define NXP_CUP_INTERFACES__MSG__DETAIL__PIXY_VECTOR__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__nxp_cup_interfaces__msg__PixyVector __attribute__((deprecated))
#else
# define DEPRECATED__nxp_cup_interfaces__msg__PixyVector __declspec(deprecated)
#endif

namespace nxp_cup_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct PixyVector_
{
  using Type = PixyVector_<ContainerAllocator>;

  explicit PixyVector_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->timestamp = 0ull;
      this->m0_x0 = 0;
      this->m0_y0 = 0;
      this->m0_x1 = 0;
      this->m0_y1 = 0;
      this->m1_x0 = 0;
      this->m1_y0 = 0;
      this->m1_x1 = 0;
      this->m1_y1 = 0;
    }
  }

  explicit PixyVector_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->timestamp = 0ull;
      this->m0_x0 = 0;
      this->m0_y0 = 0;
      this->m0_x1 = 0;
      this->m0_y1 = 0;
      this->m1_x0 = 0;
      this->m1_y0 = 0;
      this->m1_x1 = 0;
      this->m1_y1 = 0;
    }
  }

  // field types and members
  using _timestamp_type =
    uint64_t;
  _timestamp_type timestamp;
  using _m0_x0_type =
    uint8_t;
  _m0_x0_type m0_x0;
  using _m0_y0_type =
    uint8_t;
  _m0_y0_type m0_y0;
  using _m0_x1_type =
    uint8_t;
  _m0_x1_type m0_x1;
  using _m0_y1_type =
    uint8_t;
  _m0_y1_type m0_y1;
  using _m1_x0_type =
    uint8_t;
  _m1_x0_type m1_x0;
  using _m1_y0_type =
    uint8_t;
  _m1_y0_type m1_y0;
  using _m1_x1_type =
    uint8_t;
  _m1_x1_type m1_x1;
  using _m1_y1_type =
    uint8_t;
  _m1_y1_type m1_y1;

  // setters for named parameter idiom
  Type & set__timestamp(
    const uint64_t & _arg)
  {
    this->timestamp = _arg;
    return *this;
  }
  Type & set__m0_x0(
    const uint8_t & _arg)
  {
    this->m0_x0 = _arg;
    return *this;
  }
  Type & set__m0_y0(
    const uint8_t & _arg)
  {
    this->m0_y0 = _arg;
    return *this;
  }
  Type & set__m0_x1(
    const uint8_t & _arg)
  {
    this->m0_x1 = _arg;
    return *this;
  }
  Type & set__m0_y1(
    const uint8_t & _arg)
  {
    this->m0_y1 = _arg;
    return *this;
  }
  Type & set__m1_x0(
    const uint8_t & _arg)
  {
    this->m1_x0 = _arg;
    return *this;
  }
  Type & set__m1_y0(
    const uint8_t & _arg)
  {
    this->m1_y0 = _arg;
    return *this;
  }
  Type & set__m1_x1(
    const uint8_t & _arg)
  {
    this->m1_x1 = _arg;
    return *this;
  }
  Type & set__m1_y1(
    const uint8_t & _arg)
  {
    this->m1_y1 = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    nxp_cup_interfaces::msg::PixyVector_<ContainerAllocator> *;
  using ConstRawPtr =
    const nxp_cup_interfaces::msg::PixyVector_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<nxp_cup_interfaces::msg::PixyVector_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<nxp_cup_interfaces::msg::PixyVector_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      nxp_cup_interfaces::msg::PixyVector_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<nxp_cup_interfaces::msg::PixyVector_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      nxp_cup_interfaces::msg::PixyVector_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<nxp_cup_interfaces::msg::PixyVector_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<nxp_cup_interfaces::msg::PixyVector_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<nxp_cup_interfaces::msg::PixyVector_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__nxp_cup_interfaces__msg__PixyVector
    std::shared_ptr<nxp_cup_interfaces::msg::PixyVector_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__nxp_cup_interfaces__msg__PixyVector
    std::shared_ptr<nxp_cup_interfaces::msg::PixyVector_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PixyVector_ & other) const
  {
    if (this->timestamp != other.timestamp) {
      return false;
    }
    if (this->m0_x0 != other.m0_x0) {
      return false;
    }
    if (this->m0_y0 != other.m0_y0) {
      return false;
    }
    if (this->m0_x1 != other.m0_x1) {
      return false;
    }
    if (this->m0_y1 != other.m0_y1) {
      return false;
    }
    if (this->m1_x0 != other.m1_x0) {
      return false;
    }
    if (this->m1_y0 != other.m1_y0) {
      return false;
    }
    if (this->m1_x1 != other.m1_x1) {
      return false;
    }
    if (this->m1_y1 != other.m1_y1) {
      return false;
    }
    return true;
  }
  bool operator!=(const PixyVector_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PixyVector_

// alias to use template instance with default allocator
using PixyVector =
  nxp_cup_interfaces::msg::PixyVector_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace nxp_cup_interfaces

#endif  // NXP_CUP_INTERFACES__MSG__DETAIL__PIXY_VECTOR__STRUCT_HPP_
