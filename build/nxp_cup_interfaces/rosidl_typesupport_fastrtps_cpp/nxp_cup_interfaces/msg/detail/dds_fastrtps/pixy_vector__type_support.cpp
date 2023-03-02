// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from nxp_cup_interfaces:msg/PixyVector.idl
// generated code does not contain a copyright notice
#include "nxp_cup_interfaces/msg/detail/pixy_vector__rosidl_typesupport_fastrtps_cpp.hpp"
#include "nxp_cup_interfaces/msg/detail/pixy_vector__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace nxp_cup_interfaces
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_nxp_cup_interfaces
cdr_serialize(
  const nxp_cup_interfaces::msg::PixyVector & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: timestamp
  cdr << ros_message.timestamp;
  // Member: m0_x0
  cdr << ros_message.m0_x0;
  // Member: m0_y0
  cdr << ros_message.m0_y0;
  // Member: m0_x1
  cdr << ros_message.m0_x1;
  // Member: m0_y1
  cdr << ros_message.m0_y1;
  // Member: m1_x0
  cdr << ros_message.m1_x0;
  // Member: m1_y0
  cdr << ros_message.m1_y0;
  // Member: m1_x1
  cdr << ros_message.m1_x1;
  // Member: m1_y1
  cdr << ros_message.m1_y1;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_nxp_cup_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  nxp_cup_interfaces::msg::PixyVector & ros_message)
{
  // Member: timestamp
  cdr >> ros_message.timestamp;

  // Member: m0_x0
  cdr >> ros_message.m0_x0;

  // Member: m0_y0
  cdr >> ros_message.m0_y0;

  // Member: m0_x1
  cdr >> ros_message.m0_x1;

  // Member: m0_y1
  cdr >> ros_message.m0_y1;

  // Member: m1_x0
  cdr >> ros_message.m1_x0;

  // Member: m1_y0
  cdr >> ros_message.m1_y0;

  // Member: m1_x1
  cdr >> ros_message.m1_x1;

  // Member: m1_y1
  cdr >> ros_message.m1_y1;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_nxp_cup_interfaces
get_serialized_size(
  const nxp_cup_interfaces::msg::PixyVector & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: timestamp
  {
    size_t item_size = sizeof(ros_message.timestamp);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: m0_x0
  {
    size_t item_size = sizeof(ros_message.m0_x0);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: m0_y0
  {
    size_t item_size = sizeof(ros_message.m0_y0);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: m0_x1
  {
    size_t item_size = sizeof(ros_message.m0_x1);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: m0_y1
  {
    size_t item_size = sizeof(ros_message.m0_y1);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: m1_x0
  {
    size_t item_size = sizeof(ros_message.m1_x0);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: m1_y0
  {
    size_t item_size = sizeof(ros_message.m1_y0);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: m1_x1
  {
    size_t item_size = sizeof(ros_message.m1_x1);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: m1_y1
  {
    size_t item_size = sizeof(ros_message.m1_y1);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_nxp_cup_interfaces
max_serialized_size_PixyVector(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;


  // Member: timestamp
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Member: m0_x0
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: m0_y0
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: m0_x1
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: m0_y1
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: m1_x0
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: m1_y0
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: m1_x1
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: m1_y1
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }

  return current_alignment - initial_alignment;
}

static bool _PixyVector__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const nxp_cup_interfaces::msg::PixyVector *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _PixyVector__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<nxp_cup_interfaces::msg::PixyVector *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _PixyVector__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const nxp_cup_interfaces::msg::PixyVector *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _PixyVector__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_PixyVector(full_bounded, 0);
}

static message_type_support_callbacks_t _PixyVector__callbacks = {
  "nxp_cup_interfaces::msg",
  "PixyVector",
  _PixyVector__cdr_serialize,
  _PixyVector__cdr_deserialize,
  _PixyVector__get_serialized_size,
  _PixyVector__max_serialized_size
};

static rosidl_message_type_support_t _PixyVector__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_PixyVector__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace nxp_cup_interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_nxp_cup_interfaces
const rosidl_message_type_support_t *
get_message_type_support_handle<nxp_cup_interfaces::msg::PixyVector>()
{
  return &nxp_cup_interfaces::msg::typesupport_fastrtps_cpp::_PixyVector__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, nxp_cup_interfaces, msg, PixyVector)() {
  return &nxp_cup_interfaces::msg::typesupport_fastrtps_cpp::_PixyVector__handle;
}

#ifdef __cplusplus
}
#endif
